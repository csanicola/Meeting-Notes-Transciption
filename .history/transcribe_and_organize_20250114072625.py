import whisper
import os

# Path to iCloud Voice Memos folder
icloud_path = os.path.expanduser(
    "/Users/carolinesanicola/Library/Mobile Documents/com~apple~CloudDocs/Voice Memos/Meetings")
vault_path = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault/")

# Find the latest voice memo
files = [f for f in os.listdir(icloud_path) if f.endswith(".m4a")]
latest_file = max([os.path.join(icloud_path, f)
                  for f in files], key=os.path.getctime)

# Transcribe the audio
model = whisper.load_model("base")
result = model.transcribe(latest_file)
transcription = result["text"]

# Organize text into categories
discussion_points = []
follow_ups = []
for line in transcription.split("."):
    if "follow up" in line.lower() or "action" in line.lower():
        follow_ups.append(line.strip())
    else:
        discussion_points.append(line.strip())

# Create Markdown content
markdown_content = f"""
# Meeting Notes - {os.path.basename(latest_file)}

## Discussion Points
{"\n- ".join(discussion_points)}

## Follow-Ups
{"\n- ".join(follow_ups)}
"""

# Save to Obsidian vault
output_file = os.path.join(vault_path, "Meeting_Notes.md")
with open(output_file, "w") as f:
    f.write(markdown_content)

print(f"Markdown file saved to: {output_file}")
