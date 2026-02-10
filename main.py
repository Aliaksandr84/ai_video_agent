from flask import Flask, request, jsonify
from model import run_dial_inference

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    img_file = request.files['image']
    result = run_dial_inference(img_file)  # Implement this function according to your model
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)