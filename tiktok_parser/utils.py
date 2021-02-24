import requests
import json
import base64
import time
import re
import urllib.parse


def get_video_by_id(shortcode):
    if shortcode == "":
        return False
    base_url = f"https://api.wppress.net/tiktok/nwm/{shortcode}"
    data = requests.get(base_url)
    try:
        data = data.json()
        return data
    except:
        return False


def download_video_by_id(username, shortcode):
    # download video no water mark
    if shortcode == "":
        return False
    video = get_video_by_id(shortcode)
    if video:
        video_id = video["id"]
        res = requests.get(
            f"https://api-h2.tiktokv.com/aweme/v1/play/?video_id={video_id}&vr_type=0&is_play_url=1&source=PackSourceEnum_FEED&media_type=4&ratio=default&improve_bitrate=1",
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 OPR/72.0.3815.378",
                "referer": "https://www.tiktok.com/",
            },
        )
        with open(f"{username}/{shortcode}.mp4", "wb") as fb:
            fb.write(res.content)
        return True
    return False
