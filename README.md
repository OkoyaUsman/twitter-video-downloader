# Twitter Video Downloader

A Python tool to download videos from Twitter/X tweets using only the tweet URL. No authentication required!

## Features

- 🎥 Download videos from any public Twitter/X tweet
- 📁 Automatically saves videos to an `output` directory
- 🎬 Support for multiple videos in a single tweet (frame selection)
- 🚀 Simple command-line interface
- 🔒 No Twitter account or API keys required
- ✨ Automatic file naming with tweet ID

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install curl-cffi
```

Or if you prefer using a requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Download a video from a Twitter/X URL:

```bash
python main.py "https://x.com/username/status/1234567890"
```

The video will be saved as `{tweet_id}.mp4` in the `output` directory.

### Custom Filename

Specify a custom filename for the downloaded video:

```bash
python main.py "https://x.com/username/status/1234567890" --file_name "my_video.mp4"
```

### Multiple Videos in a Tweet

If a tweet contains multiple videos, you can specify which one to download using the `--frame` parameter:

```bash
python main.py "https://x.com/username/status/1234567890" --frame 2
```

The frame number can be 1, 2, 3, or 4 (default is 1).

### Complete Example

```bash
python main.py "https://x.com/OkoyaUsman/status/1692989065241469174" --file_name "twitter_video.mp4" --frame 1
```

## Command-Line Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `url` | string | Yes | - | Twitter/X URL of the tweet |
| `--file_name` | string | No | `{tweet_id}.mp4` | Custom filename for the downloaded video |
| `--frame` | integer | No | 1 | Frame number (1-4) if tweet has multiple videos |

## How It Works

1. Extracts the tweet ID from the provided Twitter/X URL
2. Uses Twitter's GraphQL API to fetch tweet data (no authentication required)
3. Parses the video information from the tweet data
4. Downloads the highest quality video variant available
5. Saves the video to the `output` directory

## Project Structure

```
twitter-video-downloader/
├── main.py          # Main script with TwitterVideoDownloader class
├── output/          # Directory where downloaded videos are saved (created automatically)
├── README.md        # This file
└── LICENSE          # License file
```

## Requirements

- `curl-cffi`: For making HTTP requests with browser impersonation
- Python 3.7+

## Error Handling

The script handles various error cases:
- Invalid Twitter URLs
- Tweets without videos
- Network errors
- API failures

Error messages will be displayed in the console if something goes wrong.

## Limitations

- Only works with public tweets
- Requires the tweet to contain video media
- Downloads the highest quality variant available
- May break if Twitter changes their API structure, feel free to open issue in that case

## License

See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational purposes only. Please respect Twitter/X's Terms of Service and copyright laws when downloading content. Only download videos that you have permission to download.

## Author

Created by [OkoyaUsman](https://x.com/OkoyaUsman)

## Support

If you encounter any issues or have questions, please open an issue on GitHub.