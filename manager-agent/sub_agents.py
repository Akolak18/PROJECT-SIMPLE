"""
Specialized sub-agents used by the Manager Agent.
Each agent handles a specific domain of tasks.
"""
import os
import json
import anthropic


class BaseAgent:
    description = ""
    capabilities: list[str] = []

    def execute(self, task: str, context: dict) -> dict:
        raise NotImplementedError


class FileAgent(BaseAgent):
    description = "Handles file system operations: reading, writing, listing files and directories"
    capabilities = ["read_file", "write_file", "list_directory", "check_file_exists", "append_file"]

    def execute(self, task: str, context: dict) -> dict:
        task_lower = task.lower()

        if any(w in task_lower for w in ("read", "open", "show", "get content")):
            path = context.get("path") or self._extract_path(task)
            if not path:
                return {"error": "No file path specified. Provide 'path' in context."}
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return {"operation": "read", "path": path, "content": content, "size_bytes": len(content.encode())}
            except FileNotFoundError:
                return {"error": f"File not found: {path}"}
            except Exception as e:
                return {"error": str(e)}

        elif any(w in task_lower for w in ("write", "create", "save", "overwrite")):
            path = context.get("path")
            content = context.get("content", "")
            if not path:
                return {"error": "No file path specified. Provide 'path' in context."}
            try:
                parent = os.path.dirname(path)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return {"operation": "write", "path": path, "bytes_written": len(content.encode())}
            except Exception as e:
                return {"error": str(e)}

        elif "append" in task_lower:
            path = context.get("path")
            content = context.get("content", "")
            if not path:
                return {"error": "No file path specified. Provide 'path' in context."}
            try:
                with open(path, "a", encoding="utf-8") as f:
                    f.write(content)
                return {"operation": "append", "path": path, "bytes_appended": len(content.encode())}
            except Exception as e:
                return {"error": str(e)}

        elif any(w in task_lower for w in ("list", "dir", "ls", "files in")):
            directory = context.get("directory", ".")
            try:
                entries = os.listdir(directory)
                files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
                dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
                return {"operation": "list", "directory": directory, "files": files, "directories": dirs, "total": len(entries)}
            except Exception as e:
                return {"error": str(e)}

        elif any(w in task_lower for w in ("exist", "check")):
            path = context.get("path") or self._extract_path(task)
            if not path:
                return {"error": "No file path specified."}
            return {"operation": "exists", "path": path, "exists": os.path.exists(path)}

        return {"error": "Could not determine file operation. Use: read/write/append/list/exists with appropriate context."}

    def _extract_path(self, task: str) -> str | None:
        for word in task.split():
            word = word.strip("\"'(),")
            if ("/" in word or word.startswith(".") or
                    any(word.endswith(ext) for ext in (".py", ".txt", ".json", ".csv", ".md", ".yaml", ".yml"))):
                return word
        return None


class CodeAgent(BaseAgent):
    description = "Analyzes, generates, reviews, and explains code in any programming language"
    capabilities = ["analyze_code", "generate_code", "explain_code", "review_code", "fix_bugs", "refactor_code"]

    def __init__(self):
        self.client = anthropic.Anthropic()

    def execute(self, task: str, context: dict) -> dict:
        code = context.get("code", "")
        language = context.get("language", "")

        prompt = task
        if code:
            lang_hint = f"{language}\n" if language else ""
            prompt += f"\n\nCode:\n```{lang_hint}{code}\n```"

        response = self.client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=4096,
            system="You are an expert software engineer. Provide concise, practical, and correct code assistance.",
            messages=[{"role": "user", "content": prompt}],
        )

        text = next((b.text for b in response.content if b.type == "text"), "")
        return {
            "operation": "code",
            "task": task,
            "result": text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }


class SearchAgent(BaseAgent):
    description = "Searches for information (simulated — connect a real search API to extend)"
    capabilities = ["web_search", "research_topic", "find_information", "lookup_documentation"]

    def execute(self, task: str, context: dict) -> dict:
        query = context.get("query", task)
        topic = query[:80]
        return {
            "operation": "search",
            "query": query,
            "results": [
                {
                    "rank": 1,
                    "title": f"Overview: {topic}",
                    "snippet": f"Comprehensive guide covering {topic} with examples and best practices.",
                    "url": "https://docs.example.com/overview",
                },
                {
                    "rank": 2,
                    "title": f"Tutorial: Getting started with {topic}",
                    "snippet": f"Step-by-step tutorial for {topic}, from basics to advanced usage.",
                    "url": "https://tutorial.example.com/start",
                },
                {
                    "rank": 3,
                    "title": f"Stack Overflow: Common {topic} questions",
                    "snippet": f"Top-voted community answers about {topic} with practical solutions.",
                    "url": "https://stackoverflow.com/questions/tagged/" + topic.replace(" ", "-"),
                },
            ],
            "note": "Simulated results. Integrate a real API (SerpAPI, Brave Search, etc.) for live data.",
        }


class DataAgent(BaseAgent):
    description = "Processes and analyzes data: statistics, aggregations, JSON parsing, summaries"
    capabilities = ["compute_statistics", "analyze_list", "parse_json", "summarize_data", "filter_data", "aggregate"]

    def execute(self, task: str, context: dict) -> dict:
        data = context.get("data")
        if data is None:
            return {"error": "No data provided. Include 'data' key in context."}

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                pass

        task_lower = task.lower()

        if isinstance(data, list):
            numbers = [x for x in data if isinstance(x, (int, float))]

            if numbers and any(w in task_lower for w in ("stat", "analyz", "calculat", "mean", "average", "sum", "min", "max")):
                n = len(numbers)
                total = sum(numbers)
                mean = total / n
                sorted_d = sorted(numbers)
                mid = n // 2
                median = sorted_d[mid] if n % 2 == 1 else (sorted_d[mid - 1] + sorted_d[mid]) / 2
                variance = sum((x - mean) ** 2 for x in numbers) / n
                std_dev = variance ** 0.5
                return {
                    "operation": "statistics",
                    "count": n,
                    "sum": total,
                    "mean": round(mean, 4),
                    "median": median,
                    "std_dev": round(std_dev, 4),
                    "min": min(numbers),
                    "max": max(numbers),
                }

            if "filter" in task_lower:
                threshold = context.get("threshold")
                operator = context.get("operator", "gt")
                if threshold is not None and numbers:
                    ops = {"gt": lambda x: x > threshold, "lt": lambda x: x < threshold,
                           "gte": lambda x: x >= threshold, "lte": lambda x: x <= threshold}
                    fn = ops.get(operator, ops["gt"])
                    filtered = [x for x in numbers if fn(x)]
                    return {"operation": "filter", "original_count": len(numbers), "filtered_count": len(filtered), "results": filtered}

            return {
                "operation": "analyze_list",
                "item_count": len(data),
                "types": list({type(x).__name__ for x in data}),
                "sample": data[:10] if len(data) > 10 else data,
                "numeric_items": len(numbers),
            }

        elif isinstance(data, dict):
            return {
                "operation": "analyze_dict",
                "key_count": len(data),
                "keys": list(data.keys()),
                "schema": {k: type(v).__name__ for k, v in data.items()},
            }

        return {"operation": "raw", "result": str(data)[:1000]}
