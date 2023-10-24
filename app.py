import openai
import os 
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import gradio as gr

os.environ['OPENAI_API_KEY'] = ''
openai.api_key = os.getenv('OPENAI_API_KEY')


memory = ConversationBufferMemory()
llm = ChatOpenAI()
conversation = ConversationChain(
    llm=llm,
    memory=memory
)

with gr.Blocks() as chat_system:
    chat = gr.Chatbot()
    prompt = gr.Textbox(placeholder="What's on your mind?")
    clear = gr.ClearButton([prompt, chat])
    clear.click(conversation.memory.clear)

    def llm_reply(prompt, chat_history):
        reply = conversation.predict(input=prompt)
        chat_history.append((prompt, reply))
        return "", chat_history

    prompt.submit(llm_reply, [prompt, chat], [prompt, chat])


if __name__ == "__main__":

    chat_system.queue().launch(
        server_name='0.0.0.0',
        share=False
    )