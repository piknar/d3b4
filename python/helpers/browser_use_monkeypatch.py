from typing import Any
from python.helpers import dirty_json

# browser_use is optional - not installed in d3b4 (no browser support)
try:
    from browser_use.llm import ChatGoogle
    _BROWSER_USE_AVAILABLE = True
except ImportError:
    _BROWSER_USE_AVAILABLE = False
    ChatGoogle = None


def gemini_clean_and_conform(text: str):
    obj = None
    try:
        obj = dirty_json.parse(text)
    except Exception:
        return None

    if not isinstance(obj, dict):
        return None

    if isinstance(obj.get("action"), list):
        normalized_actions = []
        for item in obj["action"]:
            if not isinstance(item, dict):
                continue
            action_key, action_value = next(iter(item.items()), (None, None))
            if not action_key:
                continue
            if action_key == "complete_task":
                action_key = "done"
            v = (action_value or {}).copy()
            if action_key in ("scroll_down", "scroll_up", "scroll"):
                is_down = action_key != "scroll_up"
                v.setdefault("down", is_down)
                v.setdefault("num_pages", 1.0)
                normalized_actions.append({"scroll": v})
            elif action_key == "go_to_url":
                v.setdefault("new_tab", False)
                normalized_actions.append({action_key: v})
            elif action_key == "done":
                if "data" not in v:
                    response_text = v.pop("response", None)
                    summary_text = v.pop("page_summary", None)
                    title_text = v.pop("title", "Task Completed")
                    final_response = response_text or "Task completed successfully."
                    final_summary = summary_text or "No page summary available."
                    v["data"] = {"title": title_text, "response": final_response, "page_summary": final_summary}
                v.setdefault("success", True)
                normalized_actions.append({action_key: v})
            else:
                normalized_actions.append(item)
        obj["action"] = normalized_actions

    return dirty_json.stringify(obj)


def _patched_fix_gemini_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
    if '$defs' in schema:
        defs = schema.pop('$defs')
        def resolve_refs(obj: Any) -> Any:
            if isinstance(obj, dict):
                if '$ref' in obj:
                    ref = obj.pop('$ref')
                    ref_name = ref.split('/')[-1]
                    if ref_name in defs:
                        resolved = defs[ref_name].copy()
                        for key, value in obj.items():
                            if key != '$ref':
                                resolved[key] = value
                        return resolve_refs(resolved)
                    return obj
                else:
                    return {k: resolve_refs(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [resolve_refs(item) for item in obj]
            return obj
        schema = resolve_refs(schema)

    def clean_schema(obj: Any) -> Any:
        if isinstance(obj, dict):
            cleaned = {}
            for key, value in obj.items():
                if key not in ['additionalProperties', 'title', 'default']:
                    cleaned_value = clean_schema(value)
                    if (key == 'properties' and isinstance(cleaned_value, dict)
                            and len(cleaned_value) == 0
                            and isinstance(obj.get('type', ''), str)
                            and obj.get('type', '').upper() == 'OBJECT'):
                        cleaned['properties'] = {'_placeholder': {'type': 'string'}}
                    else:
                        cleaned[key] = cleaned_value
            if (isinstance(cleaned.get('type', ''), str)
                    and cleaned.get('type', '').upper() == 'OBJECT'
                    and 'properties' in cleaned
                    and isinstance(cleaned['properties'], dict)
                    and len(cleaned['properties']) == 0):
                cleaned['properties'] = {'_placeholder': {'type': 'string'}}
            if 'required' in cleaned and isinstance(cleaned.get('required'), list):
                cleaned['required'] = [p for p in cleaned['required'] if p != 'title']
            return cleaned
        elif isinstance(obj, list):
            return [clean_schema(item) for item in obj]
        return obj

    return clean_schema(schema)


def apply():
    """Applies the monkey-patch to ChatGoogle (only if browser_use is available)."""
    if _BROWSER_USE_AVAILABLE and ChatGoogle is not None:
        ChatGoogle._fix_gemini_schema = _patched_fix_gemini_schema
