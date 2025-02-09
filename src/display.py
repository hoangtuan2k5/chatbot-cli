import os
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print as rprint

console = Console()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def select_role(roles: dict) -> str:
    clear_screen()
    console.print("Select a role:", style="bold blue")
    for key, role in roles.items():
        console.print(f"[yellow]{key}[/yellow]: {role[:100]}...")

    while True:
        choice = Prompt.ask("Enter role number", choices=list(roles.keys()))
        if choice in roles:
            return roles[choice]


def select_role_inline(roles: dict) -> str:
    """Version of select_role that doesn't clear screen - for inline mode"""
    console.print("Select a role:", style="bold blue")
    for key, role in roles.items():
        console.print(f"[yellow]{key}[/yellow]: {role[:100]}...")

    while True:
        choice = Prompt.ask("Enter role number", choices=list(roles.keys()))
        if choice in roles:
            return roles[choice]


def show_instructions():
    instructions = """
    Instructions:
    Basic Commands:
    - Type 'exit' to quit the application
    - Press Enter to send message
    - Press Ctrl+J to insert a new line in message

    Copy Commands:
    - 'cp' - Copy the entire response
    - 'c-1', 'c-2', etc. - Copy specific code blocks
    - Combine commands: 'cp c-1 c-2'

    System Commands:
    1. Direct commands (start with '!'):
       - !help - Show command examples
       - !dir (Windows) or !ls (Unix) - List files
       - !python --version - Show Python version

    2. Natural language commands (New!):
       Ask in any language, for example:
       - "show me all files"
       - "hiển thị các file"
       - "xóa màn hình"
       - "thông tin hệ thống"
       - "limpia la pantalla"
    
    Note:
    - All commands require confirmation (Y/N)
    - 30-second timeout for safety
    - OS-specific command handling
    """
    rprint(Panel(instructions, title="How to use", border_style="blue"))


def display_markdown(text: str):
    try:
        md = Markdown(text)
        console.print(md)
    except Exception as e:
        print(f"\nError rendering markdown: {str(e)}")
        print(text)  # Fallback to plain text
