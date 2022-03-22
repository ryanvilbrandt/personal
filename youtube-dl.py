import youtube_dl

# Extract audio from playlist, with auto-numbering
ydl_opts = {
    'cachedir': False,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    # "outtmpl": "%(playlist_index)s - %(title)s.%(ext)s"
    "outtmpl": "%(title)s.%(ext)s"
}

# Download video with subtitle
# ydl_opts = {
#     "writesubtitles": True,
#     # "skip_download": True,
# }
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([
        "https://www.youtube.com/watch?v=z_4cEbrRwKs"
    ])
