from flask import Flask, g, render_template, request, jsonify
from functools import wraps
from sklearn.externals import joblib
import pandas as pd
import json

#Machine learning model
model = joblib.load("Model/Classifier.pkl")

app = Flask(__name__)

#Authentication
api_user = 'rootadmin'
api_pass = 'goodpass'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.authorization

        if auth and auth.username == api_user and auth.password == api_pass:

            return f(*args, **kwargs)

        else:
           
            return jsonify({'message' : 'Authentication failed!'}), 403

    return decorated

#Routes

@app.route('/predict',methods=['POST'])
def predict():

    #Get member info from request
    prediction = request.get_json(force=True)
    predict_data = pd.DataFrame(prediction,index=[1])

    #Predict with the model
    predicted_data = model.predict(predict_data)[0]

    #Output to user
    output = {'Prediction': predicted_data}
    final_prediction = jsonify(output)

    return final_prediction


if __name__ == '__main__':
    app.run(debug=True)