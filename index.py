import json
import os
import platform
import random
import subprocess
import sys
import time
import tweepy

def mp4_to_gif(filename) -> int:
    result = subprocess.run([ffmpeg_path, "-i", filename, "-vf", 'fps=50,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', filename.replace("mp4", "gif")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        raise Exception(result.stdout)
    return result.returncode

def get_length(filename) -> float:
    result = subprocess.run([ffprobe_path, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        raise Exception(result.stdout)
    return float(result.stdout)

def get_blend_files(dir) -> list[str]:
    return list(filter(lambda file: file.endswith(".blend"), os.listdir(dir)))

if __name__ == "__main__":
    # Load config from json file
    with open("config.json", "r") as f:
        config = json.load(f)

    if not os.path.exists("out"):
        # Create out directory if it doesn't exist
        os.mkdir("out")
    else:
        # Clean out directory (in case last script run was unsucessful)
        for file in os.listdir("out"):
            os.remove(f"out/{file}")

    # Get paths to executables (if set).
    blender_path = config["blender_path"] or "blender"
    ffmpeg_path = config["ffmpeg_path"] or "ffmpeg"
    ffprobe_path = config["ffprobe_path"] or "ffprobe"

    # Select which blend file to render from
    if len(sys.argv) > 1:
        # Get blend file from command line
        blend_file = sys.argv[1]
    else:
        if config["default_blend"] != "":
            # Select default blend file
            blend_file = config["default_blend"]

            # Random chance to select a nondefault blend file
            if random.randint(0, 100) / 100 < config["nondefault_chance"]:
                files = get_blend_files("blend") # Get list of blend files
                files.remove(blend_file) # Remove default blend file from list
                blend_file = random.choice(files) # Select random blend file
        else:
            # Select a random blend file
            blend_file = random.choice(get_blend_files("blend"))

    # Render a random animation from the blend file
    subprocess.run([blender_path, "--background", f"blend/{blend_file}", "--python", "blender.py"])
    video = os.listdir("out")[0] # Get filename of render
    name = os.path.splitext(video)[0] # Get animation name from filename

    # Convert mp4 to gif if length of video is <= gif_duration
    if get_length(f"out/{video}") <= config["gif_duration"]:
        mp4_to_gif(f"out/{video}") # Convert mp4 to gif
        os.remove(f"out/{video}") # Delete mp4 file
        video = video.replace(".mp4", ".gif")
    
    # Check if hostname_filter is set and exit if hostname_filter is not in hostname (for debugging/testing purposes)
    if config["hostname_filter"] != "" and config["hostname_filter"] not in platform.node():
        print(f"{config['hostname_filter']} not in hostname; exiting...")
        exit(0)
    
    # Tweepy setup
    auth = tweepy.OAuth1UserHandler(
        os.environ.get("TWITTER_CONSUMER_KEY") or config["consumer_key"], os.environ.get("TWITTER_CONSUMER_SECRET") or config["consumer_secret"],
        os.environ.get("TWITTER_ACCESS_TOKEN") or config["access_token"], os.environ.get("TWITTER_ACCESS_TOKEN_SECRET") or config["access_token_secret"],
        callback=os.environ.get("TWITTER_CALLBACK") or config["callback"]
    )
    api = tweepy.API(auth)

    # Upload video to Twitter
    uploaded = api.media_upload(f"out/{video}", media_category="TWEET_VIDEO" if video.endswith("mp4") else "TWEET_GIF", chunked=True)
    while (uploaded.processing_info.get("state", "") == "pending"):
        time.sleep(uploaded.processing_info["check_after_secs"])
        uploaded = api.get_media_upload_status(uploaded.media_id_string)
    
    # Send tweet
    status = name
    if os.path.exists("infos.json"):
        # Get animation description from infos.json
        with open("infos.json") as f:
            infos = json.load(f)
            status += f"\n{infos.get(name, '')}"
    api.update_status(status, media_ids=[uploaded.media_id_string])
    os.remove(f"out/{video}") # Delete video file
