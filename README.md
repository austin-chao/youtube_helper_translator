# Youtube Translator

This is an introductory project built to learn Langchain

## Description

This program enables you to chat with Youtube videos. Multi languages supported via OpenAI Wisper API (See supported languages here: "https://help.openai.com/en/articles/7031512-whisper-api-faq")

## Getting Started

![image](https://github.com/austin-chao/youtube_helper_translator/assets/44959004/91967912-f168-4a8c-8322-04be87c2c6a4)

Step 1: Enter the youtube URL  in the "What is the Youtube URL" textbox on the left.
Step 2: Enter your question about the video under "Ask a question about the video"
Step 3: Toggle "Is this in a foreign language" if you want the model to use audio instead of text transcript.
Step 4: Click submit on the top left.
Step 5: See the result displayed in the center.

### Known Bugs
* Using audio instead of transcript may give an error if the video is too long.
* Using audio downloads the video into the youtube_videos folder.
* Asking a question for a different youtube video in the same session may provide answers pertaining to a previous video. Restarting the application will fix this.  

### Dependencies

* Ubuntu-22.04, Docker, Bash, Python-3.11
* OpenAI key is required in the .env file in the format:
```
OPENAI_API_KEY=[ENTER KEY HERE]
```

### Executing program

* Open Docker and bash in your terminal
* Run the commands below
```
docker build -t ai-test-yt-assistant .
```
```
docker run -p 8501:8501 -v $(pwd):/the/workdir/path ai-test-yt-assistant
```
* Enter http://localhost:8501/ into your prefered browser

## Authors

Contributors names and contact info

Austin Chao
twitter.com/austin_chao1

## Version History

* 0.1
    * Initial Release

## Acknowledgments

Inspiration, code snippets, etc.
* [matiassingers](https://github.com/rishabkumar7/youtube-assistant-langchain))
* * The base program was built by matiassingers, his program has been modifiedto use gpt-3.5-turbo-instruct instead of text-davinci-003 and to allow audio-to-text if a transcript isn't available.
