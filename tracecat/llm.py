from __future__ import annotations

from typing import Any, Literal

import orjson
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion, Choice
from tenacity import retry, stop_after_attempt, wait_exponential

from tracecat.config import MAX_RETRIES
from tracecat.logger import standard_logger

logger = standard_logger(__name__)


ModelType = Literal[
    "gpt-4-turbo-preview",
    "gpt-4-0125-preview",
    "gpt-4-vision-preview",
    "gpt-3.5-turbo-0125",
]
DEFAULT_MODEL_TYPE: ModelType = "gpt-3.5-turbo-0125"
DEFAULT_SYSTEM_CONTEXT = (
    "You are an expert decision maker."
    " You follow instructions and make the best decision."
)


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
async def async_openai_call(  # type: ignore
    prompt: str,
    model: ModelType = DEFAULT_MODEL_TYPE,
    temperature: float = 0.2,
    system_context: str = DEFAULT_SYSTEM_CONTEXT,
    response_format: Literal["json_object", "text"] = "text",
    stream: bool = False,
    parse_json: bool = True,
    **kwargs,
):
    """Call the OpenAI API with the given prompt and return the response.

    Returns
    -------
    dict[str, Any]
        The message object from the OpenAI ChatCompletion API.
    """
    load_dotenv()
    client = AsyncOpenAI()

    def parse_choice(choice: Choice) -> str | dict[str, Any]:
        # The content will not be null, so we can safely use the `!` operator.
        content = choice.message.content
        if not content:
            logger.warning("No content in response.")
            return ""
        res = content.strip()
        if parse_json and response_format == "json_object":
            json_res: dict[str, Any] = orjson.loads(res)
            return json_res
        return res

    if response_format == "json_object":
        system_context += " Please only output valid JSON."

    messages = [
        {"role": "system", "content": system_context},
        {"role": "user", "content": prompt},
    ]

    logger.info("🧠 Calling OpenAI API with model: %s...", model)
    response: ChatCompletion = await client.chat.completions.create(  # type: ignore[call-overload]
        model=model,
        response_format={"type": response_format},
        messages=messages,
        temperature=temperature,
        stream=stream,
        **kwargs,
    )
    if stream:
        return response

    return parse_choice(response.choices[0])