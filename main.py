# TODO: target comment, add logging lmao, auto config.json setup, thumbnail creation on side?

import datetime
import re
import praw
import base_config
from praw.models import MoreComments
from pydub import AudioSegment
import moviepy
from moviepy.editor import *
import pathlib
import os
import json
import logging
import text_speech_handler

home_path = pathlib.Path().resolve()

# load config
config = base_config.setup()

class StoryGetter:
    def __init__(self, grab='story', vid_path='test.mp4', vid_save_path='untitled.mp4', sub_id=None, story_target=False,
                 vertical=False, comment_target=False):
        self.stories = []
        self.reddit = 0
        self.grab = grab
        self.vid_path = vid_path
        self.vid_save_path = vid_save_path
        self.sub_id = sub_id
        self.story_target = story_target
        self.vertical = vertical
        self.comment_target = comment_target
        self.sentence_break_flags = []

    def bot_login(self):
        print('logging into reddit API')
        reddit_login = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent
        )
        self.reddit = reddit_login

    def bot_run(self):
        # error handling
        if self.story_target is True and self.grab != 'story':
            print('error: story target does not match grab!')
            exit()
        if self.story_target:
            if self.sub_id is not None:
                print('sub_id is not none')
                target_list = [self.sub_id]
            else:
                target_list = config.target_story
            for sub_id in target_list:
                print('go')
                submission = self.reddit.submission(sub_id)
                subreddit = submission.subreddit
                self.stories.append(
                    {'sub': subreddit.display_name, 'title': submission.title, 'text': submission.selftext,
                     'id': submission.id})
            return
        if self.grab == 'story':
            print('gathering text from reddit, story')
            for subreddit in config.sub_reddits:
                counter = 0
                for submission in self.reddit.subreddit(subreddit).hot(limit=10):
                    if counter == config.number_of_posts:
                        break
                    if submission.stickied:
                        continue
                    else:
                        self.stories.append(
                            {'sub': subreddit.display_name, 'title': submission.title, 'text': submission.selftext,
                             'id': submission.id})
                        counter += 1
        else:
            print('gathering text from reddit, comments')
            submission = self.reddit.submission(self.sub_id)
            counter = 0
            for top_level_comment in submission.comments:
                if counter >= config.number_of_comments:
                    break
                #if top_level_comment.stickied:
                #    continue
                if isinstance(top_level_comment, MoreComments):
                    continue
                else:
                    self.stories.append({'sub': self.sub_id, 'title': submission.title, 'text': top_level_comment.body,
                                         'id': submission.id})
                    counter += 1

    def save_story(self):
        current = datetime.datetime.now()
        dt = current.strftime("%d_%m_%y")
        filepath = f"data/saved_stories/{dt}_{self.stories[0]['sub']}.json"
        print(self.stories)
        with open(filepath, "w") as outfile:
            json.dump(self.stories, outfile, indent=3)

    def non_api_story(self, filepath):
        print('getting non api json file')
        # get stories from file in data, json
        with open(filepath) as json_file:
            data = json.load(json_file)
        print(data)
        self.stories = data

    def parse(self, bad_word, text):
        text = text.upper()
        check = True
        while check:
            search_result = re.search(bad_word, text)
            if search_result is None:
                break
            else:
                text_first = text[:search_result.span()[0]]
                text_second = text[search_result.span()[1]:]
                replacement = config.bad_words[bad_word]
                text = text_first + replacement + text_second
        return text

    def profanity_filter(self):
        print('filtering profanity')
        word_dict = config.bad_words
        word_dict = {'t': 't'}
        edited = []
        for story in self.stories:
            # parse title and text
            story_title = story['title']
            story_text = story['text']
            story_id = story['id']
            for bad_word in word_dict.keys():
                title = self.parse(bad_word, story_title, config)
                text = self.parse(bad_word, story_text, config)
                story_title = title
                story_text = text
            edited.append({'sub': story['sub'], 'title': story_title, 'text': story_text, 'id': story_id})
        self.stories = edited

    def sentence_splitter(self):
        print('spliting sentances')

        def split_into_sentences(text: str) -> list[str]:
            text = " " + text + "  "
            text = text.replace("\n", " ")
            text = re.sub(prefixes, "\\1<prd>", text)
            text = re.sub(websites, "<prd>\\1", text)
            text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
            text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
            if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
            text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
            text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
            text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
            text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
            text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
            text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
            text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
            if "”" in text: text = text.replace(".”", "”.")
            if "\"" in text: text = text.replace(".\"", "\".")
            if "!" in text: text = text.replace("!\"", "\"!")
            if "?" in text: text = text.replace("?\"", "\"?")
            text = text.replace(".", ".<stop>")
            text = text.replace("?", "?<stop>")
            text = text.replace("!", "!<stop>")
            text = text.replace("<prd>", ".")
            sentences = text.split("<stop>")
            sentences = [s.strip() for s in sentences]
            if sentences and not sentences[-1]: sentences = sentences[:-1]
            return sentences

        alphabets = "([A-Za-z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov|edu|me)"
        digits = "([0-9])"
        multiple_dots = r'\.{2,}'

        for c, story in enumerate(self.stories):
            new = split_into_sentences(story['text'])
            self.stories[c]['text'] = new

    def long_sentence_split(self):
        # 80max
        print('long sentence splitup')
        for c, story in enumerate(self.stories):
            self.sentence_break_flags.append([])
            for c2, line in enumerate(self.stories[c]['text']):
                self.sentence_break_flags[c].append(False)
                if len(line) == 1:
                    del self.stories[c]['text'][c2]
                if len(line) > 80:
                    no_add = False
                    ind = 80
                    breaker = False
                    for c3, char in enumerate(line):
                        if c3 > 80:
                            if char == ' ' or char == '.' or char == '?' or char == '!':
                                print(f'activate {char}')
                                # break sentence
                                self.sentence_break_flags[c][c2] = True
                                first = line[:c3] + '.'
                                last = line[c3:]
                                self.stories[c]['text'][c2] = first
                                self.stories[c]['text'].insert(c2 + 1, last)
                                break
        print(self.stories)
        #while breaker or line[ind] != ' ':
        #    if line[ind] == '.' or line[ind] == '?' or line[ind] == '!':
        #        no_add = True
        #        break
        #    if ind < len(line):
        #        ind += 1
        #    if ind == len(line) - 1:
        #        break
        #if breaker:
        #    break
        # add to sentence flags
        #if no_add is False:
        #    self.sentence_break_flags[c][c2] = True
        #    first = line[:ind] + '.'
        #    last = line[ind:]
        #    self.stories[c]['text'][c2] = first
        #    self.stories[c]['text'].insert(c2 + 1, last)
        #else:
        #self.sentence_break_flags[c][c2] = False

    def bad_char_removal(self):
        # * error
        print('bad_char_removal')
        for c, story in enumerate(self.stories):
            for c2, line in enumerate(story['text']):
                if c2 > 1:
                    print(f"after: {story['text'][c2 - 1]}")
                print(f'before: {line}')
                for c3, char in enumerate(line):
                    # 32-34, 46, 48-57, 63, 65-90
                    ok_list = [32, 33, 34, 46, 63]
                    ascii_value = ord(char)
                    if len(line) == 1:
                        self.stories[c]['text'].pop(c2)
                    if ascii_value in ok_list:
                        pass
                    elif ascii_value in range(48, 58):
                        pass
                    elif ascii_value in range(65, 91):
                        pass
                    else:
                        if c3 == 0:
                            #cut = self.stories[c]['text'][c2][]
                            pass
                        else:
                            first = self.stories[c]['text'][c2][:c3]
                            last = self.stories[c]['text'][c2][c3 + 1:]
                            total = first + last
                            self.stories[c]['text'][c2] = total

    def text2speach(self):
        print('creating text to speach')
        match config.tts_to_use:
            case "gtts":
                text_speech_handler.run_gtts(self.stories)
            case "tts":
                text_speech_handler.run_tts(self.stories)
            case "pytts":
                text_speech_handler.run_pytts(self.stories)
            case "ai_clone":
                text_speech_handler.run_ai_clone(self.stories)

    def total_time(self):
        audio_duration = 0
        ai_voice_clone = False
        for c, story in enumerate(self.stories):
            text_list = story['text']
            print(f'text list len: {len(text_list)}')
            if ai_voice_clone:
                AudioSegment.from_wav(f'data/audio/title_{story["sub"]}{c}.wav').export(
                    f'data/audio/title_{story["sub"]}{c}.mp3', format="mp3")
                AudioSegment.from_wav(f'data/audio/story_card_{c}.wav').export(
                    f'data/audio/story_card_{c}.mp3', format="mp3")
            sub = story['sub']
            for c2, line in enumerate(text_list):
                if ai_voice_clone:
                    AudioSegment.from_wav(f'data/audio/text_{sub}{c}_{c2}.wav').export(
                        f'data/audio/text_{sub}{c}_{c2}.mp3', format="mp3")
                audio_path = f'{home_path}/data/audio/text_{sub}{c}_{c2}.mp3'
                audio = AudioSegment.from_file(audio_path)
                audio_duration += audio.duration_seconds
        in_mins = (audio_duration + (len(self.stories) * 12)) / 60
        print(f'Total Source Video length needed{in_mins}')

    def title_clip_gen(self, sub, c, title, grab, vertical, config):
        if vertical:
            split_card = TextClip(txt=f'{config.story_delim}{c + 1}', fontsize=config.text_size,
                                  color=config.text_color,
                                  method='caption',
                                  stroke_color=config.stroke_color, align=config.align, font=config.font,
                                  size=config.vertical_resolution, stroke_width=config.stroke_size).set_duration(2)
            # find length of title audio
            audio = AudioSegment.from_file(f"{home_path}/data/audio/title_{sub}{c}.mp3")
            audio_card = AudioSegment.from_file(f"{home_path}/data/audio/story_card_{c}.mp3")
            title_duration = audio.duration_seconds
            title_clip = TextClip(txt=title, fontsize=config.text_size, color=config.text_color, method='caption',
                                  stroke_color=config.stroke_color, align=config.align, font=config.font,
                                  size=config.vertical_resolution, stroke_width=config.stroke_size).set_duration(
                title_duration)

        else:
            split_card = TextClip(txt=f'{config.story_delim}{c + 1}', fontsize=config.text_size,
                                  color=config.text_color,
                                  method='caption',
                                  stroke_color=config.stroke_color, align=config.align, font=config.font,
                                  size=config.resolution, stroke_width=config.stroke_size).set_duration(2)
            # find length of title audio
            audio = AudioSegment.from_file(f"{home_path}/data/audio/title_{sub}{c}.mp3")
            audio_card = AudioSegment.from_file(f"{home_path}/data/audio/story_card_{c}.mp3")
            title_duration = audio.duration_seconds
            title_clip = TextClip(txt=title, fontsize=config.text_size, color=config.text_color, method='caption',
                                  stroke_color=config.stroke_color, align=config.align, font=config.font,
                                  size=config.resolution, stroke_width=config.stroke_size).set_duration(
                title_duration)
        title_audio_clip = AudioFileClip(f"{home_path}/data/audio/title_{sub}{c}.mp3")
        title_new_audioclip = CompositeAudioClip([title_audio_clip])
        title_clip.audio = title_new_audioclip
        if grab == 'story':
            title_clip = concatenate_videoclips([split_card, title_clip], method='compose')
        else:
            title_clip = concatenate_videoclips([title_clip, split_card], method='compose')
        # add text and audio for title
        seg_duration = [title_duration + 2]
        txt_clip_list = [title_clip]
        return seg_duration, txt_clip_list

    def video_modification(self):
        main_clip_list = []
        total_duration = []
        first = True
        for c, story in enumerate(self.stories):
            title = story['title']
            text_list = story['text']
            sub = story['sub']
            if self.grab == 'story':
                seg_duration, txt_clip_list = self.title_clip_gen(sub, c, title, self.grab, self.vertical)
            else:
                if first:
                    seg_duration, txt_clip_list = self.title_clip_gen(sub, c, title, self.grab, self.vertical)
                    first = False
                else:
                    if self.vertical:
                        split_card = TextClip(txt=f'{config.story_delim}{c + 1}', fontsize=config.text_size,
                                              color=config.text_color,
                                              method='caption',
                                              stroke_color=config.stroke_color, align=config.align, font=config.font,
                                              size=config.vertical_resolution,
                                              stroke_width=config.stroke_size).set_duration(2)
                    else:
                        split_card = TextClip(txt=f'{config.story_delim}{c + 1}', fontsize=config.text_size,
                                              color=config.text_color,
                                              method='caption',
                                              stroke_color=config.stroke_color, align=config.align, font=config.font,
                                              size=config.resolution, stroke_width=config.stroke_size).set_duration(2)
                    seg_duration = [2]
                    txt_clip_list = [split_card]
            print('creating text and audio clips')
            for c2, line in enumerate(text_list):
                print(f'Clip number: {c2}')
                audio_path = f'{home_path}/data/audio/text_{sub}{c}_{c2}.mp3'

                audio = AudioSegment.from_file(audio_path)
                audio_duration = audio.duration_seconds
                seg_duration.append(audio_duration)
                if not self.sentence_break_flags:
                    pass
                else:
                    if self.sentence_break_flags[c][c2]:
                        line = line[:-1]
                        #knock . off end of line
                # add text and audio together
                if self.vertical:
                    txt_clip = TextClip(txt=line, fontsize=config.text_size, color=config.text_color, method='caption',
                                        stroke_color=config.stroke_color, align=config.align, font=config.font,
                                        size=config.vertical_resolution, stroke_width=config.stroke_size).set_duration(
                        audio_duration)
                else:
                    txt_clip = TextClip(txt=line, fontsize=config.text_size, color=config.text_color,
                                        method='caption',
                                        stroke_color=config.stroke_color, align=config.align, font=config.font,
                                        size=config.resolution, stroke_width=config.stroke_size).set_duration(
                        audio_duration)
                audio_clip = AudioFileClip(audio_path)
                new_audioclip = CompositeAudioClip([audio_clip])
                txt_clip.audio = new_audioclip
                txt_clip_list.append(txt_clip)
            total_duration.append(sum(seg_duration))
            complete_txt_clips = concatenate_videoclips(txt_clip_list, method="compose")
            main_clip_list.append(complete_txt_clips)

        # save final video
        background_video = VideoFileClip(f'{self.vid_path}')
        # crop background if vertical is true
        if self.vertical:
            background_video = moviepy.video.fx.all.crop(background_video, width=config.vertical_resolution_back[0],
                                                         height=config.vertical_resolution_back[1], x1=650)
        total_time = round(sum(total_duration)) + 1 + config.start_delay
        print(total_time)
        back_clip = background_video.subclip(config.start_delay, total_time)
        final_txt_video = concatenate_videoclips(main_clip_list, method="compose")
        cores = os.cpu_count() - 1
        final_vid = CompositeVideoClip([back_clip, final_txt_video])
        final_vid.write_videofile(f'{self.vid_save_path}', threads=cores, fps=config.fps)
        background_video.close()
        print('Video saved!')

    def cleanup(self):
        try:
            os.chdir('audio')
        except:
            exit(1)
        os.system('del *')


