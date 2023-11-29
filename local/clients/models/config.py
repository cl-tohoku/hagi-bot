from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    model: str
    history_length: int | None = None
    max_tokens: int | None = None
    temperature: float = 0.0
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    timeout: float | None = None
    max_retry: int | None = 5
    logit_bias: dict = field(default_factory=dict)
