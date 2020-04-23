import json  # to convert list and dictionary to json
import os
import requests
from flask import Flask  # it is microframework to develop a web app
from flask import request
from flask import make_response

# Falsk app for our web app
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():  # convert the data from json.
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeResponse(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    state = parameters.get("geo-state")
    #date = parameters.get("date")
    param = parameters.get("cat_select")
    r = requests.get('https://api.covid19india.org/data.json')
    json_object = r.json()
    Info = json_object['statewise']
    condition = ''.join([i[param] for i in Info if i['state'] == state])
    if param != 'deaths':
        speech = "The no. of " + param + " reported in " + state + " is " + condition
    else:
        speech = "The no. of " + param + " cases reported in " + state + " is " + condition
    return {"fulfillmentMessages": Speech
           }  # return { # "speech": speech, # "displayText":speech, # "source":"apiai-weather-webhook"}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("starting on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
