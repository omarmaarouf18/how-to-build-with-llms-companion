import pathlib
import subprocess
import sys

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
MODEL = "claude-opus-5-5"       # use any current model name
ROOT = pathlib.Path.cwd().resolve()
SECRETS = (".env", ".ssh", ".aws", ".pem", ".key", "id_rsa", "credentials")

# [3] Context: the system prompt says who the agent is and how it works
SYSTEM = ("You are a coding agent working in the current directory. "
          "Use your tools to inspect files and run commands. "
          "Verify your work before you say you are done.")

# [7] Tool registry: what the model is allowed to ask for
TOOLS = [
    {"name": "read_file",
     "description": "Read a text file in the project and return it.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string"}},
                      "required": ["path"]}},
    {"name": "run_command",
     "description": "Run a shell command in the project directory.",
     "input_schema": {"type": "object",
                      "properties": {"command": {"type": "string"}},
                      "required": ["command"]}},
]

# [8] Permission layer: reads stay inside the project and away from
#     secrets; every command needs a human
def allowed(name, args):
    if name == "read_file":
        path = (ROOT / args["path"]).resolve()
        if path != ROOT and ROOT not in path.parents:
            return False
        rel = str(path.relative_to(ROOT))   # check only the part inside
        return not any(s in rel for s in SECRETS)
    answer = input(f"\nAllow {name} {args}? [y/N] ")
    return answer.strip().lower() == "y"

# [9] Executor: the harness, not the model, actually runs things
def run_tool(name, args):
    if not allowed(name, args):
        return "Denied by the permission layer."
    try:
        if name == "read_file":
            text = (ROOT / args["path"]).read_text(encoding="utf-8")
            return text[:20000]
        if name == "run_command":
            r = subprocess.run(args["command"], shell=True, cwd=ROOT,
                               capture_output=True, text=True,
                               timeout=120)
            out = (r.stdout + r.stderr)[-20000:]
            return f"exit code {r.returncode}\n{out}"
    except Exception as e:
        return f"Error: {e}"
    return f"Unknown tool: {name}"

# [2] The loop: call the model, run what it asks for, feed results back
def agent(task, max_steps=25):
    messages = [{"role": "user", "content": task}]
    for _ in range(max_steps):
        response = client.messages.create(
            model=MODEL, max_tokens=16000, system=SYSTEM,
            tools=TOOLS, messages=messages)
        messages.append({"role": "assistant",
                         "content": response.content})
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content
                           if b.type == "text")
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"-> {block.name} {block.input}")
                results.append({"type": "tool_result",
                                "tool_use_id": block.id,
                                "content": run_tool(block.name,
                                                    block.input)})
        messages.append({"role": "user", "content": results})
    return "Stopped: step limit reached."

# [1] Interface: the simplest one, a command line
if __name__ == "__main__":
    print(agent(" ".join(sys.argv[1:]) or "What does this project do?"))
