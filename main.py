#!/usr/bin/env -S uv run --env-file=.env
import os

import discord
from fastmcp import Client
from mcp.types import TextContent

mcp_client = Client("https://mcp.deepwiki.com/sse")


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {client.user}")


async def ask_deepwiki(mcp_client: Client, prompt: str) -> str:
    if not prompt:
        return ""
    async with mcp_client:
        print(f"ask_deepwiki: Prompting Deepwiki with: {prompt[:100]}...")
        result = await mcp_client.call_tool(
            name="ask_question",
            arguments={
                "repoName": "bazzite-org/docs.bazzite.gg",
                "question": prompt,
            },
        )
        print("ask_deepwiki: Received result from mcp_client.call_tool.")
        content = "\n".join(
            [x.text for x in result.content if isinstance(x, TextContent)]
        )

        return content


@tree.command(name="deepwiki", description="Ask Deepwiki about something")
async def ask_deepwiki_command(ctx: discord.Interaction, prompt: str):
    print("ask_deepwiki_command: Command received.")  # Initial print
    await ctx.response.defer()  # Defer the response immediately
    print("Calling ask_deepwiki...")
    result = await ask_deepwiki(mcp_client, prompt)
    print(f"ask_deepwiki returned: {result[:100]}...")  # Print first 100 chars
    if not result:
        await ctx.followup.send("Deepwiki did not return a response.", ephemeral=True)
    else:
        # Split result into chunks of max length 2000
        max_chunk_length = 2000
        chunks = [
            result[i : i + max_chunk_length]
            for i in range(0, len(result), max_chunk_length)
        ]

        for chunk in chunks:
            # Send each chunk as a followup message
            # For the first chunk, if it's the only one, we might want to edit the original deferred message.
            # However, the prompt implies sending multiple followups if needed.
            # Simple approach: send all as followups.
            await ctx.followup.send(chunk, ephemeral=True)


async def main():
    await client.start(os.getenv("DISCORD_BOT_TOKEN", ""))


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Error: {e}")
