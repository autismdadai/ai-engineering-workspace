"""Review a `docker run` command for running untrusted agent code.

It reads the command, never runs it. It is a checklist for the options it
knows, not a guarantee: it can't see the image, the daemon's settings, a
compose file or anything the container does once it starts. It reports
dangerous options (which remove isolation) and missing hardening options, each
with a short reason (Part 08, Section 3.7). Even a clean result shares the host
kernel unless a runtime such as gVisor's runsc is used, and runtime bugs have
allowed escapes.

It fails closed: an option it doesn't recognise is assumed to take a value,
and if it can't find the image name it says so and doesn't report "ok".

Usage: python sandbox_check.py "docker run --rm ... image cmd"
Prints JSON. Exit code 0 only if "ok" is true; 1 otherwise; 2 for a usage error.
"""
import json
import shlex
import sys

# docker run's on/off flags (they take no value). Every other option is
# assumed to take one, so an unfamiliar option can't hide the rest.
LONG_FLAGS = {"--detach", "--interactive", "--tty", "--rm", "--privileged", "--read-only",
              "--init", "--no-healthcheck", "--oom-kill-disable", "--publish-all",
              "--disable-content-trust", "--quiet", "--sig-proxy", "--help"}
SHORT_FLAGS = set("ditPq")              # -d -i -t -P -q
SHORT_NAMES = {"-v": "--volume", "-e": "--env", "-u": "--user", "-m": "--memory",
               "-w": "--workdir", "-p": "--publish", "-h": "--hostname", "-l": "--label",
               "-a": "--attach", "-c": "--cpu-shares", "-d": "--detach", "-i": "--interactive",
               "-t": "--tty", "-P": "--publish-all", "-q": "--quiet"}

# Host folders that are dangerous to mount: the whole folder, or anything inside it.
SYSTEM_PATHS = ("/etc", "/proc", "/sys", "/dev", "/boot", "/var/run", "/run", "/var/lib/docker",
                "/usr", "/bin", "/sbin", "/lib")
# Dangerous when mounted whole. A project folder inside /home is normal, but it
# still exposes everything in it: mount only what the task needs, read-only.
WHOLE_PATHS = ("/", "/home", "/root", "/var", "/var/lib")

DANGEROUS = {
    "privileged": "--privileged turns off the protections: 'not a securely sandboxed process'",
    "runtime_socket": "mounting a container-runtime socket (docker, containerd, podman) gives "
                      "root-level control of the host",
    "host_path_mount": "mounting a sensitive host path (/, /etc, /var/run, /home, ...) exposes the host",
    "host_namespace": "sharing a host namespace (network, pid, ipc, uts, userns, cgroupns) "
                      "or another container's removes isolation",
    "cap_add": "--cap-add gives back a Linux capability; each one needs a reason",
    "seccomp_off": "seccomp=unconfined removes the default system-call filter",
    "lsm_off": "apparmor=unconfined, label=disable or systempaths=unconfined removes a protection",
    "root_user": "--user 0 or root runs as root inside the container",
    "device": "--device passes a host device into the container",
}

HARDENING = {
    "network_none": "--network none: only a loopback device, no network",
    "cap_drop_all": "--cap-drop ALL: drop the 14 default capabilities too",
    "no_new_privileges": "--security-opt no-new-privileges: su, sudo and setuid gains stop working",
    "read_only": "--read-only: the root filesystem can't be written",
    "pids_limit": "--pids-limit N (N > 0): caps the number of processes",
    "memory": "--memory N (N > 0): caps memory (set --memory-swap to the same value for no swap)",
    "cpus": "--cpus N (N > 0): caps CPU time",
    "non_root_user": "--user with a non-root ID",
}


