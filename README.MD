# Playlist Generator

This repository contains a generator for an M3U playlist comprising various resources, such as YouTube, Twitch, Dailymotion, and direct URL streaming.

**Disclaimer:**

Please note that the M3U links provided may lead to content sources. It is your responsibility to ensure compliance with copyright laws and usage policies while using this software. The generator and the repository owner are not responsible for the use or misuse of this software, including any links to potentially copyrighted or pirated content.

## How to Install:

1. Click on the "Use this template" button and create a new public repository.
2. Navigate to the repository settings -> Actions -> General -> Workflow permissions.
3. Choose "Read and Write" permissions and save the settings.
4. Go to Actions, select "M3U Generator" -> Run Workflow -> Run Workflow.
5. Verify that the workflow ran successfully.

## How to Use:

1. Edit the file `channel_info.txt` following the specified format:
FORMAT: 'channel name' | 'group name' | 'logo' | 'tvg-id'

Channel 1 | Movies | https://example.com/Channel1.jpg | ch1
https://www.youtube.com/@Channel1/live


2. Save and commit the changes to your repository.
3. Run the workflow again.
4. Access `playlist.m3u`, obtain the RAW file, and copy the URL.
5. Paste the URL in VLC or your preferred media player to enjoy!

**The workflow runs every 3 hours, updating the links.**


