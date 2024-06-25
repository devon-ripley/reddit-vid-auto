import os
import time

import torch
from TTS.api import TTS
import pyttsx3
from gtts import gTTS
from gradio_client import Client



def run_tts(stories):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS('tts_models/en/ljspeech/tacotron2-DDC_ph').to(device)
    for c, story in enumerate(stories):
        tts.tts_to_file(story['title'], file_path=f'data/audio/title_{story["sub"]}{c}.mp3')
        tts.tts_to_file(f'Story number {c + 1}', file_path=f'data/audio/story_card_{c}.mp3')
        for c2, line in enumerate(story['text']):
            tts.tts_to_file(line, file_path=f'data/audio/text_{story["sub"]}{c}_{c2}.mp3')


#def tts_tortoise_setup():
#    config = TortoiseConfig()
#    model = Tortoise.init_from_config(config)
#    model.load_checkpoint(config, checkpoint_dir="models/", eval=True)

# with random speaker
#    output_dict = model.synthesize('test', config, speaker_id="random", extra_voice_dirs=None)

def run_tts_tortoise(stories):
    tts = TTS("tts_models/en/multi-dataset/tortoise-v2")
    voice_dir = "models/voices/"
    speaker = "lj"
    preset = "ultra_fast"
    for c, story in enumerate(stories):
        tts.tts_to_file(text=story['title'],
                        file_path=f'data/audio/title_{story["sub"]}{c}.mp3',
                        voice_dir=voice_dir,
                        speaker=speaker,
                        preset=preset)
        tts.tts_to_file(text=f'Story number {c + 1}',
                        file_path=f'data/audio/story_card_{c}.mp3',
                        voice_dir=voice_dir,
                        speaker=speaker,
                        preset=preset)
        for c2, line in enumerate(story['text']):
            tts.tts_to_file(text=line,
                            file_path=f'data/audio/text_{story["sub"]}{c}_{c2}.mp3',
                            voice_dir=voice_dir,
                            speaker=speaker,
                            preset=preset)


def run_pytts(stories):
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
    slow = False
    for c, story in enumerate(stories):
        tts = gTTS(text=story['title'], lang='en', slow=slow)
        tts.save(f'data/audio/title_{story["sub"]}{c}.mp3')
        tts = gTTS(text=f'Story number {c + 1}', lang='en', slow=slow)
        tts.save(f'data/audio/story_card_{c}.mp3')
        for c2, line in enumerate(story['text']):
            print(f'Line: {line}')
            tts = gTTS(text=line, lang='en', slow=slow)
            tts.save(f'data/audio/text_{story["sub"]}{c}_{c2}.mp3')


def run_ai_clone(stories):
    #os.chdir('ai_voice_cloning')
    #os.system('start start.bat')
    #time.sleep(15)
    current_path = os.path.abspath(os.getcwd())
    samples = 25
    iterations = 50
    # run start.bat for ai_voice_cloning
    client = Client("http://127.0.0.1:7860/")
    voice = "jane_eyre"
    for c, story in enumerate(stories):
        result = client.predict(
            story['title'],
            "\n",
            "Happy",
            "I am happy",
            "jane_eyre",
            None,
            3,  # float in 'Voice Chunks' Number component
            1,  # float (numeric value between 1 and 6)
            3,  # float in 'Seed' Number component
            samples,  # float (numeric value between 2 and 512) in 'Samples'
            iterations,  # float (numeric value between 0 and 512) in 'Iterations'
            0.2,  # float (numeric value between 0 and 1) in 'Temperature'
            "DDIM",  # Literal['P', 'DDIM'] in 'Diffusion Samplers' Radio component
            8,  # float (numeric value between 1 and 32) in 'Pause Size'
            0,  # float (numeric value between 0 and 1) in 'CVVP Weight'
            0.8,  # float (numeric value between 0 and 1) in 'Top P'
            1,  # float (numeric value between 0 and 1) in 'Diffusion Temperature'
            1,  # float (numeric value between 0 and 8) in 'Length Penalty'
            2,  # float (numeric value between 0 and 8) in 'Repetition Penalty'
            2,  # float (numeric value between 0 and 4) in 'Conditioning-Free K'
            ["Conditioning-Free"],
            # List[Literal['Half Precision', 'Conditioning-Free']] in 'Experimental Flags' Checkboxgroup component
            False,  # bool in 'Use Original Latents Method (AR)' Checkbox component
            False,  # bool in 'Use Original Latents Method (Diffusion)' Checkbox component
            api_name="/generate"
        )
        print(result[2]['choices'][0][0][22:])
        command = f'copy {current_path}\\ai_voice_cloning\\results\\jane_eyre\\{result[2]["choices"][0][0][22:]} {current_path}\\data\\audio\\title_{story["sub"]}{c}.wav'
        print(command)
        os.system(command)
        # save it!!!
        #tts.save(f'data/audio/title_{story["sub"]}{c}.mp3')

        result = client.predict(
            f'Story number {c + 1}',
            "\n",
            "Happy",
            "I am happy",
            "jane_eyre",
            None,
            3,  # float in 'Voice Chunks' Number component
            1,  # float (numeric value between 1 and 6)
            3,  # float in 'Seed' Number component
            16,  # float (numeric value between 2 and 512) in 'Samples'
            30,  # float (numeric value between 0 and 512) in 'Iterations'
            0.2,  # float (numeric value between 0 and 1) in 'Temperature'
            "DDIM",  # Literal['P', 'DDIM'] in 'Diffusion Samplers' Radio component
            8,  # float (numeric value between 1 and 32) in 'Pause Size'
            0,  # float (numeric value between 0 and 1) in 'CVVP Weight'
            0.8,  # float (numeric value between 0 and 1) in 'Top P'
            1,  # float (numeric value between 0 and 1) in 'Diffusion Temperature'
            1,  # float (numeric value between 0 and 8) in 'Length Penalty'
            2,  # float (numeric value between 0 and 8) in 'Repetition Penalty'
            2,  # float (numeric value between 0 and 4) in 'Conditioning-Free K'
            ["Conditioning-Free"],
            # List[Literal['Half Precision', 'Conditioning-Free']] in 'Experimental Flags' Checkboxgroup component
            False,  # bool in 'Use Original Latents Method (AR)' Checkbox component
            False,  # bool in 'Use Original Latents Method (Diffusion)' Checkbox component
            api_name="/generate"
        )
        print(result[2]['choices'][0][0])
        os.system(f'copy {current_path}\\ai_voice_cloning\\results\\jane_eyre\\{result[2]["choices"][0][0][22:]} {current_path}\\data\\audio\\story_card_{c}.wav')
        #save it!!
        #tts.save(f'data/audio/story_card_{c}.mp3')
        for c2, line in enumerate(story['text']):
            print(f'Line: {line}')
            result = client.predict(
                line,
                "\n",
                "Happy",
                "I am happy",
                "jane_eyre",
                None,
                3,  # float in 'Voice Chunks' Number component
                1,  # float (numeric value between 1 and 6)
                3,  # float in 'Seed' Number component
                16,  # float (numeric value between 2 and 512) in 'Samples'
                30,  # float (numeric value between 0 and 512) in 'Iterations'
                0.2,  # float (numeric value between 0 and 1) in 'Temperature'
                "DDIM",  # Literal['P', 'DDIM'] in 'Diffusion Samplers' Radio component
                8,  # float (numeric value between 1 and 32) in 'Pause Size'
                0,  # float (numeric value between 0 and 1) in 'CVVP Weight'
                0.8,  # float (numeric value between 0 and 1) in 'Top P'
                1,  # float (numeric value between 0 and 1) in 'Diffusion Temperature'
                1,  # float (numeric value between 0 and 8) in 'Length Penalty'
                2,  # float (numeric value between 0 and 8) in 'Repetition Penalty'
                2,  # float (numeric value between 0 and 4) in 'Conditioning-Free K'
                ["Conditioning-Free"],
                # List[Literal['Half Precision', 'Conditioning-Free']] in 'Experimental Flags' Checkboxgroup component
                False,  # bool in 'Use Original Latents Method (AR)' Checkbox component
                False,  # bool in 'Use Original Latents Method (Diffusion)' Checkbox component
                api_name="/generate"
            )
            #tts.save(f'data/audio/text_{story["sub"]}{c}_{c2}.mp3')
            print(result[2]['choices'][0][0])
            os.system(f'copy {current_path}\\ai_voice_cloning\\results\\jane_eyre\\{result[2]["choices"][0][0][22:]} {current_path}\\data\\audio\\text_{story["sub"]}{c}_{c2}.wav')
            #saveit!!
    client.close()

