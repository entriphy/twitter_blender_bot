# Twitter Blender Bot
Twitter bot that tweets a random animation from a .blend file. This project is used for [@klonoa_anim_bot](https://twitter.com/klonoa_anim_bot). Since this is currently targeted for rendering Klonoa animations, you may need to adjust the `blender.py` script if you want to render animations from a different blend file. 

Sample .blend files are provided in the "Klonoa Animations" section.

NOTE: Windows and macOS are currently unsupported.

# Setup + Running
1. Install the [`tweepy`](https://pypi.org/project/tweepy/) package.
    * `pip install tweepy`
2. Ensure `blender`, `ffmpeg`, `ffprobe` are installed and in `PATH`.
    *  The path to these executables can also be set in `config.json`. On Windows and macOS, you will most likely need to do this.
3. Add Twitter API and bot account credentials in `config.json` (see "Configuration" section).
4. Place .blend file(s) in the `blend` directory.
    * Ensure the scene has one armature named "Armature" with actions associated with it and at least one camera. If there is more than one camera in the scene, a random camera will be selected.
5. Run the main script.
    * `python index.py`

# Configuration
The script can be configured by editing `config.json`.

## Twitter configuration
All fields are required to tweet the rendered video. API keys can be retrieved by creating an application in the Twitter Developer Portal, and account credentials for the bot account can be retrieved by following Twitter's [3-legged OAuth 1.0 Flow](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens).
| Name                  | Type  | Description                                      |
|-----------------------|-------|--------------------------------------------------|
| `consumer_key`        | `str` | Key for Twitter API application.                 |
| `consumer_secret`     | `str` | Secret for Twitter API application.              |
| `access_token`        | `str` | Access token for the Twitter bot account.        |
| `access_token_secret` | `str` | Access token secret for the Twitter bot account. |
| `callback`            | `str` | Callback URL for Twitter API application.        |

## General Configuration
| Name                | Type    | Description                                                                                                                                                                                                                                |
|---------------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `default_blend`     | `str`   | Filename of default blend file to render. Think of this like a "priority" blend file, i.e. you want to render and tweet a certain blend file more than others. If empty, a random blend file from the  `blend` directory will be selected. |
| `nondefault_chance` | `float` | The percentage chance that a nondefault blend file will be randomly selected. Must be a value between 0.0 and 1.0. Only works if `default_blend` is not empty.                                                                             |
| `gif_duration`      | `float` | The max video length allowed when converting the rendered video to a GIF. If the video length exceeds this number, the video file will not be converted to a GIF and will be uploaded as an MP4.                                           |
| `blender_path`      | `str`   | Path to Blender executable.                                                                                                                                                                                                                |
| `ffmpeg_path`       | `str`   | Path to FFmpeg executable.                                                                                                                                                                                                                 |
| `ffprobe_path`      | `str`   | Path to ffprobe executable.                                                                                                                                                                                                                |

## KPRS configuration
These fields are required when using the `kprs_anim_info.py` script to extract animation descriptions.
| Name        | Type        | Description                                                                                 |
|-------------|-------------|---------------------------------------------------------------------------------------------|
| `kprs_path` | `str`       | Path to [Klonoa Phantasy Reverie Series](https://store.steampowered.com/app/1730680/Klonoa_Phantasy_Reverie_Series) install directory (ex. .../steamapps/common/KLONOA). |
| `kprs_chrs` | `list[str]` | List of character IDs to extract animation descriptions from.                               |

## Klonoa Animations
An archive of all blend files being used for [@klonoa_anim_bot](https://twitter.com/klonoa_anim_bot) can be downloaded from [here](https://files.catbox.moe/gbtx8i.zip). The bot uses the following configuration:
```
{
    "default_blend": "klonoa.blend",
    "nondefault_chance": 0.25,
    "gif_duration": 2.0
}
```