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
    - Type 'exit' to quit the application
    - Press Enter to send message
    - Press Ctrl + L for new line
    - Type 'cp' to copy full response
    - Type 'c-1', 'c-2',... to copy specific code blocks
    - Combine multiple copy commands: 'cp c-1 c-2'
    """
    rprint(Panel(instructions, title="How to use", border_style="blue"))


def display_markdown(text: str):
    try:
        md = Markdown(text)
        console.print(md)
    except Exception as e:
        print(f"\nError rendering markdown: {str(e)}")
        print(text)  # Fallback to plain text
