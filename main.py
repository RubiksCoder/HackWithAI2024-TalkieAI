import requests
from dotenv import load_dotenv
import os
import gradio as gr
import assemblyai as aai
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('API_KEY')
aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')
assembly_api_key = os.getenv('GOOGLE_API_KEY')

headers = {
   'Authorization': f'sk-{api_key}'
}

data = {
  "phone_number": "",
  "from": None,
  "task": "",
  "model": "enhanced",
  "language": "eng",
  "voice": "Florian",
  "voice_settings": {},
  "local_dialing": False,
  "max_duration": 12,
  "answered_by_enabled": False,
  "wait_for_greeting": False,
  "record": True,
  "amd": False,
  "interruption_threshold": 100,
  "temperature": None,
  "transfer_list": {},
  "metadata": {},
  "pronunciation_guide": [],
  "start_time": None,
  "request_data": {},
  "tools": [],
  "webhook": None
}

genai.configure(api_key=assembly_api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

def generate_output(message, name):
  # print(message)
  default = f"You are Joe. You are a personal assistant for {name}."
  before = """Please create a prompt for an AI calling assistant made with bland Ai. This 
              calling assistant takes in requests to call places to book appointments or inquire
              about information or whatever the user asks it to do. Here is the prompt from the 
              user, please generate a prompt for the assistant (tell them what they should be doing):"""
  response = chat_session.send_message(before + message)
  # print(default + response.text)
  return default + response.text

def process_input(name, phone_number, audio, text):
  if audio is not None:
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio)

    if transcript.status == aai.TranscriptStatus.error:
      print(transcript.error)
    else:
      print(transcript.text)

    msg = generate_output(transcript.text, name)
    data["phone_number"] = phone_number
    data["task"] = msg
    requests.post('https://api.bland.ai/v1/calls', json=data, headers=headers)
  
  else:
    msg = generate_output(text + f"name is: {name} and phone number to call: {phone_number}", name)
    data["phone_number"] = phone_number
    data["task"] = msg
    requests.post('https://api.bland.ai/v1/calls', json=data, headers=headers)

def main():
  iface = gr.Interface(
      process_input,
      inputs=[
          gr.Textbox(label="Name"),
          gr.Textbox(label="Phone Number to Call:"),
          gr.Audio(type="filepath", label="Speak here"),
          gr.Textbox(lines=2, placeholder="Type here...", label="Prompt here")
      ],
      outputs="text",
      title="Speech and Text Input Demo",
      description="A simple demo app to take speech and text input and provide an output."
  )
  iface.launch()

if __name__ == "__main__":
  main()  