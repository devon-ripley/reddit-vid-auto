import base_config
import gradio as gr
import json

with open('config.json') as json_file:
    data = json.load(json_file)
config = base_config.Config()
config.client_id = data["client_id"]
config.client_secret = data["client_secret"]
config.user_agent = data["user_agent"]

# story vars auto load
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

def save_story(grab, sub_id, story_target):
    import main
    main.save_story(grab, sub_id, story_target)
    return "story saved"


def config_edit(client_id, client_secret, user_agent, number_of_posts, sub_reddits, number_of_comments,
                story_delim_audio, story_delim, target_story, start_delay,
                fps, resolution, resolution_back, vertical_resolution, vertical_resolution_back, font, text_size,
                text_color, stroke_color, stroke_size, align):
    data = {}
    data["client_id"] = client_id
    data["client_secret"] = client_secret
    data["user_agent"] = user_agent

    # story vars auto load
    data["number_of_posts"] = number_of_posts
    data["sub_reddits"] = sub_reddits

    # comment vars
    data["number_of_comments"] = number_of_comments
    data["story_delim_audio"] = story_delim_audio
    data["story_delim"] = story_delim
    data["target_story"] = target_story

    # vid vars
    data["start_delay"] = start_delay
    data["fps"] = fps
    data["resolution"] = resolution
    data["resolution_back"] = resolution_back
    data["vertical_resolution"] = vertical_resolution
    data["vertical_resolution_back"] = vertical_resolution_back
    data["font"] = font
    # Trebuchet-MS-Bold, Segoe-UI-Semibold 'to wide' , Arial-black is great, a little sharp
    data["text_size"] = text_size
    data["text_color"] = text_color
    data["stroke_color"] = stroke_color
    data["stroke_size"] = stroke_size
    data["align"] = align
    with open('config.json', "w") as outfile:
        json.dump(data, outfile, indent=3)
    return "config file updated"

def run_vid_auto(grab, vid_path, vid_save_path, story_target, vertical, comment_target, sub_id,
                 non_api):
    import main
    main.vid_auto(grab, vid_path, vid_save_path, sub_id, story_target, vertical, comment_target, non_api, config)
    return f"Video saved {vid_save_path}"


run_main = gr.Interface(
    fn=run_vid_auto,
    inputs=[
        gr.Dropdown(["story", "comment"], label="Video type"),
        gr.Textbox(label="Input video path", value="input_vid/", info="Must be .mp4"),
        gr.Textbox(label="Output video path", value="output/", info="Must be .mp4"),
        gr.Checkbox(label="target story", info="uses story targets from config, if checked sub id and non api must be blank"),
        gr.Checkbox(label="vertical"),
        gr.Checkbox(label="comment not working!")
    ],
    additional_inputs=[
        gr.Textbox(label="sub_id", info='only use for single targeted submission'),
        gr.File(label="Non_api")
    ],
    outputs=["text"],
allow_flagging="never"
)

run_save_story = gr.Interface(
    fn=save_story,
    inputs=[
        gr.Dropdown(["story", "comment"], label="Story type"),
        gr.Textbox(label="sub ID"),
        gr.Checkbox(label="target story", info="uses story targets from config, if checked sub id must be blank")
    ],
    outputs=["text"],
allow_flagging="never"
)

run_config_edit = gr.Interface(
    fn=config_edit,
    inputs=[
        gr.Textbox(label="client_id", value=config.client_id),
        gr.Textbox(label="client_secret", value=config.client_secret),
        gr.Textbox(label="user_agent", value=config.user_agent),
        gr.Textbox(label="number_of_posts", value=config.number_of_posts),
        gr.Textbox(label="sub_reddits", value=config.sub_reddits),
        gr.Textbox(label="number_of_comments", value=config.number_of_comments),
        gr.Textbox(label="story_delim_audio", value=config.story_delim_audio),
        gr.Textbox(label="story_delim", value=config.story_delim),
        gr.Textbox(label="story targets", value=config.target_story),
        gr.Textbox(label="start_delay", value=config.start_delay),
        gr.Textbox(label="fps", value=config.fps),
        gr.Textbox(label="resolution", value=config.resolution),
        gr.Textbox(label="resolution_back", value=config.resolution_back),
        gr.Textbox(label="vertical_resolution", value=config.vertical_resolution),
        gr.Textbox(label="vertical_resolution_back", value=config.vertical_resolution_back),
        gr.Textbox(label="font", value=config.font),
        gr.Textbox(label="text_size", value=config.text_size),
        gr.Textbox(label="text_color", value=config.text_color),
        gr.Textbox(label="stroke_color", value=config.stroke_color),
        gr.Textbox(label="stroke_size", value=config.stroke_size),
        gr.Textbox(label="align", value=config.align),
    ],
    outputs=["text"],
    allow_flagging="never",
    clear_btn=None
)

gui = gr.TabbedInterface(
    interface_list=[run_main, run_save_story, run_config_edit], tab_names=["make video", "save story", "config_edit"],
    title="Reddit Auto Vid"
)

gui.launch()
