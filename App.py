from flask import Flask, render_template, Response, redirect, url_for
from Python import CameraAccess as ca
from Python import Ai_thing as ai
import os

app = Flask(__name__)
response = ''

@app.route('/')
def home():
    return render_template("Home.html")

@app.route('/AITools')
def AItools():
    return render_template("AITools.html")

@app.route("/GenerateOutfits")
def generate_outfits():
    return render_template("GenerateOutfits.html")

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