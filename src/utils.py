import pyperclip
import re


def copy_content(text: str, command: str) -> str:
    commands = command.strip().lower().split()
    result = []
    copied_content = []

    for cmd in commands:
        if cmd == "cp":
            copied_content.append(text)
            result.append("✓ Full response copied")

        elif cmd.startswith("c-"):
            try:
                index = int(cmd.split("-")[1]) - 1
                code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
                if 0 <= index < len(code_blocks):
                    copied_content.append(code_blocks[index])
                    result.append(f"✓ Code block #{index + 1} copied")
                else:
                    result.append(f"❌ Code block #{index + 1} not found")
            except:
                result.append(f"❌ Invalid command: {cmd}")
        else:
            result.append(f"❌ Invalid command: {cmd}")

    if copied_content:
        # Join all copied content with newlines between them
        pyperclip.copy("\n\n".join(copied_content))

    return "\n".join(result)
