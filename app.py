
import gradio as gr

from config import model_path, tokenizer_path, env, bucket_name, readme
from model import Model
from case_summaries import CaseSummaries

def run():

    summaries = CaseSummaries()
    case_placeholder = summaries.random_summary()
    model = Model(model_path=model_path, tokenizer_path=tokenizer_path)
    
    with gr.Blocks() as demo:
        cache = gr.Textbox(visible=False)
        description = gr.Markdown(value=readme)
        with gr.Row():
            btn = gr.Button(value="Get Random Case")
            btn2 = gr.Button(value="Run")

        with gr.Row():
            txt = gr.Textbox(label="Case Description", lines=15, value=case_placeholder)
            txt2 = gr.Chatbot(label='Predicted Court Opinion')

        btn.click(summaries.random_summary, outputs=[txt], queue=False)
        btn2.click(lambda x: x, txt, cache, queue=False).then(
            model.inference, cache, txt2)

    demo.queue().launch(server_name= "0.0.0.0", server_port=8080, share=False)

if __name__=='__main__':
    run()