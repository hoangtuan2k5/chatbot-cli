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
        # Split content into role, message and copy commands
        parts = content.strip().split(" | ")
        message = parts[0]
        copy_command = parts[1] if len(parts) > 1 else None

        # Check for role prefix (e.g., "1#show me code")
        if "#" in message:
            role_num, message = message.split("#", 1)
            if role_num in ROLES:
                system_role = ROLES[role_num]
            else:
                system_role = ROLES[DEFAULT_INLINE_ROLE]
        else:
            system_role = ROLES[DEFAULT_INLINE_ROLE]

        chatbot = Chatbot(system_role)

        # Handle file mode
        if args.file:
            message = chatbot.process_file_input(message, args.file)

        # Detect and handle command execution
        if message.startswith("!"):
            cmd = message[1:].strip()
            if cmd.lower() == "help":
                result, _ = execute_command("help")
                print(result)
                return
            result, success = execute_command(cmd)
            print(result)
            if not success:
                print("\nTry '!help' for command examples")
            return

        # Handle natural language command
        response_text = chatbot.get_response(f"If this text describes a command to execute, suggest the appropriate command for {platform.system().lower()} OS. If not, respond normally: {message}")
        
        # Check if response contains a command suggestion
        if "COMMAND:" in response_text:
            cmd = response_text.split("COMMAND:")[1].split("\n")[0].strip()
            if cmd:
                # Remove any OS-specific comments in parentheses
                cmd = cmd.split("(")[0].strip()
                if confirm_execution(cmd):
                    result, success = execute_command(cmd)
                    print(result)
                    if not success:
                        print("\nTry '!help' for command examples")
                return

        # Normal chatbot response
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

    @kb.add("c-j")  # Use Ctrl+J for new line
    def _(event):
        """Add newline on Ctrl+J (more intuitive than Ctrl+L)"""
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
                accept_default=False,  # Keep this False
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

            # Handle system command execution
            if user_input.startswith("!"):
                # Direct command execution
                cmd = user_input[1:].strip()
                if cmd.lower() == "help":
                    result, _ = execute_command("help")
                else:
                    result, success = execute_command(cmd)
                    if not success:
                        print("\nTry '!help' for command examples")
                print(result)
                continue

            if user_input:
                # Handle natural language command request
                response_text = chatbot.get_response(f"If this text describes a command to execute, suggest the appropriate command for {platform.system().lower()} OS. If not, respond normally: {user_input}")
                
                # Check if response contains a command suggestion
                if "COMMAND:" in response_text:
                    cmd = response_text.split("COMMAND:")[1].split("\n")[0].strip()
                    if cmd:
                        # Remove any OS-specific comments in parentheses
                        cmd = cmd.split("(")[0].strip()
                        if confirm_execution(cmd):
                            result, success = execute_command(cmd)
                            print(result)
                            if not success:
                                print("\nTry '!help' for command examples")
                        continue

                # Normal chatbot response
                print("\nAssistant:", flush=True)
                last_response = response_text  # Store last response for copy command
                display_markdown(response_text)
                print()

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()
