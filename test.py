from fastmcp import Client
from mcp.types import TextContent

client = Client("https://mcp.deepwiki.com/sse")


question = "What is bazzite?"


async def main():
    async with client:
        tools = await client.list_tools()
        tools_names = [t.name for t in tools]
        print("Tools available: ", tools_names)

        if "ask_question" in tools_names:
            print("found tool ask_question")
            print("calling tool ask_question...")

            result = await client.call_tool(
                "ask_question",
                {
                    "repoName": "bazzite-org/docs.bazzite.gg",
                    "question": "Answer the following question with less than 2000 characters in length: "
                    + question,
                },
            )
            content = "\n".join(
                [x.text for x in result.content if isinstance(x, TextContent)]
            )
            print(content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
