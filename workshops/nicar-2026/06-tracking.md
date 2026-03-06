---
install:
  - opencv-python-headless
  - supervision
  - ultralytics
data_files:
  - "istockphoto-534232220-640_adpp_is.mp4"
---
# Bonus: Tracking & Counting

Want to reproduce [this Bloomberg piece about congestion pricing?](https://www.bloomberg.com/graphics/2025-nyc-congestion-pricing-week-one-traffic-mix-shifts/) We can get about 60% of the way there!

The library doing the heavy lifting here is [supervision](https://supervision.roboflow.com/), which handles tracking, drawing, and counting on top of any object detection model. It's fantastic.

```show
data/istockphoto-534232220-640_adpp_is.mp4
```

## Step 1: Detect

First, we just detect objects in a single frame. YOLO finds the cars, supervision draws the boxes.

```script{log=error}
tracking/detect.py
```

## Step 2: Track

Now we add **tracking**. ByteTrack links detections across frames — "that's car #7, same one from 3 seconds ago." Each object gets a unique ID and a motion trail.

```script{log=error}
tracking/track.py
```

## Step 3: Count

Draw a virtual line across the road. Every time a tracked object crosses it, the counter ticks up. Think: counting cars at an intersection, people entering a building, boats passing under a bridge.

```script{log=error}
tracking/count.py
```

The actual count is around 20 in and 20 out. How close did we get?

## ...but can Gemini just do this?

We've been using Gemini for all sorts of stuff. Let's see if it can count cars in the video. We upload the same clip and ask it to count.

```script{log=error}
tracking/gemini-count.py
```

**The answer is: no, not really.** LLMs are bad at counting things in video – they're great at *vibes*, they're great as yes/no, but measurements are where things get iffy (at least at the moment). This is exactly the kind of task where boring traditional computer vision (detection + tracking + counting) beats the "just ask AI" approach.

## Going further

What if you don't just want *cars*, though — you want to be Bloomberg, and spot taxis and box trucks and commercial vehicles! While you might try to find a model that does that, you can also **train your own** with a handful of labeled images.

If you're interested in going to the next level, check out [the Roboflow docs](https://blog.roboflow.com/getting-started-with-roboflow/) — you can train a custom YOLO model, swap it in, and everything else stays the same.
