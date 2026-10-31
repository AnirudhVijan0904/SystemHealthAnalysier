# System Health Analyser (PlatformGPT)

Chat app that reads sample platform logs, summarizes health issues, and can show a deployment diagram of failing component calls.

## Requirements

- Python 3.11 or newer (3.13 works)
- A [Google Gemini API key](https://aistudio.google.com/apikey)
- [Graphviz](https://graphviz.org/download/) (needed for PNG diagrams). On Windows, install it and confirm `dot.exe` exists. Typical path:

  `C:\Program Files (x86)\Graphviz\bin\dot.exe`

  If `where.exe dot` fails, add that `bin` folder to your PATH, or the app will still look in the common install locations.

## Setup

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set your key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Do not commit `.env`.

## Run

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## What to try

Text-only health check:

```text
Is everything up with my applications? Give a concise summary of any critical issues.
```

Diagram in the chat:

```text
Can you help me visualize the issue using deployment diagrams?
```

The diagram is also available at `/diagram` and downloadable from `/diagram/download`.

## Notes

- The UI title is **PlatformGPT**. The GitHub repository name is still `SystemHealthAnalysier`.
- Sample logs and maps live under `agent_code/data/`.
