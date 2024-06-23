import torch
from TTS.api import TTS
import pyttsx3
from gtts import gTTS


def tts_run(stories):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS('tts_models/en/ljspeech/tacotron2-DDC_ph').to(device)
    for c, story in enumerate(stories):
        tts.tts_to_file(story['title'], file_path=f'data/audio/title_{story["sub"]}{c}.mp3')
        tts.tts_to_file(f'Story number {c + 1}', file_path=f'data/audio/story_card_{c}.mp3')
        for c2, line in enumerate(story['text']):
            tts.tts_to_file(line, file_path=f'data/audio/text_{story["sub"]}{c}_{c2}.mp3')


def pytts_run(stories):
    engine = pyttsx3.init()
    for c, story in enumerate(stories):
        engine.save_to_file(story['title'], f'data/audio/title_{story["sub"]}{c}.mp3')
        engine.runAndWait()
        engine.save_to_file(f'Story number {c + 1}', f'data/audio/story_card_{c}.mp3')
        engine.runAndWait()
        for c2, line in enumerate(story['text']):
            engine.save_to_file(line, f'data/audio/text_{story["sub"]}{c}_{c2}.mp3')
            engine.runAndWait()


def run_gtts(stories):
    slow = True
    for c, story in enumerate(stories):
        tts = gTTS(text=story['title'], lang='en', slow=slow)
        tts.save(f'data/audio/title_{story["sub"]}{c}.mp3')
        tts = gTTS(text=f'Story number {c + 1}', lang='en', slow=slow)
        tts.save(f'data/audio/story_card_{c}.mp3')
        for c2, line in enumerate(story['text']):
            print(f'Line: {line}')
            tts = gTTS(text=line, lang='en', slow=slow)
            tts.save(f'data/audio/text_{story["sub"]}{c}_{c2}.mp3')
