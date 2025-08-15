"""
Flask server for the Emotion Detection web app.
This file handles HTTP routes, integrates with the emotion detector,
and returns results to the client in JSON format.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """
    Render the main index page.
    """
    return render_template("index.html")


@app.route("/emotionDetector", methods=["POST"])
def detect_emotion():
    """
    Detect emotions in the provided text using Watson NLP.
    Returns a JSON response with emotion scores or an error message.
    """
    text_to_analyse = request.form["textToAnalyze"]
    result = emotion_detector(text_to_analyse)

    # Handle invalid or blank input
    if result['dominant_emotion'] is None:
        return jsonify({
            "formatted_output": "Invalid text! Please try again!"
        })

    anger = result['anger']
    disgust = result['disgust']
    fear = result['fear']
    joy = result['joy']
    sadness = result['sadness']
    dominant = result['dominant_emotion']

    response_str = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )

    return jsonify({
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness,
        "dominant_emotion": dominant,
        "formatted_output": response_str
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
