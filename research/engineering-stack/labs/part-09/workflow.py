"""A small durable workflow engine, for learning (Engineering Stack, Part 09).

Standard library only. It shows the ideas behind LangGraph, Temporal and
similar tools, at toy scale:

- a graph of steps (nodes) that may loop, with a step limit;
- a checkpoint saved after every step, keyed by a thread id, so a run that
  crashes or pauses can resume where it stopped (durability "sync");
- pausing for a person (interrupt) and resuming: the paused step runs again
  from its start, so code before the pause runs twice;
- retries with exponential backoff and full jitter;
- an idempotency store, so a retried side effect happens once.

Not a production engine: one process at a time per thread, no locking, and
checkpoints are plain JSON files. Section 3 of the part explains each idea.
"""
import hashlib
import hmac
import json
import os
import random
import re
import time

END = "__end__"
_THREAD_ID = re.compile(r"[A-Za-z0-9_-]{1,64}")


class Interrupt(Exception):
    """Raised inside a step to pause the run until a person answers."""

    def __init__(self, value, index):
        super().__init__(f"paused at interrupt {index}")
        self.value = value
        self.index = index


class TransientError(Exception):
    """A failure worth retrying (a timeout, a 429 or a 5xx, say)."""


class StepLimitError(RuntimeError):
    """The run took more steps than allowed without reaching END."""


class IdempotencyError(ValueError):
    """The same idempotency key was reused with different parameters."""


class StateTamperedError(ValueError):
    """A signed checkpoint failed its signature check."""


class RetryPolicy:
    """Exponential backoff with full jitter (AWS's "full jitter").

    The wait before retry n (n = 0, 1, ...) is a random number between 0
    and min(cap, initial * factor ** n). max_attempts counts the first try.
    """

    def __init__(self, max_attempts=3, initial=0.5, factor=2.0, cap=128.0,
                 retry_on=(TransientError,)):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.max_attempts = max_attempts
        self.initial = initial
        self.factor = factor
        self.cap = cap
        self.retry_on = retry_on

    def delay(self, n, rng):
        return rng.uniform(0, min(self.cap, self.initial * self.factor ** n))


class Context:
    """Given to each step. Its interrupt() pauses the run for a person."""

    def __init__(self, resume_values):
        self._resume = list(resume_values)
        self._index = 0

    def interrupt(self, value):
        """Return the person's answer, or pause the run if there is none yet.

        Answers are matched to interrupts by position, so a step must call
        interrupt() in the same order every time it runs.
        """
        index = self._index
        self._index += 1
        if index < len(self._resume):
            return self._resume[index]
        raise Interrupt(value, index)


class FileCheckpointer:
    """Saves one JSON checkpoint per thread in a folder.

    With a secret, each file carries an HMAC-SHA256 signature, and a file
    changed by anyone without the secret is refused on load.
    """

    def __init__(self, folder, secret=None):
        self.folder = folder
        self.secret = secret.encode() if isinstance(secret, str) else secret
        os.makedirs(folder, exist_ok=True)

    def _path(self, thread_id):
        if not isinstance(thread_id, str) or not _THREAD_ID.fullmatch(thread_id):
            raise ValueError("thread_id must be 1 to 64 letters, digits, _ or -")
        return os.path.join(self.folder, thread_id + ".json")

    def _sign(self, body):
        return hmac.new(self.secret, body.encode(), hashlib.sha256).hexdigest()

    def save(self, thread_id, checkpoint):
        body = json.dumps(checkpoint, sort_keys=True)
        record = {"checkpoint": body}
        if self.secret:
            record["signature"] = self._sign(body)
        path = self._path(thread_id)
        temp = path + ".tmp"
        with open(temp, "w", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)  # all or nothing: never a half-written file

    def load(self, thread_id):
        path = self._path(thread_id)
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as handle:
            record = json.load(handle)
        body = record["checkpoint"]
        if self.secret:
            expected = self._sign(body)
            if not hmac.compare_digest(expected, str(record.get("signature", ""))):
                raise StateTamperedError(f"checkpoint for {thread_id!r} was changed")
        return json.loads(body)