def parse(command):
    """Return ([(long_name, value)], image) for a docker run command."""
    words = shlex.split(command)
    if words[:2] == ["docker", "run"]:
        words = words[2:]
    elif words[:3] == ["docker", "container", "run"]:
        words = words[3:]
    else:
        raise ValueError("expected a command starting with 'docker run'")
    options, i = [], 0
    while i < len(words) and words[i].startswith("-") and words[i] != "--":
        word = words[i]
        if word.startswith("--"):
            if "=" in word:
                name, value = word.split("=", 1)
            elif word in LONG_FLAGS:
                name, value = word, None
            else:
                if i + 1 >= len(words):
                    raise ValueError(f"{word} needs a value")
                name, value = word, words[i + 1]
                i += 1
            options.append((name, value))
        else:
            letters = word[1:]
            for k, letter in enumerate(letters):
                if letter in SHORT_FLAGS:
                    options.append((SHORT_NAMES.get("-" + letter, "-" + letter), None))
                    continue
                rest = letters[k + 1:]
                if rest:
                    value = rest[1:] if rest.startswith("=") else rest
                else:
                    if i + 1 >= len(words):
                        raise ValueError(f"-{letter} needs a value")
                    value = words[i + 1]
                    i += 1
                options.append((SHORT_NAMES.get("-" + letter, "-" + letter), value))
                break
        i += 1
    if i < len(words) and words[i] == "--":
        i += 1
    image = words[i] if i < len(words) else None
    return options, image


def last(options, *names):
    found = [v for n, v in options if n in names]
    return found[-1] if found else None


def number(value):
    try:
        return float(str(value).rstrip("bkmgBKMG"))
    except (TypeError, ValueError):
        return None


def mount_source(name, value):
    """The host side of a -v or --mount value, if any."""
    if name == "--volume":
        return value.split(":")[0] if ":" in value else None
    for part in value.split(","):
        key, _, val = part.partition("=")
        if key.strip() in ("source", "src"):
            return val.strip()
    return None


def review(command):
    options, image = parse(command)
    danger, notes = set(), []
    for name, value in options:
        v = (value or "").strip()
        lower = v.lower()
        if name == "--privileged" and lower not in ("false", "0"):
            danger.add("privileged")
        elif name in ("--volume", "--mount"):
            source = mount_source(name, v) or ""
            path = source.rstrip("/") or ("/" if source.startswith("/") else "")
            if ".sock" in source or source.endswith(("docker", "containerd", "podman")):
                danger.add("runtime_socket")
            elif path and (path in WHOLE_PATHS or
                           any(path == p or path.startswith(p + "/") for p in SYSTEM_PATHS)):
                danger.add("host_path_mount")
        elif name in ("--network", "--net", "--pid", "--ipc", "--uts", "--userns", "--cgroupns"):
            if lower == "host" or lower.startswith("container:"):
                danger.add("host_namespace")
        elif name == "--cap-add":
            danger.add("cap_add")
        elif name == "--security-opt":
            compact = lower.replace(" ", "").replace(":", "=")
            if compact == "seccomp=unconfined":
                danger.add("seccomp_off")
            elif compact in ("apparmor=unconfined", "label=disable", "systempaths=unconfined"):
                danger.add("lsm_off")
        elif name == "--user":
            if v.split(":")[0] in ("0", "root"):
                danger.add("root_user")
        elif name == "--device":
            danger.add("device")

    present = set()
    if (last(options, "--network", "--net") or "").lower() == "none":
        present.add("network_none")
    if any(n == "--cap-drop" and (v or "").upper() == "ALL" for n, v in options):
        present.add("cap_drop_all")
    if any(n == "--security-opt" and (v or "").replace(":", "=") in
           ("no-new-privileges", "no-new-privileges=true") for n, v in options):
        present.add("no_new_privileges")
    read_only = [v for n, v in options if n == "--read-only"]
    if read_only and (read_only[-1] is None or read_only[-1].lower() in ("true", "1")):
        present.add("read_only")
    for key, names in (("pids_limit", ("--pids-limit",)), ("memory", ("--memory",)),
                       ("cpus", ("--cpus",))):
        value = number(last(options, *names))
        if value is not None and value > 0:
            present.add(key)
    user = last(options, "--user")
    if user and user.split(":")[0] not in ("0", "root"):
        present.add("non_root_user")
    if image is None:
        notes.append("no image name found: the command may be incomplete or use an option "
                      "this checker doesn't know")
    runtime = last(options, "--runtime")
    return {
        "image": image,
        "dangerous": {k: DANGEROUS[k] for k in sorted(danger)},
        "missing": {k: HARDENING[k] for k in HARDENING if k not in present},
        "notes": notes,
        "runtime": runtime or "default (runc: shares the host kernel)",
        "ok": not danger and len(present) == len(HARDENING) and image is not None,
    }


def main(argv):
    if len(argv) != 1:
        print(__doc__)
        return 2
    try:
        report = review(argv[0])
    except ValueError as error:
        print(f"error: {error}")
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
