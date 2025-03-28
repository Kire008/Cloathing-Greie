import openai
import base64
import os
import cv2
import json


API_KEY = "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"  # Replace with your OpenAI API key
def chat_with_gpt(api_key, image_path, prompt, model="gpt-4-turbo", temperature=0.7, max_tokens=256):
    client = openai.OpenAI(api_key=api_key)


    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")


    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI that can analyze and rename images of clothes. You will try to only answer in one word for each task."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def analyze():
    global API_KEY
    user_prompt = "Analyze the image, return which cloathing type (it has to be exactly one of these: shirts, pants, shoes, jackets or misc for handbags, hats and other acceossries), also return the color and patterns of the cloathing. Really focus if there is cloathing or not, if its not only return False. Everything you return should be in format: type of cloathing color patterns"
    image_path = "static/Saved_Images/img.jpg"
    response = chat_with_gpt(API_KEY, image_path, user_prompt)
    response=response.lower()
    if response != "False":
        return response

    else:
        os.remove("static/Saved_Images/img.jpg")
        return False
    
def save_img(category, color, patterns):
    try:
        n = len([file for file in os.listdir(f"static/Saved_Images/{category}") if file.endswith('.jpg')])
    except:
        os.makedirs(f"static/Saved_Images/{category}")
        n=0
    data = [
        {"category": category},
        {"color": color},
        {"patterns": patterns},
        {"img_path": f"static/Saved_Images/{category}/img {n}.jpg"}
    ]
    cv2.imwrite(f'static/Saved_Images/{category}/img {n}.jpg', cv2.imread("static/Saved_Images/img.jpg"))
    with open(f'static/Saved_Images/{category}/imgData {n}.json', 'w') as fi:
        json.dump(data, fi, indent=4)


def generate_outfit(generate_outfit_input):
    global API_KEY
    data = []
    for cloathing in os.listdir("static/Saved_Images/"):
        for file in [file for file in os.listdir(f"static/Saved_Images/{cloathing}") if file.endswith('.json')]:
            with open(f"static/Saved_Images/{cloathing}/{file}", 'r') as fi:
                data.append(fi.read())

    client = openai.OpenAI(api_key=API_KEY)
    model = "gpt-4-turbo"
    temperature = 0.7
    max_tokens = 256
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI that can analyze images or description of clothes. You will try to only answer in one word for each task."},
                {"role": "user", "content": f"Give me a outfit that contains atleast a shirt and pants, and add other clothes and accessories (misc) that fits for the input given. make sure the clothes are from the list of clothes im giving you. Return all the data of the cloathing pieces you choose in the same format i gave you, except its not inside a list but its a dict. Clothes: {data} Input: {generate_outfit_input}"}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        outfit_response = response.choices[0].message.content

        # Ensure the output folder exists
        os.makedirs("static/generated_outfits", exist_ok=True)

        # Get the number of existing files to avoid overwriting
        n = len([file for file in os.listdir("static/generated_outfits") if file.endswith(".json")])

        return outfit_response

    except Exception as e:
        return f"Error: {e}"