class Workflow:
    """A graph of steps. Each step takes (state, ctx) and returns updates."""

    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.retry = {}
        self.entry = None

    def add_node(self, name, fn, retry=None):
        if name == END or name in self.nodes:
            raise ValueError(f"bad or duplicate node name {name!r}")
        self.nodes[name] = fn
        self.retry[name] = retry or RetryPolicy(max_attempts=1)
        if self.entry is None:
            self.entry = name

    def add_edge(self, source, target):
        self.edges[source] = lambda state: target

    def add_router(self, source, router):
        """router(state) returns the next node's name, or END."""
        self.edges[source] = router

    def _next(self, name, state):
        if name not in self.edges:
            return END
        target = self.edges[name](state)
        if target != END and target not in self.nodes:
            raise ValueError(f"step {name!r} routed to unknown step {target!r}")
        return target

    def _call(self, name, state, ctx, sleep, rng, log):
        policy = self.retry[name]
        for attempt in range(policy.max_attempts):
            ctx._index = 0  # a retried step starts over, interrupts included
            try:
                return self.nodes[name](dict(state), ctx)
            except Interrupt:
                raise  # a pause is not a failure: never retried
            except policy.retry_on as error:
                log.append({"step": name, "attempt": attempt + 1, "error": str(error)})
                if attempt + 1 == policy.max_attempts:
                    raise
                sleep(policy.delay(attempt, rng))
        raise AssertionError("unreachable")

    def run(self, thread_id, checkpointer, state=None, resume=None,
            step_limit=25, sleep=time.sleep, rng=None):
        """Start or continue a thread. Returns its latest checkpoint.

        Pass `state` to start a new thread, `resume` to answer a pause, or
        neither to continue a thread that crashed. The checkpoint's
        "status" is "done", "interrupted" (see "pending") or "running".
        """
        rng = rng or random.Random()
        cp = checkpointer.load(thread_id)
        if cp is None:
            if state is None:
                raise ValueError(f"no thread {thread_id!r}; pass state= to start one")
            cp = {"node": self.entry, "state": dict(state), "step": 0,
                  "resume": [], "status": "running", "log": []}
            checkpointer.save(thread_id, cp)
        elif state is not None:
            raise ValueError(f"thread {thread_id!r} already exists")
        if cp["status"] == "done":
            return cp
        if cp["status"] == "interrupted":
            if resume is None:
                raise ValueError(f"thread {thread_id!r} is paused; pass resume=")
            cp["resume"].append(resume)
            cp["status"] = "running"
            cp.pop("pending", None)
        elif resume is not None:
            raise ValueError(f"thread {thread_id!r} is not paused")

        while True:
            name = cp["node"]
            if name == END:
                cp["status"] = "done"
                checkpointer.save(thread_id, cp)
                return cp
            if cp["step"] >= step_limit:
                raise StepLimitError(
                    f"step limit of {step_limit} reached without reaching END")
            ctx = Context(cp["resume"])
            try:
                update = self._call(name, cp["state"], ctx, sleep, rng, cp["log"])
            except Interrupt as pause:
                cp["status"] = "interrupted"
                cp["pending"] = {"step": name, "index": pause.index, "value": pause.value}
                checkpointer.save(thread_id, cp)
                return cp
            new_state = {**cp["state"], **(update or {})}
            cp = {"node": self._next(name, new_state), "state": new_state,
                  "step": cp["step"] + 1, "resume": [], "status": "running",
                  "log": cp["log"]}
            checkpointer.save(thread_id, cp)  # saved before the next step starts


class IdempotencyStore:
    """Remembers the result of each side effect by key, in a JSON file.

    Same key and same parameters: the stored result comes back and the
    effect does not run again. Same key with different parameters: an error.
    The effect and the record are not one transaction, so a crash between
    them still repeats the effect; real systems put the key in the same
    database transaction, or the receiving service checks it (as payment
    APIs do).
    """

    def __init__(self, path):
        self.path = path

    def _read(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, encoding="utf-8") as handle:
            return json.load(handle)

    def run(self, key, params, effect):
        fingerprint = hashlib.sha256(
            json.dumps(params, sort_keys=True).encode()).hexdigest()
        records = self._read()
        if key in records:
            if records[key]["fingerprint"] != fingerprint:
                raise IdempotencyError(f"key {key!r} reused with different parameters")
            return records[key]["result"]
        result = effect(**params)
        records[key] = {"fingerprint": fingerprint, "result": result}
        temp = self.path + ".tmp"
        with open(temp, "w", encoding="utf-8") as handle:
            json.dump(records, handle)
        os.replace(temp, self.path)
        return result


def approved(answer):
    """Only an explicit approval approves; anything else is a no."""
    return isinstance(answer, dict) and answer.get("decision") == "approve"
