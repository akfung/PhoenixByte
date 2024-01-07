
import gradio as gr

from src.config import readme
from src.model import Model
from src.config import justice_names
from src.case_summaries import CaseSummaries

def run():
    choices = list(justice_names)+['Court']
    summaries = CaseSummaries()
    case_placeholder = summaries.random_summary()
    model = Model()
    
    with gr.Blocks(theme=gr.themes.Soft(text_size=gr.themes.sizes.text_lg)) as demo:
        cache = gr.Textbox(visible=False)
        description = gr.Markdown(value=readme)
        dropdown = gr.Dropdown(
            label="Justice Name",
            choices=choices,
            value='Court',
            interactive=True,
            )
        with gr.Row():
            btn = gr.Button(value="Get Random Case")
            btn2 = gr.Button(value="Run")

        with gr.Row():
            txt = gr.Textbox(label="Case Description", lines=15, value=case_placeholder)
            txt2 = gr.Chatbot(label='Predicted Court Opinion')

        btn.click(summaries.random_summary, outputs=[txt], queue=False)
        btn2.click(lambda x: x, inputs=[txt], outputs=cache, queue=False).then(
            model.inference, inputs=[cache, dropdown], outputs=txt2)

    demo.queue().launch(share=False, server_name="0.0.0.0")

if __name__=='__main__':
    run()