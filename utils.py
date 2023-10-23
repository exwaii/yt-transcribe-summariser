# import whisper
import urllib.parse
import openai
from dotenv import load_dotenv
import os
import tiktoken
from datetime import timedelta


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

FORBIDDEN_FOLDER_CHARS = '\\/:*?"<>|'

LOCAL = True


def transcribe(title, path):
    if LOCAL:
        import whisper

        model = whisper.load_model("base")  # Change this to your desired model
        print("Whisper model loaded.")
        transcribe = model.transcribe(audio=path)
        segments = transcribe["segments"]
        transcript = ""
        for segment in segments:
            startTime = str(0) + str(timedelta(seconds=int(segment["start"]))) + ",000"
            endTime = str(0) + str(timedelta(seconds=int(segment["end"]))) + ",000"
            text = segment["text"]
            segmentId = segment["id"] + 1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
            transcript += segment

    else:
        audio_file = open(path, "rb")

        transcript = openai.Audio.transcribe(
            "whisper-1",
            audio_file,
            prompt=f"The following is a transcript of the audio file, with the title: {title}",
            response_format="srt",
        )
    with open(get_stem(path) + ".srt", "w") as f:
        f.write(transcript)

    return transcript


def timestamp_to_seconds(timestamp):
    hours, minutes, seconds_milli = timestamp.split(":")
    seconds, milliseconds = seconds_milli.split(",")
    total_seconds = (
        int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
    )
    return total_seconds


def get_stem(path):
    return os.path.splitext(path)[0]


def create_html(srt):
    lines = srt.strip().split("\n")
    html_output = []

    i = 0
    while i < len(lines):
        # Skip the index
        i += 1

        # Split the timestamps and create clickable links for both start and end
        start_timestamp, end_timestamp = lines[i].split(" --> ")
        start_time = start_timestamp.replace(",", ".")
        end_time = end_timestamp.replace(",", ".")

        clickable_start = f'<a href="#" data-time="{timestamp_to_seconds(start_timestamp)}" class="timestamp">{start_time}</a>'
        clickable_end = f'<a href="#" data-time="{timestamp_to_seconds(end_timestamp)}" class="timestamp">{end_time}</a>'
        html_output.append(f"{clickable_start} --> {clickable_end}")

        i += 1
        subtitles = []

        # Get the subtitles
        while i < len(lines) and lines[i] != "":
            subtitles.append(lines[i])
            i += 1

        # Add the subtitles to the output
        html_output.append("<br>".join(subtitles) + " <br>")

        i += 1

    return "\n".join(html_output)


def clean_subtitles(srt):
    lines = srt.strip().split("\n")
    subtitles = []

    i = 0
    while i < len(lines):
        # Skip the index
        i += 2
        # Get the subtitles
        while i < len(lines) and lines[i] != "":
            subtitles.append(lines[i])
            i += 1

        # Add the subtitles to the output
        i += 1
    return "\n".join(subtitles)


def embed_subtitles(srt):
    lines = srt.strip().split("\n")
    html_output = []

    i = 0
    while i < len(lines):
        # Skip the index
        i += 1

        # Split the timestamps and create clickable links for both start and end
        start_timestamp, end_timestamp = lines[i].split(" --> ")
        start_time = start_timestamp.replace(",", ".")

        i += 1
        subtitles = []

        # Get the subtitles
        while i < len(lines) and lines[i] != "":
            subtitles.append(lines[i])
            i += 1

        # Add the subtitles to the output

        html_output.append(
            '<div class="transcript-section">'
            + f'  <span>{" ".join(subtitles)}</span>'
            + f'  <span class="timestamp-jump" data-time="{timestamp_to_seconds(start_timestamp)}" timestamp="{start_time}"></span>'
            + "</div>"
        )
        i += 1

    return "\n".join(html_output)


# print(embed_subtitles(open("static/transcriptions/Why following your passion is terrible advice/Why following your passion is terrible advice.srt").read()))


def sanitize(file_name):
    # remove any invalid characters
    return urllib.parse.quote(
        "".join(c for c in file_name if c not in FORBIDDEN_FOLDER_CHARS)
    )


def summarise(text):
    if len(encoding.encode(text)) < 2048:
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are to return a summary of the user's input. Do not refer explicitly to the user's input, instead only return the summary.",
                },
                {"role": "user", "content": text},
            ],
        )["choices"][0]["message"]["content"]
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are to return a summary of the user's input. Do not refer explicitly to the user's input, instead only return the summary.",
            },
            {"role": "user", "content": text},
        ],
    )["choices"][0]["message"]["content"]


def main():
    pass


if __name__ == "__main__":
    main()
