import sys
import argparse
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

from src.chatbot import Chatbot
from src.config import ROLES
from src.display import (
    select_role,
    select_role_inline,
    show_instructions,
    display_markdown,
)
from src.utils import copy_content


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

        system_role = select_role_inline(ROLES)
        chatbot = Chatbot(system_role)

        # Handle file mode
        if args.file:
            message = chatbot.process_file_input(message, args.file)

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

    @kb.add("enter")  # Add Enter binding to send message
    def _(event):
        """Send message on Enter"""
        b = event.current_buffer
        if b.text.strip():
            b.validate_and_handle()

    @kb.add("c-l")  # Changed to Ctrl+J for new line
    def _(event):
        """Add newline on Ctrl+J"""
        event.current_buffer.newline()

    session = PromptSession()

    while True:
        try:
            user_input = session.prompt(
                "You: ",
                multiline=True,
                key_bindings=kb,
                prompt_continuation="... ",
                enable_suspend=True,
                complete_while_typing=False,
                input_processors=[],
                accept_default=False,  # Keep this False
                validate_while_typing=False,
            )

            if user_input.strip().lower() == "exit":
                break

            # Handle copy command
            if user_input.strip().lower() in [
                "cp"
            ] or user_input.strip().lower().startswith("c-"):
                if last_response:
                    result = copy_content(last_response, user_input.strip().lower())
                    print(result)
                    continue
                else:
                    print("❌ No previous response to copy")
                    continue

            if user_input.strip():
                print("\nAssistant:", flush=True)
                response_text = chatbot.get_response(user_input)
                last_response = response_text  # Store last response for copy command
                display_markdown(response_text)
                print()

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()
