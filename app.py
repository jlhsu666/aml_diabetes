from flask import Flask,request,render_template
import urllib
import json
import os

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("form.html")

@app.route('/aml', methods=['GET','POST'])
def aml():
# request.values['p1']
# data = {
#     "Inputs": {
#         "input1":
#         [
#             {
#                 'Pregnancies': "6",
#                 'Glucose': "148",
#                 'BloodPressure': "72",
#                 'SkinThickness': "35",
#                 'Insulin': "0",
#                 'BMI': "33.6",
#                 'DiabetesPedigreeFunction': "0.627",
#                 'Age': "50",
#                 'Outcome': "1",
#             },
#         ],
#     },
#     "GlobalParameters": {
#     }
# }

    data = {
        "Inputs": {
            "input1":
            [
                {
                       "Pregnancies": 6,
                       "Glucose": 148,
                       "BloodPressure": 72,
                       "SkinThickness": 35,
                       "Insulin": 0,
                       "BMI": 33.6,
                       "DiabetesPedigreeFunction": 0.627,
                       "Age": 50,
                       "Outcome": 1
#                     'Glucose': request.values['p5'],
#                     'BloodPressure': request.values['p4'],
#                     'Insulin': request.values['p6'],
#                     'BMI': request.values['p3'],
#                     'Sex': request.values['p2'],
#                     'Age': request.values['p1'],
#                     'Outcome': '4.8598'
                },
            ],
        },
        "GlobalParameters": {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'http://78e7aa04-731a-4fc9-9d33-1b8ebe7c6806.eastasia.azurecontainer.io/score'
    # api_key = '9KOw0kBlhyVauSeGfgeu72LH4UEx52Wd' # Replace this with the API key for the web service

    api_key = os.getenv("AML_API_KEY")
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    htmlstr="<html><body>"

    try:
        response = urllib.request.urlopen(req)

        result = json.loads(response.read())
        htmlstr=htmlstr+"依據您輸入的參數，經過數據分析模型比對，罹患糖尿病的結果為"
        htmlstr=htmlstr+str(result['Results']['WebServiceOutput0'][0]['Scored Labels'])
        # print(result)

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

        htmlstr=htmlstr+"</body></html>"
    return htmlstr

@app.route('/<name>')
def hello(name):
    return "Hello, " + name + "!!!"

if __name__=="__main__":
    app.run()

