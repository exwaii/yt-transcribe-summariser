# yt-transcribe-summariser

A project to transcribe and summarise audio files. Merge of my two older projects, one that was purely CLI ([here](https://github.com/exwaii/transcribe-summariser)) and one that implented a web UI for a school project ([here](https://github.com/exwaii/sdd-transcribe-summariser)).

## How to use

### Install dependencies with pip

Verify you have pip and git installed:

``` bash
$ pip -V 
pip 20.0.2
$ git -v
git version 2.39.2
$ git clone https://github.com/exwaii/sdd-transcribe-summariser
```

Alternatively, you can download the files manually.

The versions don't matter, just make sure you have pip installed.

Install the dependencies from `requirements.txt`:

``` bash
pip install -r requirements.txt
```

Create a `.env` file with your OPENAI_API_KEY and DISCORD_TOKEN for the discord bot.

You can now start the webserver with `python web.py`
