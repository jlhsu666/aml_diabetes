from flask import Flask,request,render_template
import urllib
import json

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("form.html")

@app.route('/aml', methods=['GET','POST'])
def aml():
# request.values['p1']
# data = {
#     "Inputs": {
#         "WebServiceInput0":
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
            "WebServiceInput0":
            [
                {
                    'AGE': request.values['p1'],
                    'SEX': request.values['p2'],
                    'BMI': request.values['p3'],
                    'BP': request.values['p4'],
                    'S1': request.values['p5'],
                    'S2': request.values['p6'],
                    'S3': request.values['p7'],
                    'S4': request.values['p8'],
                    'S5': '4.8598',
                    "S6": '87',
                    "Y": '151',
                },
            ],
        },
        "GlobalParameters": {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'http://20.239.122.214:80/api/v1/service/ai-brain/score'
    api_key = 'o1HomfPgcBcWKQpiue1eRQmQlLvA5J3B' # Replace this with the API key for the web service
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

