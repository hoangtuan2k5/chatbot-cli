import sys
import argparse
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
import platform
import os

from src.chatbot import Chatbot
from src.config import ROLES, DEFAULT_INLINE_ROLE
from src.display import (
    select_role,
    select_role_inline,
    show_instructions,
    display_markdown,
)
from src.utils import copy_content, execute_command, confirm_execution

def process_message(message: str, current_role: str = DEFAULT_INLINE_ROLE) -> tuple[str, str]:
    """Process message to extract role and clean message. Returns (clean_message, system_role)"""
    message = message.strip()
    if "#" in message:
        parts = message.split("#", 1)
        if len(parts) == 2:
            role_num = parts[0].strip()
            if role_num in ROLES:
                return parts[1].strip(), ROLES[role_num]
    return message, ROLES[current_role]

def main():
    parser = argparse.ArgumentParser(description="CLI Chatbot")
    parser.add_argument(
        "content", nargs="?", help="Input content", default=None
    )  # Positional argument
    parser.add_argument("--file", type=str, help="Path to input file", default=None)
    parser.add_argument(
        "--content",
        dest="content_flag",
        help="Input content (alternative way)",
        default=None,
    )  # Renamed to avoid conflict
    args = parser.parse_args()

    # Use either positional content or --content flag
    content = args.content or args.content_flag

    # Inline mode (content specified)
    if content:
        # Split content into message and copy commands
        parts = content.strip().split(" | ")
        message = parts[0]
        copy_command = parts[1] if len(parts) > 1 else None

        # Process message to get role and clean message first
        message, system_role = process_message(message)
        chatbot = Chatbot(system_role)

        # Handle file mode
        if args.file:
            file_content = chatbot.process_file_input("", args.file)
            message = f"{message}\n\n{file_content}" if message else file_content

        if not args.file and message.startswith("!"):
            # Handle direct command execution
            cmd = message[1:].strip()
            if cmd.lower() == "help":
                result, _ = execute_command("help")
            else:
                result, success = execute_command(cmd)
                if not success:
                    print("\nTry '!help' for command examples")
            print(result)
            return

        # Normal message handling
        response_text = chatbot.get_response(message)
        display_markdown(response_text)

        # Process copy command if present
        if copy_command:
            result = copy_content(response_text, copy_command)
            print(result)
        return

    # Interactive chat mode
    system_role = select_role(ROLES)  # This one clears screen
    chatbot = Chatbot(system_role)
    show_instructions()

    kb = KeyBindings()
    last_response = ""  # Store last response for copy command

    @kb.add("enter")
    def _(event):
        """Send message on Enter"""
        b = event.current_buffer
        if b.text.strip():
            b.validate_and_handle()

    @kb.add("c-j")
    def _(event):
        """Add newline on Ctrl+J"""
        event.current_buffer.newline()

    session = PromptSession()

    while True:
        try:
            # Use current directory as prompt for CLI Assistant role
            prompt_text = f"{os.getcwd()}> " if system_role == ROLES[DEFAULT_INLINE_ROLE] else "You: "
            user_input = session.prompt(
                prompt_text,
                multiline=True,
                key_bindings=kb,
                prompt_continuation="    ",
                enable_suspend=True,
                complete_while_typing=False,
                input_processors=[],
                accept_default=False,
                validate_while_typing=False,
            )

            user_input = user_input.strip()
            if user_input.lower() == "exit":
                break

            # Handle copy command
            if user_input.lower() in ["cp"] or user_input.lower().startswith("c-"):
                if last_response:
                    result = copy_content(last_response, user_input.lower())
                    print(result)
                    continue
                else:
                    print("❌ No previous response to copy")
                    continue

            # Process message to get role and clean message
            clean_message, new_role = process_message(user_input)
            if new_role != system_role:
                system_role = new_role
                chatbot = Chatbot(system_role)
                user_input = clean_message

            # Handle direct commands
            if user_input.startswith("!"):
                cmd = user_input[1:].strip()
                if cmd.lower() == "help":
                    result, _ = execute_command("help")
                else:
                    result, success = execute_command(cmd)
                    if not success:
                        print("\nTry '!help' for command examples")
                print(result)
                continue

            # Normal message handling
            if user_input:
                print("\nAssistant:", flush=True)
                response_text = chatbot.get_response(user_input)
                last_response = response_text
                display_markdown(response_text)
                print()

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

if __name__ == "__main__":
    main()
