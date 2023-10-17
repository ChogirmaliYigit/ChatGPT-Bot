import openai
from environs import Env

env = Env()
env.read_env()
API_KEY = env.str("API_KEY")  # Api Key

def get_response(messages):
    openai.api_key = API_KEY
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages,
        temperature=0.7
    )
    response = completion.get("choices")[0].get("message").get("content")
    return response