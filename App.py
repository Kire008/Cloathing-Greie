from flask import Flask, render_template, Response
from Python import CameraAccess as ca

app = Flask(__name__)

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



#Important Functions:
@app.route('/Add_Item')
def Add_Item():
    return render_template("Add_Item.html")
    

@app.route('/Video')
def video():
    return Response(ca.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)