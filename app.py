from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load('heart-disease-model.pkl')

@app.route('/')
def home():
    return "Heart Disease Prediction API"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = np.array(data['features']).reshape(1, -1)

        prediction = model.predict(features)
        probability = model.predict_proba(features) if hasattr(model, 'predict_proba') else None

        response = {
            "prediction": int(prediction[0]),
            "probability": probability.tolist() if probability is not None else "Not available"
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
