class Config:
    def __init__(self):
        self.client_id = 'ggffsssjjj'
        self.client_secret = 'jjjjhhhhhggg555'
        self.user_agent = 'reader'

        #story vars auto load
        self.number_of_posts = 1
        self.sub_reddits = ['relationship_advice']

        # comment vars
        self.number_of_comments = 15
        self.story_delim_audio = ''
        self.story_delim = '#'
        self.target_story = ['1dnt7ar', '1dnu3y3', '1dnkv2i']


        #vid vars
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
