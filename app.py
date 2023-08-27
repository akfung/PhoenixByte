import requests
import random
from bs4 import BeautifulSoup
import time
import gradio as gr

from config import model_path, tokenizer_path
from model import Model

class CaseSummaries:
    def __init__(self):
        self._case_summaries = None

    @property
    def case_summaries(self):
        if self._case_summaries == None:
            r = requests.get('https://en.wikipedia.org/wiki/List_of_pending_United_States_Supreme_Court_cases')
            soup = BeautifulSoup(r.content, 'html')
            self._case_summaries = soup.find_all(True, {'class': ['wikitable', 'sortable', 'jquery-tablesorter']})[0].find_all('tr')[1:]
        return self._case_summaries

    def random_summary(self) -> str:
        # function to get a random case summary from wikipedia pending list
        row:str = random.choice(self.case_summaries)
        summary = row.find_all('td')[2]
        summary = summary.get_text()
        return summary
    

def run():
    
    summaries = CaseSummaries()
    case_placeholder = summaries.random_summary()
    model = Model(model_path=model_path, tokenzier_path=tokenizer_path)
    with gr.Blocks() as demo:
        cache = gr.Textbox(visible=False)
        with gr.Row():
            btn = gr.Button(value="Get Random Case")
            btn2 = gr.Button(value="Run")

        with gr.Row():
            txt = gr.Textbox(label="Case Description", lines=15, value=case_placeholder)
            txt2 = gr.Chatbot(label='Predicted Court Opinion')


        btn.click(summaries.random_summary, outputs=[txt], queue=False)
        # btn2.click(inference, inputs=[txt], outputs=[txt2])
        btn2.click(lambda x: x, txt, cache, queue=False).then(
            model.inference, cache, txt2)

    demo.queue().launch(server_name= "0.0.0.0", share=False)

if __name__=='__main__':
    run()