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
            "stream": False,  # Streaming disabled by default
            "messages": self.messages,
        }

    def process_file_input(self, content: str, file_path: str) -> str:
        if not file_path:
            return content

        try:
            # Read file in chunks to handle large files safely
            with open(file_path, "r", encoding="utf-8") as f:
                chunks = []
                while chunk := f.read(8192):  # 8KB chunks
                    chunks.append(chunk)
                    if len("".join(chunks)) > 1_000_000:  # 1MB limit
                        raise ValueError("File too large (max 1MB)")
                file_content = "".join(chunks)
                
            file_ext = file_path.split(".")[-1].lower()
            return f"{content}\n```{file_ext}\n{file_content}\n```"
            
        except UnicodeDecodeError:
            return f"{content}\n(Error: File appears to be binary)"
        except FileNotFoundError:
            return f"{content}\n(Error: File not found: {file_path})"
        except PermissionError:
            return f"{content}\n(Error: Permission denied accessing {file_path})"
        except ValueError as e:
            return f"{content}\n(Error: {str(e)})"
        except Exception as e:
            return f"{content}\n(Error reading file: {str(e)})"

    def get_cli_response(self, content: str, os_type: str) -> str:
        """Special method for CLI Assistant role that checks for commands"""
        # Check if the content appears to be asking for a command
        command_indicators = [
            "how to", "làm sao", "làm thế nào",  # How to indicators
            "show", "hiển thị", "xem",  # Show/display indicators
            "list", "liệt kê",  # List indicators
            "delete", "xóa",  # Delete indicators
            "create", "tạo",  # Create indicators
            "move", "di chuyển",  # Move indicators
            "copy", "sao chép",  # Copy indicators
            "run", "chạy",  # Run indicators
            "start", "bắt đầu",  # Start indicators
            "stop", "dừng",  # Stop indicators
            "restart", "khởi động lại",  # Restart indicators
            "find", "tìm",  # Find indicators
            "change", "thay đổi",  # Change indicators
            "update", "cập nhật",  # Update indicators
            "install", "cài đặt",  # Install indicators
            "remove", "gỡ bỏ",  # Remove indicators
            "clear", "xóa",  # Clear indicators
            "check", "kiểm tra",  # Check indicators
            "open", "mở"  # Open indicators
        ]
        
        is_command_like = any(indicator.lower() in content.lower() for indicator in command_indicators)
        
        if is_command_like:
            modified_content = f"If this text describes a command to execute, suggest the appropriate command for {os_type} OS. If not, respond normally: {content}"
        else:
            # If it doesn't look like a command request, just use the content as is
            modified_content = content
            
        return self.get_response(modified_content)

    def get_response(self, content: str) -> str:
        """Get a normal response without command checking"""
        try:
            payload = self._prepare_payload(content)
            
            # Make request with timeout
            response = requests.post(
                config.API_URL,
                headers=self.headers,
                json=payload,
                timeout=30  # 30 second timeout
            )
            response.raise_for_status()

            response_content = response.json()["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": response_content})
            return response_content

        except requests.Timeout:
            error_msg = "\nError: Request timed out. Please try again."
        except requests.ConnectionError:
            error_msg = "\nError: Connection failed. Please check your internet connection."
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                error_msg = "\nError: Invalid API key"
            elif e.response.status_code == 429:
                error_msg = "\nError: Rate limit exceeded. Please try again later."
            else:
                error_msg = f"\nError: HTTP {e.response.status_code} - {e.response.text}"
        except Exception as e:
            error_msg = f"\nError: {str(e)}"
        
        return error_msg
