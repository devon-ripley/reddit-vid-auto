import main
import config
import gradio as gr

def greeting(name, intensity):
    return "hello, " + name + "!" * int(intensity)

gui = gr.Interface(
    fn=greeting,
    inputs=["text", "slider"],
    outputs=["text"]
)

gui.launch()