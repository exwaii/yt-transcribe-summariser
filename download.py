import time
from pytube import YouTube

FORBIDDEN_FOLDER_CHARS = '\\/:*?"<>|'

def get_audio_spotify(url):
    pass

def get_video_yt(url):
    start = time.time()
    print("getting youtube audio")
    yt = YouTube(url)
    for char in FORBIDDEN_FOLDER_CHARS:
        yt.title = yt.title.replace(char, "")
        if yt.description:
            yt.description = yt.channel_urldescription.replace(char, "")
    original_title = yt.title
    yt.title = yt.title + " video"
    path = yt.streams.filter(progressive=True).order_by('resolution').desc()[0].download(f"transcriptions\\{original_title}")
    print(path)
    with open(f"transcriptions\\{original_title}\\url.txt", "w") as f:
        f.write(url)
    download_time = time.time() - start
    print(f"youtube audio downloaded in {download_time // 60} minute(s) and {download_time % 60} second(s)")
    return original_title, yt.description, path

def get_audio_yt(url):
    # TODO
    # GET SUBTITLES IF THERE ARE SUBTITLES
    # PUNCTUATE AND PARAGRAPH AND REMOVE REDUNCANCIES IN TRANSCRIPT
    # SUBTITLES HAVE TIMESTAMPS, FIGURE OUT HOW TO MAKE TRANSCRIPTION TIMESTAMPS FROM WHISPER CODE
    # WITH SUMMARY, CAN MAKE LIKE A CONTENTS PAGE (IF THERE ISNT ALREADY)
    # GPT PULL OUT KEY POINTS, AND TIMESTAMPS WHERE

    start = time.time()
    print("getting youtube audio")
    yt = YouTube(url)
    title = yt.title
    description = yt.description
    print(yt)
    for char in FORBIDDEN_FOLDER_CHARS:
        title = title.replace(char, "")
        if description:
            description = description.replace(char, "")
    path = yt.streams.get_audio_only().download(f"static\\transcriptions\\{title}")
    print(path)
    with open(f"static/transcriptions/{title}/url.txt", "w") as f:
        f.write(url)
    download_time = time.time() - start
    print(f"youtube audio downloaded in {download_time // 60} minute(s) and {download_time % 60} second(s)")
    return title, description, path

def main():
    get_video_yt(input("Enter youtube url: "))


if __name__ == "__main__":
    main()