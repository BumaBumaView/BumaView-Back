import os
import requests
import json

from ..schemas.ai import ChatCompletionResponse


def generate_questions(company_name: str, category: str) -> list[str]:
  api_key = os.getenv("DIFY_INTERVIEW_QUESTION_GENERATION_API_KEY")
  endpoint = os.getenv("DIFY_ENDPOINT", "https://dify.obtuse.kr/v1/")

  arguments = {
    "company_name": company_name,
    "job_name": category
  }

  response = LLM_Generate(api_key, endpoint, arguments)
  data = ChatCompletionResponse(**response.json())
  questions = json.loads(data.answer)
  return questions


def LLM_Generate(api_key, endpoint, arguments):
  url = f"{endpoint}/completion-messages"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
  }
  body = {
      "inputs": arguments,
      "response_mode": "blocking",
      "user": "bumaview"
  }
  response = requests.post(url, json=body, headers=headers)
  response.raise_for_status()
  return response
