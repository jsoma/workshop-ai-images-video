These are teaching demos for a journalism workshop. They are intentionally terse, single-purpose, and readable by beginners. Do NOT "improve," refactor, or add robustness to them.

RULES:
- One file = one concept. Multi-tool workflows go in `recipes/`.
- 15–60 lines per file. No exceptions.
- No error handling. No `if __name__`. No logging module. No defensive coding. No try/except. Scripts run top-to-bottom.
- No docstrings. No inline comments except a single `#` comment on line 1 describing what the file does.
- No type annotations beyond Pydantic models.
- No argparse, click, or CLI argument parsing.
- No `__init__.py`. These are not packages.
- No `requirements.txt`. Dependencies are in `pyproject.toml`.
- Do NOT refactor to reduce duplication across files. Every file must be self-contained and copy-pasteable.
- Do NOT delete `.pt` model weights in the root. YOLO/Ultralytics downloads them at runtime.

PATTERNS — follow these exactly when writing or editing demos:
- `pathlib.Path` for all file paths, never raw strings.
- `DATA = Path(__file__).parent.parent / "data"` for input files.
- `.env` loaded via `load_dotenv(Path(__file__).resolve().parents[1] / ".env")` when API keys are needed.
- Constants in CAPS right after imports.
- `print()` for output.
- Section markers (`# --- Step 1 ---`) only in multi-step recipes.
- Bare `df` at end of file is fine (pretty-prints in notebooks).

STRUCTURED OUTPUT — use Pydantic AI:
- All LLM demos returning structured data MUST use `pydantic_ai.Agent` with `output_type=`.
- Do NOT use Instructor.
- Do NOT use provider-specific `response_schema` / `GenerateContentConfig`.
- Pydantic `Field(description=...)` does the prompting — keep descriptions short.

AUDIO/VIDEO via Gemini:
- Audio (small files): `BinaryContent(data=path.read_bytes(), media_type="audio/mpeg")`
- Video (large files): upload via `GoogleProvider().client.files.upload()`, pass as `VideoUrl(url=file.uri, media_type=file.mime_type)`. Include processing wait loop.
- YouTube: `VideoUrl(url="https://youtube.com/...")`
- Token usage: `result.usage()` after any run. `UsageLimits` for caps. No provider-specific `count_tokens`.

NAMING — do NOT shadow package names:
- Never name a script the same as an installed package (e.g. `whisperx.py`, `pyannote.py`).
- Use prefixed names instead: `transcribe-whisperx.py`, `diarize-pyannote.py`.
- The `audio/` dir runs from the demos root, so any `foo.py` there shadows `import foo`.

HIDDEN LINES — lines ending with `# hidden` are stripped by patchwork-builder:
- Use for suppressing warnings/logging in demos that would clutter notebook output.
- Example: `import warnings  # hidden`

CELL BREAKS — `# --- cell ---` splits a script into multiple notebook cells:
- Use to show intermediate output between steps.
- A bare expression (e.g. `df`, `result.output`) at end of a cell section gets auto-displayed.
- A line starting with `#` immediately after `# --- cell ---` becomes a markdown cell.

FOLDER STRUCTURE:
- vision-llm/ — LLM + image
- detection/ — object detection (YOLO, YOLOE, Grounding DINO)
- classification/ — zero-shot (CLIP, SigLIP)
- documents/ — text extraction, page classification, structured data from PDFs (natural-pdf)
- audio/ — transcription and diarization (WhisperX, Gemini, pyannote)
- video/ — video processing (download, frames, scenes, Gemini)
- tracking/ — object tracking
- search/ — semantic image search (CLIP + ChromaDB)
- recipes/ — multi-step workflows combining the above

ENVIRONMENT SETUP:
- The venv lives at `ai-images-video/.venv` (Python 3.12). NOT `demos/.venv`.
- `demos/.venv` is a leftover stripped-down venv — do not use it.
- Dependencies are in `demos/pyproject.toml`. Audio packages (whisperx, nemo, pyannote) are
  NOT in pyproject.toml — they are installed separately via `uv pip install` into the root venv.
- API keys (OPENAI_API_KEY, GOOGLE_API_KEY, ANTHROPIC_API_KEY, HF_TOKEN) live in `ai-images-video/.env`.
- `demos/.env` is a symlink to `../.env`.

RUNNING SCRIPTS:
- From `demos/` directory: `../. venv/bin/python vision-llm/basic.py`
- Or: `/path/to/ai-images-video/.venv/bin/python demos/vision-llm/basic.py`
- First run on Dropbox can be extremely slow (minutes) due to .pyc bytecache writes triggering sync.
  Warm cache first: `.venv/bin/python -m compileall -q .venv/lib/`

BUILDING NOTEBOOKS (patchwork-builder):
- Tool lives at `~/Development/patchwork-builder`. Installed via `uv tool install -e .`
- Workshop .md files in `workshops/` reference scripts via ```script blocks.
- Build: `patchwork-build workshops/nicar-2026/`
- Build + execute: `patchwork-build workshops/nicar-2026/ --execute` (calls APIs, costs money)
- Output: `notebooks/` (generated .ipynb) and `docs/` (generated HTML). Do NOT edit these directly.
- The builder strips `load_dotenv` lines, rewrites `Path(__file__)` paths, strips `# hidden` lines,
  and splits on `# --- cell ---` markers.
