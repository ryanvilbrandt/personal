import youtube_dl

# Extract audio from playlist, with auto-numbering
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    "outtmpl": "%(playlist_index)s - %(title)s.%(ext)s"
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(["https://www.youtube.com/playlist?list=PLvNp0Boas720sJW-iF7HFdHQqm03VKIj9"])
