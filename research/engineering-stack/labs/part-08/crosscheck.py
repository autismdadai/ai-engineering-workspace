"""Optional cross-check against the OpenAI Agents SDK (pip install openai-agents==0.23.1).

A fake model, defined here, stands in for a real one, so nothing is sent to
OpenAI: tracing is switched off before anything runs, and no API key is needed.
It checks two behaviours this part reports from the SDK's source code:
  B1  the default turn cap is 10 and going past it raises MaxTurnsExceeded
  B2  by default a failing tool's exception text is not shown to the model
and compares B1 with the lab's own loop.
Prints PASS, FAIL or SKIP lines; exits 1 if any check fails or the SDK is missing.
"""
import asyncio
import os
import sys

os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "1"   # no tracing upload
results = []


def report(label, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'} {label}{': ' + str(detail) if detail != '' else ''}")


try:
    from importlib.metadata import version
    from agents import Agent, MaxTurnsExceeded, Runner, function_tool, set_tracing_disabled
    from agents.items import ModelResponse
    from agents.models.interface import Model
    from agents.usage import Usage
    from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage, \
        ResponseOutputText
except ImportError:
    print("SKIP openai-agents is not installed (pip install -r requirements-crosscheck.txt)")
    sys.exit(1)

set_tracing_disabled(True)
print(f"INFO openai-agents {version('openai-agents')} on Python {sys.version.split()[0]}; "
      "tracing off, no network calls")


def tool_call(n, name):
    return ResponseFunctionToolCall(type="function_call", call_id=f"c{n}", name=name,
                                    arguments="{}", id=f"fc{n}", status="completed")


def final(text):
    return ResponseOutputMessage(id="m1", type="message", role="assistant", status="completed",
                                 content=[ResponseOutputText(type="output_text", text=text,
                                                             annotations=[])])


class FakeModel(Model):
    """Calls `tool` on every turn, or once and then answers, as told."""

    def __init__(self, tool, then_answer=False):
        self.tool, self.then_answer, self.calls, self.inputs = tool, then_answer, 0, []

    async def get_response(self, system_instructions, input, *args, **kwargs):
        self.calls += 1
        self.inputs.append(input)
        if self.then_answer and self.calls > 1:
            output = [final("done")]
        else:
            output = [tool_call(self.calls, self.tool)]
        return ModelResponse(output=output, usage=Usage(), response_id=None)

    def stream_response(self, *args, **kwargs):
        raise NotImplementedError


@function_tool
def list_files() -> str:
    """List the files."""
    return "README.md"


@function_tool
def broken_tool() -> str:
    """Always fails."""
    raise ValueError("secret detail: upstream returned HTTP 500")


async def main():
    looping = FakeModel("list_files")
    agent = Agent(name="looper", instructions="", model=looping, tools=[list_files])
    try:
        await Runner.run(agent, "go")
        report("B1 the default turn cap stops a model that never finishes", False, "no exception")
    except MaxTurnsExceeded as error:
        report("B1 the default turn cap stops a model that never finishes",
               looping.calls == 10, f"MaxTurnsExceeded after {looping.calls} model calls: {error}")

    failing = FakeModel("broken_tool", then_answer=True)
    agent = Agent(name="breaker", instructions="", model=failing, tools=[broken_tool])
    await Runner.run(agent, "go")
    sent = str(failing.inputs[-1])
    report("B2 a failing tool's exception text is kept from the model by default",
           "An error occurred while running the tool" in sent and "secret detail" not in sent,
           "the model saw the generic message only")

    from agent_loop import run_agent
    from stand_in import LoopingModel, lab_tools
    ours = LoopingModel()
    result = run_agent(ours, lab_tools(), "go", max_turns=10)
    report("B3 the lab's loop stops at the same cap when set to 10",
           result.status == "max_turns" and ours.calls == looping.calls, f"{ours.calls} calls")


asyncio.run(main())
print(f"\n{sum(results)} of {len(results)} cross-checks passed")
sys.exit(0 if results and all(results) else 1)
