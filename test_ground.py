import config
import moviepy
from moviepy.editor import *
#import torch
#from TTS.api import TTS


def text_testing():
    txt_clip = TextClip(txt='THIS IS JUST A TEST. HOPEFULLY THESE VIDEOS ARE GOOD! WHY IS NOTHING HAPPENING', fontsize=config.text_size, color=config.text_color, method='caption',
                        stroke_color=config.stroke_color, align=config.align, font=config.font,
                        size=config.resolution, stroke_width=config.stroke_size).set_duration(5)
    background_video = VideoFileClip(f'input_vid/test.mp4')
    back_clip = background_video.subclip(20, 25)
    cores = os.cpu_count() - 1
    final_vid = CompositeVideoClip([back_clip, txt_clip])
    final_vid.write_videofile(f'output/text_test_bigg.mp4', threads=cores, fps=config.fps)

def text_list():
    print(TextClip.list('font'))


def audio_test():
    # tts --list_models
    model_list = ['tts_models/en/ek1/tacotron2',
                  'tts_models/en/ljspeech/tacotron2-DDC',
                  'tts_models/en/ljspeech/tacotron2-DDC_ph',
                  'tts_models/en/ljspeech/glow-tts',
                  'tts_models/en/ljspeech/speedy-speech',
                  'tts_models/en/ljspeech/tacotron2-DCA',
                  'tts_models/en/ljspeech/vits',
                  'tts_models/en/ljspeech/vits--neon',
                  'tts_models/en/ljspeech/fast_pitch',
                  'tts_models/en/ljspeech/overflow',
                  'tts_models/en/ljspeech/neural_hmm',
                  'tts_models/en/vctk/vits',
                  'tts_models/en/vctk/fast_pitch',
                  'tts_models/en/sam/tacotron-DDC',
                  'tts_models/en/blizzard2013/capacitron-t2-c50',
                  'tts_models/en/blizzard2013/capacitron-t2-c150_v2',
                  'tts_models/en/multi-dataset/tortoise-v2',
                  'tts_models/en/jenny/jenny']

    device = "cuda" if torch.cuda.is_available() else "cpu"
    for c, model in enumerate(model_list):
        try:
            tts = TTS(model).to(device)
            tts.tts_to_file('This is just a test. Hopefully these voices are good!',
                            file_path=f'data/audio_test{c}.mp3')
        except:
            print(f'error with model, {model}')
            continue


text_list()
text_testing()
#audio_test()
