# TikTok Video Settings

## Voice
- **Engine:** Kokoro TTS
- **Model:** `/tmp/kokoro-v1.0.onnx`
- **Voices file:** `/tmp/voices-v1.0.bin`
- **Voice:** `bm_lewis` (British male, smooth/soothing)
- **Speed:** `0.85` (slightly slowed for dramatic effect)
- **Lang:** `en-us`

> Note: Kokoro model files live in /tmp and will need re-downloading after VPS reboot:
> ```
> wget -q https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx -O /tmp/kokoro-v1.0.onnx
> wget -q https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin -O /tmp/voices-v1.0.bin
> ```

## Background Video
- **Source:** YouTube via yt-dlp
- **Quality:** 1080p60 vertical (1080x1920)
- **Client:** `mediaconnect` (bypasses SABR/nsig)
- **Cookies:** `/root/yt_cookies.txt` (George's YouTube cookies)
- **Command:**
  ```bash
  yt-dlp --cookies /root/yt_cookies.txt \
    --no-js-runtimes --js-runtimes node \
    --extractor-args "youtube:player_client=mediaconnect" \
    -f "299+140" -o "/tmp/tiktok-video/minecraft_bg.mp4" \
    "YOUTUBE_URL"
  ```
- **Best source type:** Long Minecraft parkour compilations (not Shorts — Shorts cap at 360p)
- **Minecraft parkour background audio:** Keep at ~15% volume for ambiance

## Captions Style
- **Font:** Arial Bold, size 26
- **Color:** White (`&H00FFFFFF`) with thick black outline (3px) + shadow
- **Position:** Dead center of screen (`Alignment=5` in ASS = center-middle)
- **Style:** Flashy — bold, high contrast, black outline + drop shadow
- **Format:** ASS subtitle file (not SRT) for precise positioning
- **ASS Style line:**
  ```
  Style: Default,Arial,26,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,3,2,5,30,30,0,1
  ```

## Output
- **Resolution:** 1080x1920 (9:16 vertical)
- **FPS:** 60
- **Video codec:** libx264, CRF 18, preset fast
- **Audio:** AAC 192k
- **Output folder:** `/tmp/tiktok-video/`
- **Workspace copies:** `/home/node/.openclaw/workspace/tiktok/videos/`

## Download Link (for George's PC)
- Served via Python HTTP on port 7654
- PowerShell: `Invoke-WebRequest -Uri "http://178.156.248.17:7654/FILENAME" -OutFile "C:\Users\georg\Downloads\FILENAME"`

## Story Style
- Creepy/horror short stories (30–60 seconds)
- Short punchy sentences with dramatic pauses
- Twist ending
- ~10 sentences max
