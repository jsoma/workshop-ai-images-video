---
env_keys:
  - HF_TOKEN
data_files:
  - "debate/*.jpg"
---
# The full pipeline

## Screen time

Frames → classify → per-subject screen time with percentages. This is the deliverable you'd bring to an editor meeting.

```script
recipes/screen-time.py
```

## Cost

Before you run a big batch: how much will it cost? Images × tokens × price = receipt.

```script
recipes/cost.py
```
