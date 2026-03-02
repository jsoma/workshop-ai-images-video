# Images

You already know what to do with text: summarize it, answer questions about it, extract data from it. Images, audio, and video are just ways of **getting to text and structured data.**

## Structured output

Send an image to an LLM and get back structured data — fields you can sort, filter, and verify. Not prose. This is the pattern for everything else in the workshop.

```show
data/car.jpg
```

```script
vision-llm/structured.py
```

Notice the Pydantic model: each field has a name, a type, and a description. The LLM fills in the fields. If it's wrong, you can see *which* field is wrong.

## Batch processing

Same thing, whole folder. Out comes a CSV.

```script
vision-llm/batch.py
```

Open the output CSV. Spot-check a few rows against the source images. Does the make match what you see? Does the color? That's verification — not trusting the model, checking its work.

## Swap providers

Same structured task, different LLM provider. Change one string.

```script
vision-llm/providers.py
```

OpenAI, Google, Anthropic, Ollama — the code is identical except for the model name. Pick whichever fits your newsroom's budget, privacy needs, or existing accounts.
