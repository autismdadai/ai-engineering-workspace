"""Several agents, in miniature (Engineering Stack, Part 09 lab).

Standard library only, with no model: "agents" are plain functions, and
text is measured in words as a stand-in for tokens. It shows how context
moves between agents, what that costs, how errors compound, and why extra
voters help only when their mistakes are independent. The numbers it prints
are toy numbers, not measurements of any product.
"""
import random


def words(messages):
    """Size of a list of messages, in words (a stand-in for tokens)."""
    return sum(len(m["text"].split()) for m in messages)


def handoff_input(history, instructions):
    """A handoff: the next agent sees the whole conversation so far."""
    return [{"role": "system", "text": instructions}] + list(history)


def as_tool_input(brief, instructions):
    """Agent as a tool: the worker sees only the brief the manager wrote."""
    return [{"role": "system", "text": instructions}, {"role": "user", "text": brief}]


def remove_tool_messages(history):
    """A history filter that drops tool messages, like a 'remove tools' filter.

    It cannot remove tool output that an assistant message already quoted.
    """
    return [m for m in history if m["role"] != "tool"]


def run_subagent(brief, documents, summary_words=12):
    """A worker reads its documents in its own context and returns a summary.

    Returns (summary, words_the_worker_read). Only the summary goes back.
    """
    read = len(brief.split()) + sum(len(d.split()) for d in documents)
    text = " ".join(" ".join(documents).split()[:summary_words])
    return f"Summary: {text}", read


def orchestrator_cost(n_workers, read, summary, brief):
    """Toy arithmetic for one lead and n workers (all in tokens).

    Returns (worker_total, lead_extra, single_agent_extra): what the workers
    process in total, how much the lead's context grows, and how much one
    agent's context would grow if it read everything itself.
    """
    worker_total = n_workers * (brief + read + summary)
    lead_extra = n_workers * (brief + summary)
    single_agent_extra = n_workers * read
    return worker_total, lead_extra, single_agent_extra


def chain_success(p, k):
    """End-to-end success of k steps that each succeed with probability p."""
    return p ** k


def majority_vote_accuracy(p_correct, voters, shared_error, trials, seed=0):
    """Share of questions a majority vote gets right, by simulation.

    Each voter is right with probability p_correct. With probability
    shared_error, all voters share one draw (their mistakes are correlated,
    say from the same model and prompt); otherwise each draws on its own.
    Ties count as wrong.
    """
    rng = random.Random(seed)
    right = 0
    for _ in range(trials):
        if rng.random() < shared_error:
            votes = [rng.random() < p_correct] * voters
        else:
            votes = [rng.random() < p_correct for _ in range(voters)]
        right += sum(votes) * 2 > voters
    return right / trials


def pass_along(text, agents=3, tag=False):
    """Agents that copy their input into their output, like a careless chain.

    With tag=True, text from another agent is wrapped as data before the
    next agent sees it. The text still arrives; what changes is that the
    receiver can tell it is data, not an instruction. Tagging lowers the
    risk; it is not a guarantee.
    """
    for i in range(agents):
        if tag:
            text = f"<data from='agent-{i}'>{text}</data>"
        text = f"Agent {i + 1} notes: {text}"
    return text
