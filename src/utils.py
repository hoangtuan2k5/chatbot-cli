import pyperclip
import re
import subprocess
import platform
import shlex
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def confirm_execution(command: str) -> bool:
    """Ask for confirmation before executing a command."""
    confirmation = prompt(
        f"\nDo you want to execute this command: '{command}'? (Y/N): ",
        completer=WordCompleter(['Y', 'N'])
    ).strip().upper()
    return confirmation == 'Y'

def copy_content(text: str, command: str) -> str:
    """Copy content based on command with improved error handling and feedback."""
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
                code_blocks = extract_code_blocks(text)
                if 0 <= index < len(code_blocks):
                    lang, code = code_blocks[index]
                    copied_content.append(code)
                    result.append(f"✓ Code block #{index + 1} copied ({lang})")
                else:
                    result.append(f"❌ Code block #{index + 1} not found (total blocks: {len(code_blocks)})")
            except ValueError:
                result.append(f"❌ Invalid block number in command: {cmd}")
            except Exception as e:
                result.append(f"❌ Error processing command {cmd}: {str(e)}")
        else:
            result.append(f"❌ Unknown command: {cmd}")

    if copied_content:
        try:
            content = "\n\n".join(copied_content)
            pyperclip.copy(content)
        except Exception as e:
            result.append(f"❌ Error copying to clipboard: {str(e)}")

    return "\n".join(result)

def extract_code_blocks(text: str) -> list:
    """Extract code blocks from markdown text, preserving language info."""
    blocks = []
    matches = re.finditer(r"```(\w*)\n(.*?)```", text, re.DOTALL)
    for match in matches:
        lang = match.group(1) or "text"
        code = match.group(2).rstrip()
        blocks.append((lang, code))
    return blocks

def get_help_text(os_type: str) -> str:
    """Get OS-specific help text."""
    os_commands = {
        'windows': {
            'file_list': 'dir',
            'file_content': 'type',
            'pwd': 'cd',
            'sysinfo': 'systeminfo',
            'memory': 'wmic memorychip get',
            'disk': 'wmic logicaldisk get size,freespace,caption',
            'clear': 'cls'
        },
        'linux': {
            'file_list': 'ls',
            'file_content': 'cat',
            'pwd': 'pwd',
            'sysinfo': 'uname -a',
            'memory': 'free -h',
            'disk': 'df -h',
            'clear': 'clear'
        },
        'darwin': {
            'file_list': 'ls',
            'file_content': 'cat',
            'pwd': 'pwd',
            'sysinfo': 'uname -a',
            'memory': 'vm_stat',
            'disk': 'df -h',
            'clear': 'clear'
        }
    }

    commands = os_commands.get(os_type, os_commands['linux'])

    return f"""Available Commands (current OS: {os_type}):

1. File Operations:
   - {commands['file_list']}                 - List files in directory
   - {commands['file_content']} file.txt      - Show file contents
   - {commands['pwd']}                 - Show current directory

2. System Information:
   - {commands['sysinfo']}          - Show system information
   - python --version   - Show Python version
   - {commands['memory']}           - Show memory information
   - {commands['disk']}             - Show disk space

3. Screen Control:
   - {commands['clear']}                 - Clear screen

You can request these commands in any language, examples:
- "hiển thị danh sách file"
- "xóa màn hình"
- "thông tin hệ thống"
- "kiểm tra bộ nhớ"

Note: All commands require confirmation (Y/N) and have a 30-second timeout."""

def execute_command(command: str) -> tuple[str, bool]:
    """
    Execute a system command safely with OS-specific handling.
    Returns a tuple of (output/error message, success boolean)
    """
    # Get system info
    os_type = platform.system().lower()
    
    try:
        # Validate command
        if not command.strip():
            return ("Error: Empty command", False)

        # Handle help command
        if command.lower().strip() == "help":
            return (get_help_text(os_type), True)

        # Handle OS-specific command preparation
        if os_type == "windows":
            # Use cmd.exe for Windows
            shell_cmd = ["cmd", "/c", command]
        else:
            # Use sh for Unix-like systems
            shell_cmd = shlex.split(command)

        # Execute command with timeout
        result = subprocess.run(
            shell_cmd,
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
            shell=False  # More secure
        )

        # Handle command output
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                return (f"✓ Command executed successfully ({os_type}):\n{output}", True)
            return (f"✓ Command executed successfully ({os_type})", True)
        else:
            return (f"❌ Command failed:\n{result.stderr.strip()}", False)

    except subprocess.TimeoutExpired:
        return ("❌ Command timed out after 30 seconds", False)
    except subprocess.SubprocessError as e:
        return (f"❌ Error executing command: {str(e)}", False)
    except Exception as e:
        return (f"❌ Unexpected error: {str(e)}", False)
