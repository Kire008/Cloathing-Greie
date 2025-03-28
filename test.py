import json

with open("static/generated_outfits/outfit0.json", "r") as file:
    data = json.load(file)

print(data)