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
