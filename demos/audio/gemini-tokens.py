# Check token usage and cost after a run (works with any provider)
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic_ai import Agent, BinaryContent
from pydantic_ai.usage import UsageLimits

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODEL = "google-gla:gemini-2.5-flash"

# Gemini audio: ~32 tokens/sec (1,920/min). Video: ~300 tokens/sec.
PRICE_INPUT = 0.10   # $/M input tokens for gemini-2.5-flash
PRICE_OUTPUT = 0.40  # $/M output tokens

agent = Agent(MODEL)
result = agent.run_sync(
    ["Transcribe this audio.", BinaryContent(data=AUDIO.read_bytes(), media_type="audio/mpeg")],
    usage_limits=UsageLimits(total_tokens_limit=500_000),  # safety cap
)
print(result.output[:200], "...\n")

usage = result.usage()
cost = (usage.input_tokens / 1e6) * PRICE_INPUT + (usage.output_tokens / 1e6) * PRICE_OUTPUT
print(f"Input:  {usage.input_tokens:,} tokens")
print(f"Output: {usage.output_tokens:,} tokens")
print(f"Total:  {usage.total_tokens:,} tokens")
print(f"Cost:   ${cost:.4f}")
