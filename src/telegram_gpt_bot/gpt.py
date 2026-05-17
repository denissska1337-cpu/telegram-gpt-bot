from openai import AsyncOpenAI


async def reply_text(
    client: AsyncOpenAI,
    model: str,
    user_message: str,
) -> str:
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_message}],
    )
    choice = response.choices[0]
    content = choice.message.content
    if not content:
        return ""
    return content.strip()
