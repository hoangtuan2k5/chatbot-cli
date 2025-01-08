import json
import requests
from typing import Generator, Dict
from . import config


class Chatbot:
    def __init__(self, system_role: str):
        self.messages = [{"role": "system", "content": system_role}]
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
        }

    def _prepare_payload(self, content: str) -> Dict:
        self.messages.append({"role": "user", "content": content})
        return {
            "model": config.MODEL,
            "temperature": config.TEMPERATURE,
            "max_tokens": config.MAX_TOKENS,
            "stream": True,
            "messages": self.messages,
        }

    def process_file_input(self, content: str, file_path: str) -> str:
        if not file_path:
            return content

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
                file_ext = file_path.split(".")[-1]
                return f"{content}\n```{file_ext}\n{file_content}\n```"
        except Exception as e:
            return f"{content}\n(Error reading file: {str(e)})"

    def get_response(self, content: str) -> str:
        payload = self._prepare_payload(content)
        payload["stream"] = False  # Disable Streaming

        try:
            response = requests.post(config.API_URL, headers=self.headers, json=payload)
            response.raise_for_status()

            response_content = response.json()["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": response_content})
            return response_content

        except Exception as e:
            error_msg = f"\nError: {str(e)}"
            return error_msg
