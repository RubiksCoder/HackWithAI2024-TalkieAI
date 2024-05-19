import requests
from dotenv import load_dotenv
import os
import gradio as gr
import assemblyai as aai


load_dotenv()

api_key = os.getenv('API_KEY')
# Replace with your API key
aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')

headers = {
   'Authorization': f'sk-{api_key}'
}

data = {
  "phone_number": "+16136129319",
  "from": None,
  "task": "You are Sammy. You are a personal assistant for Yash Joshi. You are calling TD bank to ask about how to open a tax free savings account.",
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

# requests.post('https://api.bland.ai/v1/calls', json=data, headers=headers)


def process_input(name, phone_number, audio, text):
  transcriber = aai.Transcriber()
  transcript = transcriber.transcribe(audio)

  if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
  else:
    print(transcript.text)
    # This is where you would process the inputs and generate an output
  return transcript.text + f"name is: {name} and phone number to call: {phone_number}"


def main():

  # Define the interface
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

  # Launch the interface
  iface.launch()

if __name__ == "__main__":
  main()  