import os
import google.generativeai as genai

assembly_api_key = os.getenv('GOOGLE_API_KEY')
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

# enter prompt here:
response = chat_session.send_message("what is 1+1")

print(response.text)