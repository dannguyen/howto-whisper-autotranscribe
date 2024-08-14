# How to use Whisper AI for auto transcription in August 2024


## Todos

- write installation steps for WSL2
- write installation for macOS
- how to install ffmpeg, yt-dlp, etc
- instructions how to authenticate with HuggingFace
- which segmentation model does insanely-fast use?
- can whisper-large-v3 model be downloaded and cached locally?
- diatrization kind of fails with fauci-rodrigo example; doesn't catch off-camera producer at 0:02:29.5
- polish prettify_ifw_output.py
    - wrangling is pretty much done

## References

- Diarization: https://huggingface.co/pyannote/speaker-diarization-3.1
- ASR: https://huggingface.co/openai/whisper-large-v3
- https://github.com/Vaibhavs10/insanely-fast-whisper


## End to end example

```sh


insanely-fast-whisper \
    --hf-token=$HUGGINGFACE_ACCESS_TOKEN \
    --model openai/whisper-large-v3 \
    --batch-size 4 \
    --num-speakers 3 \
    --timestamp word \
    --file-name ./data/videos/fauci-rodrigo-read-tweets.mp4 \
    --transcript-path ./data/transcripts/fauci-rodrigo-read-tweets.raw.json

./prettify_ifw_output.py \
    -i data/transcripts/fauci-rodrigo-read-tweets.raw.json \
    -o data/transcripts/fauci-rodrigo-read-tweets.pretty.csv
```


## Various how-tos


-------------------------------------

### yt-dlp to download videos


```sh 
# Trump news conference about covid
yt-dlp -f mp4 \
    --write-subs --write-auto-subs \
    -o trump-presser-2020-09-10.mp4 \
    https://www.youtube.com/watch?v=Fjwmssidlbo 

# Dr Fauci and Olivia Rodrigo read covid/vaccine tweets
yt-dlp -f mp4 \
    --write-subs --write-auto-subs \
    -o fauci-rodrigo-read-tweets.mp4 \
    https://www.youtube.com/watch?v=o8sHSEtH3L4

yt-dlp -f mp4 \
    --write-subs \
    --write-auto-subs \
    -o biden-reclassify-marijuana.mp4 \
    https://www.youtube.com/watch?v=tDWWZ1zGNwg
```

### ffmpeg for encoding tasks

Sometimes you'll get an error about a malformed audio file (insanely-fast-whisper); see [issue/comment here](https://github.com/Vaibhavs10/insanely-fast-whisper/issues/90#issuecomment-2157880588). Use `movflags faststart` to fix the metadata

```sh
ffmpeg -y -i /tmp/xsample.mp4 \
    -movflags faststart \
    -ss 00:00:01.780 \
    -to 00:02:43.640 \
    /tmp/xsample-output.mp4
```


Changing bitrate, quality, etc:

```sh
ffmpeg -y -i /tmp/xsample.webm \
    -movflags faststart \
    -ss 00:10:10 \
    -t 00:05:00.500 \
    -c:v libx264 -crf 28 \
    -c:a aac -b:a 192k -ar 44100 \
    /tmp/xsample-output.mp4
```
