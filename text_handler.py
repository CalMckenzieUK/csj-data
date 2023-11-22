from openai import OpenAI
import os
import dotenv

key = dotenv.get_variable(file_path='/workspaces/flask_app/.env', key='OPENAI_API_KEY')



client = OpenAI(api_key=str(key))

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
