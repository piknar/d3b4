from python.helpers.memory import Memory
from python.helpers.tool import Tool, Response


class MemorySave(Tool):

    async def execute(self, text="", area="", **kwargs):

        if not area:
            area = Memory.Area.MAIN.value

        metadata = {"area": area, **kwargs}

        db = await Memory.get(self.agent)
        if db is None:
            return self.tool_response("Memory is unavailable (no embedding model configured).")

        id = await db.insert_text(text, metadata)

        result = self.agent.read_prompt("fw.memory_saved.md", memory_id=id)
        return Response(message=result, break_loop=False)
