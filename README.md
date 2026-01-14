# AGI Memory Moat — Prototype

Lightweight prototype workspace for the AGI Memory Moat project.

Contents
- `Prototype/` — Python prototype code (agent, requirements, etc.)

Quick start

1. Use the project virtual environment if present

   If a project virtualenv exists at `env`, use it:

   ```bash
   source env/bin/activate
   # or run with the venv python directly:
   env/bin/python -m pip install -r Prototype/requirements.txt
   ```

2. Create a virtualenv (if you don't have one)

   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -U pip
   pip install -r Prototype/requirements.txt
   ```

3. Verify installation

   ```bash
   env/bin/python -c "import importlib; print(importlib.import_module('flask').__version__)"
   ```

Notes
- `Prototype/requirements.txt` contains pinned dependencies used for development.
- `.gitignore` is included at the repo root to ignore virtualenvs, caches, and editor files.

Secrets and environment variables
- WARNING: Do NOT hardcode secrets (API keys, passwords, tokens) in the repository or source files.
   Use a `.env` file (kept out of version control) or system environment variables.

   - Create a local `.env` (do not commit it):

      ```bash
      # example, edit with your real values (never commit this file)
      OPENAI_API_KEY=sk-...
      SECRET_KEY=change-me-to-a-secure-value
      DATABASE_URL=sqlite:///data.db
      ```

   - Add `.env` to `.gitignore` (already included).
   - Consider keeping `.env.example` in the repo with placeholder keys so collaborators know which variables to set.

Git

```bash
git status
git log --oneline -n 5
```

Contributing
- Open an issue or make a branch for feature work. Keep changes small and add a short description.

License
- (Add license information here if applicable.)
