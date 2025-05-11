import aiohttp
import asyncio
import json


async def invoke_chute():
    api_token = "KEY HERE"

    headers = {
        "Authorization": "Bearer " + api_token,
        "Content-Type": "application/json"
    }

    body = {
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "prompt": "My favourite type of cat",
        "stream": False,
        "temperature": 0.7,
        "max_tokens": 10000,
    }

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(
                "https://llm.chutes.ai/v1/completions",
                headers=headers,
                json=body,
                ssl=False
        ) as response:
            async for line in response.content:
                line = line.decode("utf-8").strip()
                print(line)
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = data.strip()
                        if chunk:
                            print(chunk)
                    except Exception as e:
                        print(f"Error parsing chunk: {e}")


policy = asyncio.WindowsSelectorEventLoopPolicy()
asyncio.set_event_loop_policy(policy)
asyncio.run(invoke_chute())