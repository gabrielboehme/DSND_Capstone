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

@app.route('/')
def index():

    return render_template('master.html')

@app.route('/predictform',methods=['POST'])
def predictform():

    #Get member info from request
    form_data = request.form
    df = pd.DataFrame(form_data, index=[1])
    '''
    ticket_id = request.args.get('ticket_id', '')
    violation_code = request.args.get('violation_code','')
    disposition = request.args.get('disposition','')
    fine_amount = request.args.get('fine_amount','')
    late_fee = request.args.get('late_fee','')
    discount_amount = request.args.get('discount_amount','')
    clean_up_cost = request.args.get('clean_up_cost','')
    judgment_amount = request.args.get('judgment_amount','')
    lat = request.args.get('lat','')
    lon = request.args.get('lon','')
    '''
    #Predict with the model
    predicted_data = model.predict(df)[0]

    #Output to user
    output = {'Prediction': predicted_data}
    final_prediction = jsonify(output)

    return final_prediction


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