PentAI – Terminal TUI AI helper for pentesting
================================================

Files:
- pentai.py          Main TUI script
- requirements.txt   Python dependencies
- zsh_snippets.sh    Optional zsh helpers

Quick start:
1. Install dependencies:
   python3 -m pip install --user -r requirements.txt

2. Export your API key in ~/.zshrc or ~/.bashrc:
   export AI_API_KEY="your_real_key_here"

3. Make pentai.py executable and put it on your PATH:
   chmod +x pentai.py
   # e.g. move it to ~/bin or add this directory to PATH

4. Run:
   ./pentai.py --mode cmd

5. Optional: source zsh_snippets.sh from your ~/.zshrc for helpers
   source /path/to/zsh_snippets.sh
