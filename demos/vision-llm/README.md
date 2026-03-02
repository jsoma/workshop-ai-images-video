# vision-llm

Send images to cloud LLMs and get text or structured data back. Uses Pydantic AI as the default SDK, with one raw-client example for comparison.

## Files

| File | What it does |
|------|-------------|
| `basic.py` | Send one image to an LLM, get a text description |
| `structured.py` | Send one image, get structured Pydantic output |
| `batch.py` | Process a folder of images to DataFrame/CSV |
| `providers.py` | Same structured task across OpenAI, Google, Anthropic |
| `raw-openai.py` | Same task using the raw OpenAI SDK (base64 + JSON schema) |

Requires API keys in `.env` (OpenAI, Google, and/or Anthropic depending on the script).
