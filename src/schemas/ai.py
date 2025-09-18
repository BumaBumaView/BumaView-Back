from pydantic import BaseModel


class ChatCompletionResponse(BaseModel):
  message_id: str
  mode: str
  answer: str
  metadata: dict
  created_at: int
