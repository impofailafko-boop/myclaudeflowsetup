#!/usr/bin/env python3
"""
YouTube Transcript Downloader for Leapableai Channel
Run this script locally on your machine to download all video transcripts.

Usage:
    pip install youtube-transcript-api
    python3 download_transcripts.py
"""

import os
import json
from youtube_transcript_api import YouTubeTranscriptApi

# Video data
videos = [
    {"id": "fv8qtNl0tYk", "title": "I'm Giving You the Tools to 100x Your AI Output"},
    {"id": "ZbGtnDhEq2o", "title": "Multi-Agent AI: 106 Page Research Paper in 6 Hours (Workflow)"},
    {"id": "HFfSYnsEGUA", "title": "Git Workflow: The Lazy Way to Perfect Code"},
    {"id": "mYynhkUMIhg", "title": "43 AI Agents Wrote My PHD Research Paper"},
    {"id": "h0Um5rl2CXs", "title": "I Fed Gemini 3 250k Tokens. Here's What It Built."},
    {"id": "laAJONqtcXI", "title": "This Multi-Agent AI Search Algorithm is a Game-Changer (Full Blueprint)"},
    {"id": "CWCBafSFiUg", "title": "AI-Proof Education: The 100 Holes Method to Stop Cheating"},
    {"id": "LnMHh9fYB3k", "title": "How I Orchestrate 8 AI Agents for Unbeatable Business Positioning"},
    {"id": "S2y7nb2yA7g", "title": "AI-Native Course Design: Transforming Education Beyond Traditional Methods"},
    {"id": "iXbq--kc3dc", "title": "How I Used AI to Discover Things No One Else Has Found"},
    {"id": "aYG3NRN0Yz0", "title": "A Masterclass in AI Context Engineering"},
    {"id": "2urhrcdYYrQ", "title": "This AI Coding Gamification System Writes Better Code Than Humans"}
]

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

successful = []
failed = []

print("=" * 80)
print("YouTube Transcript Downloader - Leapableai Channel")
print("=" * 80)
print(f"\nTotal videos to download: {len(videos)}\n")

for idx, video in enumerate(videos, 1):
    video_id = video["id"]
    title = video["title"]
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()

    print(f"[{idx}/{len(videos)}] Fetching: {title}")

    try:
        # Get transcript using the API
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=['en'])
        transcript_list = list(fetched)

        # Save as JSON
        json_file = os.path.join(script_dir, f"{video_id}_{safe_title}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "video_id": video_id,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "transcript": [{"text": t.text, "start": t.start, "duration": t.duration} for t in transcript_list]
            }, f, indent=2, ensure_ascii=False)

        # Save as readable markdown
        md_file = os.path.join(script_dir, f"{video_id}_{safe_title}.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"**Video URL:** https://www.youtube.com/watch?v={video_id}\n\n")
            f.write(f"**Video ID:** {video_id}\n\n")
            f.write("---\n\n")
            f.write("## Transcript\n\n")
            for t in transcript_list:
                timestamp = int(t.start)
                minutes = timestamp // 60
                seconds = timestamp % 60
                f.write(f"**[{minutes:02d}:{seconds:02d}]** {t.text}\n\n")

        # Save as plain text
        txt_file = os.path.join(script_dir, f"{video_id}_{safe_title}.txt")
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
            f.write("=" * 80 + "\n\n")
            for t in transcript_list:
                f.write(f"{t.text}\n")

        successful.append(video)
        print(f"    ✓ Success - saved 3 files (.json, .md, .txt)")

    except Exception as e:
        failed.append({"video": video, "error": str(e)})
        print(f"    ✗ Failed: {str(e)[:80]}")

print("\n" + "=" * 80)
print(f"SUMMARY")
print("=" * 80)
print(f"✓ Successful: {len(successful)}")
print(f"✗ Failed: {len(failed)}")
print(f"\nFiles saved to: {script_dir}")
print("=" * 80)

# Update README
readme_file = os.path.join(script_dir, "README.md")
with open(readme_file, 'w', encoding='utf-8') as f:
    f.write("# Leapableai YouTube Transcripts\n\n")
    f.write(f"**Channel:** [@Leapableai](https://www.youtube.com/@Leapableai)\n\n")
    f.write(f"**Total Videos:** {len(videos)}\n")
    f.write(f"**Successfully Downloaded:** {len(successful)}\n")
    f.write(f"**Failed:** {len(failed)}\n\n")

    if successful:
        f.write("## Available Transcripts\n\n")
        for i, video in enumerate(successful, 1):
            safe_title = "".join(c for c in video['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
            f.write(f"{i}. **{video['title']}**\n")
            f.write(f"   - URL: https://www.youtube.com/watch?v={video['id']}\n")
            f.write(f"   - Files: `{video['id']}_{safe_title}.*` (.md, .txt, .json)\n\n")

    if failed:
        f.write("## Failed Downloads\n\n")
        for i, item in enumerate(failed, 1):
            f.write(f"{i}. **{item['video']['title']}**\n")
            f.write(f"   - Error: {item['error']}\n\n")

    f.write("\n## File Formats\n\n")
    f.write("Each transcript is saved in three formats:\n\n")
    f.write("- **Markdown (.md)**: Human-readable format with timestamps\n")
    f.write("- **Plain Text (.txt)**: Simple text format\n")
    f.write("- **JSON (.json)**: Structured data with timing information\n\n")

print(f"\nREADME.md updated successfully!")
