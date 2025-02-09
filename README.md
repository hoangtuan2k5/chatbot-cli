# CLI Chatbot

A powerful command-line interface chatbot application using the Groq API.

## Author
Hoàng Chiều Nguyễn Tuấn

## Features

- 🤖 Multiple AI personas (use with role# prefix):
  - Role 1 (Programming Expert): Advanced code assistance and software development guidance
  - Role 2 (Academic Expert): In-depth knowledge across multiple disciplines
  - Role 3 (General Assistant): Versatile help for various tasks
  - Role 4 (Special Assistant): Personalized interaction mode
  - Role 5 (CLI Assistant): Execute and explain system commands with natural language support
    • Default role for inline mode
    • Shows current directory in prompt
    • Understands commands in multiple languages
- 💬 Flexible chat modes:
  - Interactive chat with multiline support and rich formatting
  - Quick inline chat for single queries
  - File input mode with safety checks (1MB limit, binary file detection)
- 📋 Smart copy functionalities:
  - Copy full responses with `cp`
  - Copy specific code blocks with language info using `c-1`, `c-2`
  - Combine copy commands: `cp c-1 c-2`
  - Clipboard operation error handling
- 🛡️ Enhanced safety features:
  - Secure API key handling
  - File size limits and binary file detection
  - Request timeout protection (30s)
  - Specific error messages for better troubleshooting
- ⌨️ Intuitive keyboard shortcuts:
  - `Enter` - Send message
  - `Ctrl+J` - New line in message
  - `Ctrl+C` - Exit application
- 🎨 Rich text formatting with Markdown support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hoangtuan2k5/chatbot-cli.git
cd chatbot-cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API key:
   - Create a `.env` file in the root directory
   - Add your Groq API key: `GROQ_API_KEY=your_api_key_here`
   - Get your API key at [Groq Console](https://console.groq.com/keys)
   > ⚠️ Never commit your .env file or share your API key

## Command Line Setup (Optional)

### Windows (CMD)
```cmd
# Add to your autorun batch file
doskey chat=python C:\path\to\chatbot-cli\main.py $*
```

### Windows (PowerShell)
```powershell
# Add to your PowerShell profile ($PROFILE)
Function chat {
    param(
        [string]$message,
        [string]$file
    )

    # Parse arguments
    if ($args.Count -gt 0) {
        # Check if first arg is -f/--file
        if ($args[0] -eq "-f" -or $args[0] -eq "--file") {
            if ($args.Count -gt 2) {
                # File with message: chat -f file.py "message"
                $file = $args[1]
                $message = $args[2]
            } elseif ($args.Count -gt 1) {
                # File only: chat -f file.py
                $file = $args[1]
            }
        } else {
            # Message only: chat "message"
            $message = $args[0]
        }
    }

    # Build command
    if ($file -and $message) {
        & python C:\path\to\chatbot-cli\main.py --file $file $message
    } elseif ($file) {
        & python C:\path\to\chatbot-cli\main.py --file $file
    } elseif ($message) {
        & python C:\path\to\chatbot-cli\main.py $message
    } else {
        & python C:\path\to\chatbot-cli\main.py
    }
}
```

### Linux/Mac (Bash/Zsh)
```bash
# Add to ~/.bashrc or ~/.zshrc
chat() {
    local file=""
    local message=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -f|--file)
                if [[ -n "$2" ]]; then
                    file="$2"
                    shift 2
                else
                    echo "Error: File path required"
                    return 1
                fi
                ;;
            *)
                message="$1"
                shift
                ;;
        esac
    done

    # Build command
    if [[ -n "$file" && -n "$message" ]]; then
        python /path/to/chatbot-cli/main.py --file "$file" "$message"
    elif [[ -n "$file" ]]; then
        python /path/to/chatbot-cli/main.py --file "$file"
    elif [[ -n "$message" ]]; then
        python /path/to/chatbot-cli/main.py "$message"
    else
        python /path/to/chatbot-cli/main.py
    fi
}
```

## Usage
### Interactive Mode
```bash
# Using chat alias (recommended):
chat

# Using python directly:
python main.py
```

### Single Query Mode
You can use different roles by adding the role number prefix:
```bash
# Using chat alias (recommended):
chat "hiển thị danh sách file"              # Default role (5: CLI Assistant)
chat "1#explain this code"                  # Role 1: Programming Expert
chat "2#explain this concept"               # Role 2: Academic Expert
chat "5#show system info"                   # Role 5: CLI Assistant

# Using python directly:
python main.py "hiển thị danh sách file"    # Default role
python main.py "1#explain this code"        # Role 1: Programming Expert
python main.py "2#explain this concept"     # Role 2: Academic Expert
python main.py "5#show system info"         # Role 5: CLI Assistant
```

### File Input Mode
```bash
# Using chat alias (recommended):
chat -f path/to/file.py                     # Interactive mode with file
chat -f path/to/file.py "explain this"      # Default role with file
chat -f path/to/file.py "1#explain this"    # Role 1 with file

# Using python directly:
python main.py --file path/to/file.py                    # Interactive mode
python main.py --file path/to/file.py "explain this"     # Default role
python main.py --file path/to/file.py "1#explain this"   # Role 1
```
```
> Note: Files are limited to 1MB and must be text-based. Binary files will be rejected.

### Inline Copy Mode
```bash
# Copy with default role
python main.py "your question here | cp c-1 c-2"

# Copy with specific role
python main.py "1#your question here | cp c-1 c-2"
```

### Command Execution

1. Direct Command Mode (executed immediately):
```bash
# Using chat alias (recommended):
chat "!dir"                # Windows: executes immediately
chat "!ls"                 # Unix: executes immediately
chat "!python --version"   # Any system command

# Using python directly:
python main.py "!dir"
python main.py "!ls"
python main.py "!python --version"

# Interactive mode (both methods):
You: !dir                  # Windows: executes immediately
You: !ls                   # Unix: executes immediately
You: !python --version
```

2. Natural Language Mode (requires confirmation):
```bash
# Using chat alias (recommended):
chat "show me the files here"               # Suggests 'dir' or 'ls'
chat "what's my current directory"          # Suggests 'pwd' or 'cd'
chat "hiển thị danh sách file"             # Multi-language support

# Using python directly:
python main.py "show me the files here"
python main.py "what's my current directory"
python main.py "hiển thị danh sách file"

# Interactive mode (both methods):
You: show me the files in this directory
Bot: Do you want to execute 'dir'? (Y/N):
You: hiển thị danh sách file
Bot: Do you want to execute 'dir'? (Y/N):
```

Command Behavior:
- Commands with ! prefix: Execute immediately
- Natural language commands: Ask for confirmation (Y/N)
- Both types adapt to your operating system automatically

## Commands

### Chat Commands
- `exit` - Exit the application
- `cp` - Copy full response
- `c-1`, `c-2`, etc. - Copy specific code blocks
- Combined commands: `cp c-1 c-2`

### System Commands (New!)
Two ways to execute commands:

1. Direct Execution (prefix with !):
   - Commands are executed immediately without confirmation
   - Directory navigation updates prompt immediately
   - Examples:
     ```bash
     # File and System commands
     !dir                 # List files (Windows)
     !ls                  # List files (Unix)
     !python --version    # Show Python version
     !help               # Show all available commands

     # Directory Navigation
     !cd /path/to/dir     # Change to specific directory
     !cd                  # Go to home directory
     !cd ..              # Go up one directory
     
     # The prompt updates with each cd command:
     /current/path> !cd /new/path
     /new/path> _
     ```

2. Natural Language:
   - Commands are suggested and require confirmation
   - Examples:
     ```bash
     "hiển thị danh sách file"  -> Suggests 'dir' or 'ls'
     "xóa màn hình"            -> Suggests 'cls' or 'clear'
     "thông tin hệ thống"      -> Suggests 'systeminfo' or 'uname -a'
     ```

Features:
- Auto-detects operating system
- 30-second timeout protection
- Platform-specific command handling
- Secure command execution

## Error Handling

The application provides specific error messages for common issues:
- API errors (invalid key, rate limits, timeouts)
- File operations (not found, permissions, size limits)
- Clipboard operations
- Network connectivity issues
- Command execution errors

## Project Structure
```
chatbot-cli/
├── src/
│   ├── chatbot.py    # Core chatbot functionality
│   ├── config.py     # Configuration settings
│   ├── display.py    # Display and UI functions
│   └── utils.py      # Utility functions
├── requirements.txt  # Project dependencies
├── .env             # Environment variables (create this)
└── main.py         # Application entry point
```

## License
MIT License

---
Created with ❤️ by Hoàng Chiều Nguyễn Tuấn