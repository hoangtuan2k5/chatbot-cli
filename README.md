# CLI Chatbot

A powerful command-line interface chatbot application using the Groq API.

## Author
Hoàng Chiều Nguyễn Tuấn

## Features

- 🤖 Multiple AI personas to choose from:
  - Programming Expert
  - Academic assistant and Learning assistant
  - General Assistant
  - Special assistant
- 💬 Multiple chat modes:
  - Interactive chat with multiline support
  - Quick inline chat for single queries
- 📋 Advanced copy functionalities:
  - Copy full responses with `cp`
  - Copy specific code blocks with `c-1`, `c-2`
  - Combine copy commands: `cp c-1 c-2`
- 🎨 Rich text formatting with Markdown support
- ⌨️ Keyboard shortcuts:
  - `Enter` - Send message
  - `Ctrl+L` - New line
  - `Ctrl+C` - Exit application

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
   - Add your Groq API key: `GROQ_API_KEY=your_api_key_here` (You can create a free API key by visiting: [Groq API Keys](https://console.groq.com/keys))

4. Set up PATH and alias (Optional):

### Windows (CMD)
```cmd
# Add to your autorun batch file
doskey chat=python C:\path\to\chatbot-cli\main.py $*
```
Then use the ```chat``` command to run the application.

### Windows (PowerShell)
```powershell
# Add to your PowerShell profile
Function chat {
  if ($args) {
    & python C:/Users/hoang/OneDrive/chatbot_cli/main.py --content $args
  } else {
    & python C:/Users/hoang/OneDrive/chatbot_cli/main.py --content ""
  }
}
```
Then use the ```chat``` command to run the application.

### Linux/Mac (Bash)
```bash
# Add to ~/.bashrc or ~/.zshrc
chat() { 
  python /path/to/chatbot-cli/main.py "$@"; 
}
```
Then use the ```chat``` command to run the application.

## Usage

### Interactive Mode
```bash
python main.py
```

### Single Query Mode
```bash
python main.py "your question here"
```

### File Input Mode
> **Note:** Used for models that support files, see at [Groq Vision Documentation](https://console.groq.com/docs/vision).
```bash
python main.py --file path/to/file.py "explain this code"
```

### Inline Copy Mode
```bash
python main.py "your question here | cp c-1 c-2"
```

## Commands
- `exit` - Exit the application
- `cp` - Copy full response
- `c-1`, `c-2`, etc. - Copy specific code blocks
- Combined commands: `cp c-1 c-2`

## Project Structure
```
chatbot-cli/
├── src/
│   ├── chatbot.py    # Core chatbot functionality
│   ├── config.py     # Configuration settings
│   ├── display.py    # Display and UI functions
│   └── utils.py      # Utility functions
├── requirements.txt  # Project dependencies
├── .env             # Environment variables
└── main.py         # Application entry point
```

## License
MIT License

---
Created with ❤️ by Hoàng Chiều Nguyễn Tuấn