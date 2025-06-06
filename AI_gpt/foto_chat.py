from openai import OpenAI
import src.auth_data as auth_data

client = OpenAI(api_key=auth_data.token_chat_gpt)


def get_foto(request):
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"{request}",
        n=1,
        size="1024x1024"
    )

    return response


print(get_foto("космический брутальный водитель бетономешалки програмист"))
