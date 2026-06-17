Project: csv-cleaner

Quick setup (Windows + VS Code, PowerShell):
1. Open folder: File → Open Folder → C:\Users\mew85240702\csv-cleaner
2. Create venv (if not already): python -m venv .venv
3. Activate venv (PowerShell): .\.venv\Scripts\Activate.ps1
   (CMD): .\.venv\Scripts\activate.bat
4. Install deps: pip install -r requirements.txt

Run the script:
  python clean_csv.py input.csv output.csv

Optional: open output automatically:
  python clean_csv.py input.csv output.csv --open-output

Run as a VS Code task (prompts for filenames):
  Terminal → Run Task → Run clean_csv

When you run the task it will prompt for input and output file paths (defaults: sample.csv, cleaned.csv). The task activates the .venv and runs the script with --open-output so the cleaned file opens after completion. You can edit .vscode/tasks.json to change defaults or behavior.

Quick CLI wrappers (use in project directory):
- PowerShell: .\run_clean.ps1 [<input.csv>] [<output.csv>] [--Open]
  Example: .\run_clean.ps1 .\sample.csv .\cleaned.csv --Open

- Batch (CMD): run_clean.bat [<input.csv>] [<output.csv>] [--open-output]
  Example: run_clean.bat sample.csv cleaned.csv --open-output

Both scripts use the project's .venv python executable. If .venv isn't created or pandas isn't installed, run:
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt

Notes:
- Default encoding: utf-8. Use --encoding when needed.
- Use --sep to specify a different CSV delimiter.
- The script treats cells containing only whitespace as empty and drops rows that are empty across all columns.
