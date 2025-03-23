import openai
import base64
import os
import cv2
import pickle

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
    API_KEY = "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"  # Replace with your OpenAI API key
    user_prompt = "Analyze the image, return which cloathing type (sweather, pants, shorts, shoes, hats, etc..), also return the color and patterns of the cloathing. Really focus if there is cloathing or not, if its not only return False. Everything you return should be in format: type of cloathing color patterns"
    image_path = "static/Saved_Images/img.jpg"
    response = chat_with_gpt(API_KEY, image_path, user_prompt)
    if response != "False":
        return response

    else:
        os.remove("static/Saved_Images/img.jpg")
        return False
    
def save_img(category, color, patterns):
    try:
        n = len([file for file in os.listdir(f"static/Saved_Images/{category.lower()}") if file.endswith('.jpg')])
    except:
        os.makedirs(f"static/Saved_Images/{category.lower()}")
        n=0
    cv2.imwrite(f'static/Saved_Images/{category.lower()}/{category.lower()} {n}.jpg', cv2.imread("static/Saved_Images/img.jpg"))
    with open(f'static/Saved_Images/{category.lower()}/imgData {n}.pkl', 'wb') as fi:
        pickle.dump([category, color, patterns], fi)