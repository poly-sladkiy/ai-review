import re
from typing import Literal, Annotated

from pydantic import BaseModel, Field, BeforeValidator


def remove_think_section(content: str) -> str:
    pattern = r"<think>.*?</think>"
    cleaned_text = re.sub(pattern, "", content, flags=re.DOTALL)
    return cleaned_text


class OllamaMessageSchema(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: Annotated[str, BeforeValidator(remove_think_section)]


class OllamaOptionsSchema(BaseModel):
    stop: list[str] | None = None
    seed: int | None = None
    top_p: float | None = Field(default=None, ge=0.0, le=1.0)
    num_ctx: int | None = Field(default=None, ge=1)
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    num_predict: int | None = Field(default=None, ge=1)
    repeat_penalty: float | None = Field(default=None, ge=0.0)


class OllamaChatRequestSchema(BaseModel):
    model: str
    stream: bool = False
    options: OllamaOptionsSchema | None = None
    messages: list[OllamaMessageSchema]


class OllamaUsageSchema(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

    @property
    def total_tokens(self) -> int | None:
        if (self.prompt_tokens is not None) and (self.completion_tokens is not None):
            return self.prompt_tokens + self.completion_tokens

        return None


class OllamaChatResponseSchema(BaseModel):
    done: bool = Field(default=True)
    usage: OllamaUsageSchema | None = None
    model: str
    message: OllamaMessageSchema

    @property
    def first_text(self) -> str:
        return (self.message.content or "").strip()