def run_ai_clone_2(stories):
    import ai_voice_cloning.src.utils as ai_voice
    for c, story in enumerate(stories):
        kwargs = {
            'text': story['title'],
            'delimiter': "\n",
            'emotion': "happy",
            'prompt': "i am happy",
            'voice': "jane_eyre",
            'mic_audio': None,
            'voice_latents_chunks': 3,
            'candidates': 1,
            'seed': 3,
            'num_autoregressive_samples': 16,
            'diffusion_iterations': 30,
            'temperature': 0.2,
            'diffusion_sampler': "DDIM",
            'breathing_room': 8,
            'cvvp_weight': 0,
            'top_p': 0.8,
            'diffusion_temperature': 1,
            'length_penalty': 1,
            'repetition_penalty': 2,
            'cond_free_k': 2,
            'experimentals': "Conditioning-Free",
            'filepath': f'data/audio/title_{story["sub"]}{c}.wav'
        }
        ai_voice.generate_tortoise(kwargs)

        kwargs = {
            'text': f'Story number {c + 1}',
            'delimiter': "\n",
            'emotion': "happy",
            'prompt': "i am happy",
            'voice': "jane_eyre",
            'mic_audio': None,
            'voice_latents_chunks': 3,
            'candidates': 1,
            'seed': 3,
            'num_autoregressive_samples': 16,
            'diffusion_iterations': 30,
            'temperature': 0.2,
            'diffusion_sampler': "DDIM",
            'breathing_room': 8,
            'cvvp_weight': 0,
            'top_p': 0.8,
            'diffusion_temperature': 1,
            'length_penalty': 1,
            'repetition_penalty': 2,
            'cond_free_k': 2,
            'experimentals': "Conditioning-Free",
            'filepath': f'data/audio/story_card_{c}.wav'
        }
        ai_voice.generate_tortoise(kwargs)

        for c2, line in enumerate(story['text']):
            print(f'Line: {line}')

            kwargs = {
                'text': line,
                'delimiter': "\n",
                'emotion': "happy",
                'prompt': "i am happy",
                'voice': "jane_eyre",
                'mic_audio': None,
                'voice_latents_chunks': 3,
                'candidates': 1,
                'seed': 3,
                'num_autoregressive_samples': 16,
                'diffusion_iterations': 30,
                'temperature': 0.2,
                'diffusion_sampler': "DDIM",
                'breathing_room': 8,
                'cvvp_weight': 0,
                'top_p': 0.8,
                'diffusion_temperature': 1,
                'length_penalty': 1,
                'repetition_penalty': 2,
                'cond_free_k': 2,
                'experimentals': "Conditioning-Free",
                'filepath': f'data/audio/text_{story["sub"]}{c}_{c2}.wav'
            }
            ai_voice.generate_tortoise(kwargs)
