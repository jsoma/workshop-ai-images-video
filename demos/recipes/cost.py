# Estimate API cost for a batch of images. No API key needed.

# USD per million tokens (Feb 2026)
PRICE_TABLE = {
    "gpt-4o-mini":       (0.15, 0.60),
    "gpt-4o":            (2.50, 10.00),
    "gpt-5-nano":        (0.05, 0.20),
    "gemini-2.5-flash":  (0.10, 0.40),
    "gemini-2.5-pro":    (1.25, 5.00),
    "claude-3-5-haiku":  (0.80, 4.00),
    "claude-3-5-sonnet": (3.00, 15.00),
    "ollama":            (0.00, 0.00),
}

NUM_IMAGES = 500
MODEL = "gpt-4o-mini"
INPUT_TOKENS_PER_IMAGE = 1000
OUTPUT_TOKENS_PER_IMAGE = 200

# --- Calculate ---
input_price, output_price = PRICE_TABLE[MODEL]
total_input = NUM_IMAGES * INPUT_TOKENS_PER_IMAGE
total_output = NUM_IMAGES * OUTPUT_TOKENS_PER_IMAGE
input_cost = (total_input / 1_000_000) * input_price
output_cost = (total_output / 1_000_000) * output_price
total_cost = input_cost + output_cost

print(f"Model:       {MODEL}")
print(f"Images:      {NUM_IMAGES:,}")
print(f"Input cost:  ${input_cost:.4f}  ({total_input:,} tokens @ ${input_price}/M)")
print(f"Output cost: ${output_cost:.4f}  ({total_output:,} tokens @ ${output_price}/M)")
print(f"TOTAL:       ${total_cost:.4f}")
