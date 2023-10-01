from flask import Flask, render_template, redirect, url_for, request, session, redirect
from flask import request
from sklearn.preprocessing import StandardScaler
from pymongo import MongoClient
from flask_pymongo import PyMongo
import pymongo
import bcrypt
from sklearn.preprocessing import StandardScaler
import pickle
import uuid
import json
from pymongo.mongo_client import MongoClient

scaler = StandardScaler()
model = pickle.load(open('log.pkl', 'rb'))
app = Flask(__name__, template_folder='template')



uri = "mongodb+srv://divijkharche01:LEATHERbat01@cluster0.g4wwula.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri,connect=False)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.db
collection = db.user



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        Email = request.form['Email']
        password = request.form['password']
        print(username)
        print(Email)
        print(password)
        user = False
        # user = collection.find_one({'Email': request.form['Email']})
        if user:
            return render_template('register.html', error='Username already exists')
        else:
            # hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            collection.insert_one({'name': request.form['username'], 'Email': request.form['Email'], 'password': request.form['password']})
            # collection.insert_one({'Email': Email, 'password': password})
            # session['Email'] = request.form['Email']
            print("successful")
            return redirect('/login.html')
    else:
        return render_template('register.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user = collection.find_one({'Email': request.form['Email']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['Email'] = request.form['Email']
                return render_template('stroke.html')
                # return redirect(url_for('stroke'))
            # return redirect('/')
        else:
            return 'Invalid username or password'

    return render_template('login.html')



@app.route('/stoke.html')
def stroke():
    if 'username' in session:
        @app.route('/predict', methods=['POST'])
        def predict_stroke():
            if request.method == "POST":
                gender = request.form['gender']
                age = int(request.form['age'])
                hypertension = int(request.form['hypertension'])
                disease = int(request.form['heart_disease'])
                married = request.form['married']
                work = request.form['work']
                residence = request.form['residence']
                glucose = float(request.form['glucose'])
                bmi = float(request.form['bmi'])
                smoking = request.form['smoking']

                # gender
                if (gender == "Male"):
                    gender_male = 1
                    gender_other = 0
                elif (gender == "Other"):
                    gender_male = 0
                    gender_other = 1
                else:
                    gender_male = 0
                    gender_other = 0

                # married
                if (married == "Yes"):
                    married_yes = 1
                else:
                    married_yes = 0

                # work  type
                if (work == 'Self-employed'):
                    work_type_Never_worked = 0
                    work_type_Private = 0
                    work_type_Self_employed = 1
                    work_type_children = 0
                elif (work == 'Private'):
                    work_type_Never_worked = 0
                    work_type_Private = 1
                    work_type_Self_employed = 0
                    work_type_children = 0
                elif (work == "children"):
                    work_type_Never_worked = 0
                    work_type_Private = 0
                    work_type_Self_employed = 0
                    work_type_children = 1
                elif (work == "Never_worked"):
                    work_type_Never_worked = 1
                    work_type_Private = 0
                    work_type_Self_employed = 0
                    work_type_children = 0
                else:
                    work_type_Never_worked = 0
                    work_type_Private = 0
                    work_type_Self_employed = 0
                    work_type_children = 0

                # residence type
                if (residence == "Urban"):
                    Residence_type_Urban = 1
                else:
                    Residence_type_Urban = 0

                # smoking sttaus
                if (smoking == 'formerly smoked'):
                    smoking_status_formerly_smoked = 1
                    smoking_status_never_smoked = 0
                    smoking_status_smokes = 0
                elif (smoking == 'smokes'):
                    smoking_status_formerly_smoked = 0
                    smoking_status_never_smoked = 0
                    smoking_status_smokes = 1
                elif (smoking == "never smoked"):
                    smoking_status_formerly_smoked = 0
                    smoking_status_never_smoked = 1
                    smoking_status_smokes = 0
                else:
                    smoking_status_formerly_smoked = 0
                    smoking_status_never_smoked = 0
                    smoking_status_smokes = 0

                feature = scaler.fit_transform([[age, hypertension, disease, glucose, bmi, gender_male, gender_other,
                                                 married_yes, work_type_Never_worked, work_type_Private,
                                                 work_type_Self_employed, work_type_children, Residence_type_Urban,
                                                 smoking_status_formerly_smoked, smoking_status_never_smoked,
                                                 smoking_status_smokes]])

                prediction = model.predict(feature)[0]


                # if prediction == 0:
                #     if (bmi<=25 and glucose <=75):
                #         prediction = "Normal"
                #     elif (bmi <= 25 and glucose >= 75):
                #         prediction = "Normal"
                #     elif (bmi>25 and bmi<=30 and glucose >=76 and glucose<=110):
                #         prediction = " Increased Risk (High)"
                #     elif (bmi>30 and bmi<=35 and glucose >110 and glucose <=125):
                #         prediction = "Very High Risk"
                #     elif (bmi>35 and glucose >126):
                #         prediction = "Extremely High Risk"
                # else:
                # prediction = "YES"]

                collection.insert_one({'gender': gender, 'age': age, 'hypertension': hypertension, 'married': married, 'work': work, 'residence': residence, 'glucose': glucose, 'bmi': bmi, 'smoking': smoking, 'prediction': prediction})
                return render_template("stroke.html", prediction_text="Chance of Stroke Prediction is --> {}".format(prediction))

            else:
                return redirect(url_for('stroke'))

        return render_template('stroke.html')

    else:
        return redirect('/login')




@app.route('/logout')
def logout():
    session.pop('Email', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
