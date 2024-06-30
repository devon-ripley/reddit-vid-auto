import json


class Config:
    def __init__(self):
        self.client_id = 'ggffsssjjj'
        self.client_secret = 'jjjjhhhhhggg555'
        self.user_agent = 'reader'

        # story vars auto load
        self.number_of_posts = 1
        self.sub_reddits = ['relationship_advice']

        # comment vars
        self.number_of_comments = 15
        self.story_delim_audio = ''
        self.story_delim = '#'
        self.target_story = ['1dnt7ar', '1dnu3y3', '1dnkv2i']

        # vid vars
        self.start_delay = 10
        self.fps = 30
        self.resolution = (1920, 1080)
        self.resolution_back = (1920, 1080)
        self.vertical_resolution = (608, 1080)
        self.vertical_resolution_back = (608, 1080)
        self.font = 'Arial-Black'
        # Trebuchet-MS-Bold, Segoe-UI-Semibold 'to wide' , Arial-black is great, a little sharp
        self.text_size = 70
        self.text_color = 'white'
        self.stroke_color = 'black'
        self.stroke_size = 3.5
        self.align = 'center'
        self.tts_to_use = "gtts"

        # bad word list
        self.bad_words = {'SEXUAL': 'FUN TIME', 'LINGERIE': 'FUN CLOTHES'}


def setup():
    try:
        with open('config.json') as json_file:
            data = json.load(json_file)
        config = Config()
        config.client_id = data["client_id"]
        config.client_secret = data["client_secret"]
        config.user_agent = data["user_agent"]

        # story vars autoload
        config.number_of_posts = data["number_of_posts"]
        config.sub_reddits = data["sub_reddits"]

        # comment vars
        config.number_of_comments = data["number_of_comments"]
        config.story_delim_audio = data["story_delim_audio"]
        config.story_delim = data["story_delim"]
        config.target_story = data["target_story"]

        # vid vars
        config.start_delay = data["start_delay"]
        config.fps = data["fps"]
        config.resolution = data["resolution"]
        config.resolution_back = data["resolution_back"]
        config.vertical_resolution = data["vertical_resolution"]
        config.vertical_resolution_back = data["vertical_resolution_back"]
        config.font = data["font"]
        # Trebuchet-MS-Bold, Segoe-UI-Semibold 'to wide' , Arial-black is great, a little sharp
        config.text_size = data["text_size"]
        config.text_color = data["text_color"]
        config.stroke_color = data["stroke_color"]
        config.stroke_size = data["stroke_size"]
        config.align = data["align"]
        config.tts_to_use = data["tts_to_use"]

    except:
        print("No config.json file found, creating new one")
        config = Config()
        data = {}
        data["client_id"] = config.client_id
        data["client_secret"] = config.client_secret
        data["user_agent"] = config.user_agent

        # story vars auto load
        data["number_of_posts"] = config.number_of_posts
        data["sub_reddits"] = config.sub_reddits

        # comment vars
        data["number_of_comments"] = config.number_of_comments
        data["story_delim_audio"] = config.story_delim_audio
        data["story_delim"] = config.story_delim
        data["target_story"] = config.target_story

        # vid vars
        data["start_delay"] = config.start_delay
        data["fps"] = config.fps
        data["resolution"] = config.resolution
        data["resolution_back"] = config.resolution_back
        data["vertical_resolution"] = config.vertical_resolution
        data["vertical_resolution_back"] = config.vertical_resolution_back
        data["font"] = config.font
        # Trebuchet-MS-Bold, Segoe-UI-Semibold 'to wide' , Arial-black is great, a little sharp
        data["text_size"] = config.text_size
        data["text_color"] = config.text_color
        data["stroke_color"] = config.stroke_color
        data["stroke_size"] = config.stroke_size
        data["align"] = config.align
        data["tts_to_use"] = config.tts_to_use
        with open('config.json', "w") as outfile:
            json.dump(data, outfile, indent=3)
    return config
