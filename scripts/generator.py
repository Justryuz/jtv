#!/usr/bin/python3

import requests
import os
import sys
import streamlink
import logging
from logging.handlers import RotatingFileHandler
import json

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = "log.txt"
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=2)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Constants
BANNER = '''
Your Banner Here
'''
VALID_URL_SUFFIXES = ('.m3u', '.m3u8', '.ts')


def grab(url):
    if url.endswith(VALID_URL_SUFFIXES):
        logger.debug("URL ends with a valid streaming suffix: %s", url)
        if check_url(url):
            return url
        else:
            logger.error("Valid streaming URL is not reachable: %s", url)
            return None

    try:
        session = streamlink.Streamlink()
        streams = session.streams(url)
        logger.debug("URL Streams %s: %s", url, streams)
        if "best" in streams:
            return streams["best"].url
        return None
    except streamlink.exceptions.NoPluginError as err:
        logger.error("URL Error No PluginError %s: %s", url, err)
        return url
    except streamlink.StreamlinkError as err:
        logger.error("URL Error %s: %s", url, err)
        return None


def check_url(url):
    try:
        # Use a GET request and stream=True to avoid downloading the entire file
        response = requests.get(url, timeout=15, stream=True)
        response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.close()  # Ensure the connection is closed after checking the URL
        return True
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP Error for URL %s: %s", url, e.response.status_code)
    except requests.exceptions.ConnectionError as e:
        logger.error("Connection Error for URL %s: %s", url, e)
    except requests.exceptions.Timeout as e:
        logger.error("Timeout Error for URL %s: %s", url, e)
    except requests.exceptions.RequestException as e:
        logger.error("RequestException for URL %s: %s", url, e)
    return False


def process_channel_info(channel_info_path):
    channel_data = []

    try:
        with open(channel_info_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('~~'):
                    continue
                if not line.startswith('https:') and not line.startswith('http:'):
                    ch_info = line.split('|')
                    if len(ch_info) < 4:
                        logger.error(f"Invalid line format: {line}")
                        continue
                    ch_name, grp_title, tvg_logo, tvg_id = [info.strip() for info in ch_info]
                    channel_data.append({
                        'type': 'info',
                        'ch_name': ch_name,
                        'grp_title': grp_title,
                        'tvg_logo': tvg_logo,
                        'tvg_id': tvg_id,
                        'url': ''
                    })
                else:
                    link = grab(line)
                    if link:
                        channel_data.append({
                            'type': 'link',
                            'url': link
                        })
                    else:
                        logger.warning(f"Unreachable or unsupported URL: {line}")

    except Exception as e:
        logger.error(f"Error processing channel_info.txt: {e}")

    return channel_data


def main():
    print(BANNER)

    channel_info_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../channel_info.txt'))
    channel_data = process_channel_info(channel_info_path)

    # Generate M3U playlist and JSON data
    playlist_data = ['#EXTM3U']
    channel_data_json = []

    prev_item = None

    for item in channel_data:
        if item['type'] == 'info':
            prev_item = item
        elif item['type'] == 'link' and item['url']:
            playlist_data.extend([
                f'#EXTINF:-1 group-title="{prev_item["grp_title"]}" tvg-logo="{prev_item["tvg_logo"]}" tvg-id="{prev_item["tvg_id"]}", {prev_item["ch_name"]}',
                item['url']
            ])
            channel_data_json.append({
                "id": prev_item["tvg_id"],
                "name": prev_item["ch_name"],
                "alt_names": [""],
                "network": "",
                "owners": [""],
                "country": "AR",
                "subdivision": "",
                "city": "Buenos Aires",
                "broadcast_area": [""],
                "languages": ["spa"],
                "categories": [prev_item["grp_title"]],
                "is_nsfw": False,
                "launched": "2016-07-28",
                "closed": "2020-05-31",
                "replaced_by": "",
                "website": item['url'],
                "logo": prev_item["tvg_logo"]
            })

    try:
        with open("playlist.m3u", "w") as f:
            f.write('\n'.join(playlist_data))

        with open("playlist.json", "w") as f:
            json.dump(channel_data_json, f, indent=2)

    except Exception as e:
        logger.error(f"Error writing to file: {e}")


if __name__ == "__main__":
    main()
