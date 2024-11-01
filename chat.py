from openai import OpenAI
import auth_data

client = OpenAI(api_key=auth_data.token_chat_gpt)

response = client.images.generate(
  model="dall-e-2",
  prompt="водитель бетономешалки 65 лет очень худой с облезлым опухшим лицом, без пальцев на руке, алкоголик и гомосексуалист за спиной у него бетономешалка",
  n=1,
  size="1024x1024"
)

print(response)