def save_story(grab, sub_id, story_target):
    story_obj = StoryGetter(grab=grab, sub_id=sub_id, story_target=story_target)
    story_obj.bot_login()
    story_obj.bot_run()
    #story_obj.profanity_filter()
    story_obj.sentence_splitter()
    story_obj.long_sentence_split()
    story_obj.save_story()


def vid_auto(grab, vid_path, vid_save_path, sub_id, story_target, vertical, comment_target, non_api=None):
    # get text from reddit, story or comment
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, handlers=[
        logging.FileHandler("logs/debug.log"),
        logging.StreamHandler()
    ])
    story_obj = StoryGetter(grab, vid_path, vid_save_path, sub_id, story_target, vertical,
                            comment_target)
    #alt
    if non_api is not None:
        story_obj.non_api_story(non_api)
        # create speach files
        story_obj.text2speach()
        story_obj.total_time()
        # create and save video
        story_obj.video_modification()
        # story_obj.cleanup()
        exit()
    else:
        story_obj.bot_login()
        story_obj.bot_run()
    # text manipulation
    #story_obj.profanity_filter()
    story_obj.sentence_splitter()
    story_obj.long_sentence_split()
    #story_obj.bad_char_removal()
    # create speach files
    story_obj.text2speach()
    story_obj.total_time()
    # create and save video
    story_obj.video_modification()
    # story_obj.cleanup()


if __name__ == '__main__':
    #vid_auto(vid_path='input_vid/big_test.mp4', grab='comment', vid_save_path='output/final_comment.mp4', sub_id='1dra11o', story_target=False, vertical=False, comment_target=False, non_api=None)
    vid_auto(vid_path='input_vid/2.mp4', grab='comment', vid_save_path='output/comment_test.mp4', sub_id=None,
             story_target=False, vertical=False, comment_target=False,
             non_api='data/saved_stories/29_06_24_1dra11o.json')
    #save_story(grab='comment', sub_id='1dra11o', story_target=False)
    #text_speech_handler.tts_tortoise_setup()
    # 'C:\Users\derip\PycharmProjects\reddit_vid_auto\data\saved_stories\saved_test.json'
