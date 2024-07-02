import base_config
import gradio as gr
import json

config = base_config.setup()


def save_story(grab, sub_id, story_target):
    import main
    main.save_story(grab, sub_id, story_target)
    return "story saved"


def config_edit(client_id, client_secret, user_agent, number_of_posts, sub_reddits, number_of_comments,
                story_delim_audio, story_delim, target_story, start_delay,
                fps, resolution, resolution_back, vertical_resolution, vertical_resolution_back, font, text_size,
                text_color, stroke_color, stroke_size, align, tts_to_use):
    data = {}
    data["client_id"] = client_id
    data["client_secret"] = client_secret
    data["user_agent"] = user_agent

    # story vars autoload
    data["number_of_posts"] = number_of_posts
    # sub reddits to list
    sub = sub_reddits[:-1]
    sub = sub[1:]
    sub = sub.split(',')
    data["sub_reddits"] = sub

    # comment vars
    data["number_of_comments"] = number_of_comments
    data["story_delim_audio"] = story_delim_audio
    data["story_delim"] = story_delim
    # target story to list
    targ = target_story[:-1]
    targ = targ[1:]
    targ = targ.split(',')
    data["target_story"] = targ

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
    data["tts_to_use"] = tts_to_use
    with open('config.json', "w") as outfile:
        json.dump(data, outfile, indent=3)
    return "config file updated"


def run_vid_auto(grab, vid_path, vid_save_path, story_target, vertical, comment_target, sub_id,
                 non_api):
    import main
    main.vid_auto(grab, vid_path, vid_save_path, sub_id, story_target, vertical, comment_target, non_api)
    return f"Video saved {vid_save_path}"


run_main = gr.Interface(
    fn=run_vid_auto,
    inputs=[
        gr.Dropdown(["story", "comment"], label="Video type"),
        gr.Textbox(label="Input video path", value="input_videos/", info="Must be .mp4"),
        gr.Textbox(label="Output video path", value="output/", info="Must be .mp4"),
        gr.Checkbox(label="target story",
                    info="uses story targets from config, if checked sub id and non api must be blank"),
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
        gr.Textbox(label="sub ID", value=None),
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
        gr.Dropdown(["tts", "gtts", "pytts"], label="TTS to use", value=config.tts_to_use)
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
