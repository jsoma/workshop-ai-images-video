---
data_files:
  - "car.jpg"
  - "sky.jpg"
  - "cars/*.jpg"
---
# Images

You already know what to do with text: summarize it, answer questions about it, extract data from it. Images, audio, and video are just ways of **getting to text and structured data.**

## Asking questions of images

It's easy enough to send an image to an LLM and ask it some questions. It's easy to read and great for a one-off, but *very* hard to sort or filter across hundreds of images.

```show
data/car.jpg
```

Let's get some details about this car.

```script
vision-llm/raw-openai-text.py
```

It's great, but... what if we want it in a CSV? What if we have 200 to do? What if we want to make *demands* and ask for *structure?*

## Structured output

An alternative is to send an image to an LLM and get back **structured output** — fields you can sort, filter, and verify. Not prose. This is the pattern for everything else in the workshop!

```script
vision-llm/structured.py
```

While there are a handful of ways to do this, we're specifically using a Python library called **Pydantic**. It gives you a lot of tools to describe what you're looking for: each field has a name, a type, and a description. AI fills in the fields.

Easy peasy!

## Batch processing

Same thing as before, but we have **a whole folder of images**. And instead of one at a time, you can make an entire CSV!

```script
vision-llm/batch.py
```

Open the output CSV. Spot-check a few rows against the source images. Does the make match what you see? Does the color? That's verification — not trusting the model, checking its work.

## Swap providers

There are a ton of different providers of LLM *stuff* and they each have strengths and weaknesses. if you get married to ChatGPT or Claude, you'll never be able to use Gemini's document-processing powers! So instead of using the [genai library from Google](https://github.com/googleapis/python-genai) or the [OpenAI library](https://github.com/openai/openai-python) we use Pydantic AI, which allows you a bit more flexibility in swapping between providers.

If you're feeling especially wild, you can even try out [openrouter](https://openrouter.ai/), which gives you a menu of *way more* than just the Big Three.

```script
vision-llm/providers.py
```

OpenAI, Google, Anthropic, Ollama — the code is identical except for the model name. Pick whichever fits your newsroom's budget, privacy needs, or existing accounts.
