from flask import Flask, render_template, Response, redirect, url_for, jsonify, request
from Python import CameraAccess as ca
from Python import Ai_thing as ai
import os
import json

app = Flask(__name__)
response = ''

@app.route('/')
def home():
    return render_template("Home.html")

#---Cloathing Grid---
@app.route('/get_items')
def get_items():
    current_category = request.args.get("category")
    print(current_category)

    items = []
    for file in [file for file in os.listdir(f"static/Saved_Images/{current_category}") if file.endswith('.json')]:
        with open(f"static/Saved_Images/{current_category}/{file}", "r") as fi:
            items.append(json.load(fi))
            print(items)
    return jsonify(items)

@app.route('/AITools')
def AItools():
    return render_template("AITools.html")

@app.route("/GenerateOutfits")
def GenerateOutfits():
    return render_template("GenerateOutfits.html")

@app.route("/generate_outfit_prompt", methods=["POST"])
def generate_outfit_prompt():
    data = request.json
    inp = data.get("user_text", "")
    
    outfit_data = ai.generate_outfit(inp)  # Generate outfit

    if isinstance(outfit_data, str):  # If it's a string, parse it
        try:
            outfit_data = json.loads(outfit_data)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format from AI"}), 500
    
    print(outfit_data)  # Debugging

    return jsonify(outfit_data)  # Return as a proper JSON object


@app.route("/generate_outfit_pressed")
def generate_outfit_pressed():
    inp = "rain"
    ai.generate_outfit(inp)
    return redirect("GenerateOutfits")

@app.route('/MixMatch')
def mix_match():
    return render_template("MixMatch.html")

@app.route('/MyLooks')
def my_looks():
    return render_template("MyLooks.html")

@app.route('/OutfitGallery')
def outfit_gallery():
    return render_template("OutfitGallery.html")


#Adding Items
@app.route('/captured_img_analyzed')
def captured_img_analyzed():
    return render_template("/captured_img_analyzed.html")


#Important Functions:
@app.route('/Add_Item')
def Add_Item():
    return render_template("Add_Item.html")
    

@app.route('/Video')
def video():
    return Response(ca.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_img')
def capture_img():
    global response
    ca.capture_img()
    response = ai.analyze()
    if response != False:
        category, color, patterns = response.split(' ')
        return redirect(url_for("captured_img_analyzed", category=category, color=color, patterns=patterns))
    else:
        return redirect(url_for("Add_Item", error='true'))

@app.route("/del_img")
def delete_image():
    try:
        os.remove("static/Saved_Images/img.jpg")
    except:
        pass
    return redirect("/Add_Item")

@app.route("/save_img")
def save_image():
    global response
    ai.save_img(response.split(' ')[0], response.split(' ')[1], response.split(' ')[2])
    os.remove("static/Saved_Images/img.jpg")
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)