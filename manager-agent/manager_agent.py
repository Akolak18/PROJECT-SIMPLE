"""
Manager Agent — orchestrates specialized sub-agents via the Anthropic API.
Uses claude-opus-4-7 with adaptive thinking and tool use.
"""
import json
import uuid
from datetime import datetime
import anthropic
from sub_agents import FileAgent, CodeAgent, SearchAgent, DataAgent

client = anthropic.Anthropic()

# Sub-agent registry
AGENTS: dict = {
    "FileAgent": FileAgent(),
    "CodeAgent": CodeAgent(),
    "SearchAgent": SearchAgent(),
    "DataAgent": DataAgent(),
}

# Task state: task_id -> task record
tasks: dict = {}

TOOLS = [
    {
        "name": "list_agents",
        "description": (
            "List all available sub-agents with their descriptions and capabilities. "
            "Call this first when you are unsure which agent handles a given task type."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    {
        "name": "delegate_to_agent",
        "description": (
            "Delegate a task to a specialized sub-agent and get results immediately. "
            "The agent executes the task synchronously and returns results.\n\n"
            "Context keys per agent:\n"
            "- FileAgent: path (str), content (str for write), directory (str for list)\n"
            "- CodeAgent: code (str, optional), language (str, optional)\n"
            "- SearchAgent: query (str)\n"
            "- DataAgent: data (list | dict | str), threshold (number), operator ('gt'|'lt'|'gte'|'lte')"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_name": {
                    "type": "string",
                    "enum": ["FileAgent", "CodeAgent", "SearchAgent", "DataAgent"],
                    "description": "Which sub-agent to delegate to",
                },
                "task": {
                    "type": "string",
                    "description": "Clear, specific task description for the sub-agent",
                },
                "context": {
                    "type": "object",
                    "description": "Parameters needed by the agent (see parent description)",
                },
            },
            "required": ["agent_name", "task"],
            "additionalProperties": False,
        },
    },
    {
        "name": "list_tasks",
        "description": "Show all tasks that have been delegated in this session, their statuses and agents used.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
]

SYSTEM_PROMPT = """You are a Manager Agent — an intelligent orchestrator that coordinates specialized sub-agents to fulfill user requests.

Your workflow:
1. Understand what the user wants to achieve
2. Identify which sub-agents are needed (use list_agents if unsure)
3. Break the work into sub-tasks and delegate each to the right agent
4. Report what you are doing at each step
5. Synthesize all results into a clear, complete response

Sub-agents available:
- FileAgent: File I/O — reading, writing, listing files and directories
- CodeAgent: Software tasks — generate, analyze, explain, review, or fix code
- SearchAgent: Research — find information on any topic
- DataAgent: Data work — statistics, aggregations, JSON analysis

Principles:
- Always explain which agents you are using and why
- For multi-step tasks, delegate each step sequentially or in parallel where possible
- If an agent returns an error, explain it to the user and suggest alternatives
- Keep responses focused and actionable"""


def _execute_tool(name: str, input_data: dict) -> str:
    if name == "list_agents":
        payload = {
            "agents": [
                {"name": n, "description": a.description, "capabilities": a.capabilities}
                for n, a in AGENTS.items()
            ]
        }
        return json.dumps(payload, ensure_ascii=False)

    elif name == "delegate_to_agent":
        agent_name = input_data.get("agent_name", "")
        task = input_data.get("task", "")
        context = input_data.get("context") or {}

        if agent_name not in AGENTS:
            return json.dumps({"error": f"Unknown agent '{agent_name}'. Available: {list(AGENTS)}"})

        task_id = str(uuid.uuid4())[:8]
        tasks[task_id] = {
            "status": "running",
            "agent": agent_name,
            "task": task,
            "result": None,
            "created_at": datetime.now().isoformat(),
        }

        print(f"\n  [{agent_name}] Starting: {task[:80]}{'...' if len(task) > 80 else ''}")

        try:
            result = AGENTS[agent_name].execute(task, context)
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["result"] = result
            print(f"  [{agent_name}] ✓ Done (task {task_id})")
            return json.dumps({"task_id": task_id, "status": "completed", "result": result}, ensure_ascii=False)
        except Exception as exc:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["result"] = str(exc)
            print(f"  [{agent_name}] ✗ Failed (task {task_id}): {exc}")
            return json.dumps({"task_id": task_id, "status": "failed", "error": str(exc)})

    elif name == "list_tasks":
        payload = {
            "tasks": [
                {
                    "task_id": tid,
                    "status": t["status"],
                    "agent": t["agent"],
                    "task": t["task"][:80] + ("..." if len(t["task"]) > 80 else ""),
                    "created_at": t["created_at"],
                }
                for tid, t in tasks.items()
            ],
            "summary": {
                "total": len(tasks),
                "completed": sum(1 for t in tasks.values() if t["status"] == "completed"),
                "failed": sum(1 for t in tasks.values() if t["status"] == "failed"),
                "running": sum(1 for t in tasks.values() if t["status"] == "running"),
            },
        }
        return json.dumps(payload, ensure_ascii=False)

    return json.dumps({"error": f"Unknown tool: {name}"})


def run_manager(user_instruction: str, conversation_history: list) -> str:
    """
    Send an instruction to the Manager Agent and get a response.
    Updates conversation_history in place for multi-turn context.
    Returns the final text response.
    """
    conversation_history.append({"role": "user", "content": user_instruction})

    while True:
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=8192,
            thinking={"type": "adaptive"},
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    # Cache the system prompt — it never changes across turns
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tools=TOOLS,
            messages=conversation_history,
        )

        if response.stop_reason == "end_turn":
            conversation_history.append({"role": "assistant", "content": response.content})
            text = "\n".join(b.text for b in response.content if b.type == "text")
            return text

        elif response.stop_reason == "tool_use":
            conversation_history.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"\n  [Manager] → Tool: {block.name}")
                    result_str = _execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_str,
                    })

            conversation_history.append({"role": "user", "content": tool_results})

        else:
            # pause_turn or unexpected — append and return what we have
            conversation_history.append({"role": "assistant", "content": response.content})
            text = "\n".join(b.text for b in response.content if b.type == "text")
            return text or "Task completed."
