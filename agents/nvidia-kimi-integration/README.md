# Nvidia Kimi Integration

## Purpose
Integration for Nvidia Kimi API specialized for video processing and vision tasks.

## Features
- Video processing capabilities
- Image analysis
- Multimodal tasks
- Rate limiting for trial/test keys
- Health monitoring

## Configuration
Uses `nvidia_kimi` section in `/opt/blackbox5/config/api-keys.yaml`.

## Environment Variables
- `NVIDIA_KIMI_KEY` - Nvidia Kimi API key (from environment)

## Usage
```python
from agents.nvidia_kimi_integration import NvidiaKimiClient

client = NvidiaKimiClient()

# Process video
result = client.process_video(video_path, prompt="Summarize this video")

# Analyze image
result = client.analyze_image(image_path, prompt="What's in this image?")
```
