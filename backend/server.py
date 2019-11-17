from flask import Flask
from flask import request
import url_checker
import page_checker

app = Flask(__name__)

@app.route('/check-phishing')
def hello_world():
    url = request.args.get('url')
    data1 = url_checker.computeAlerts(url)
    if data1 != []:
        data = {}
        data['isPhishing'] = True
        try:
            data2 = page_checker.get_issues(url)
            data['issues'] = data1 + data2['issues']
            return data
        except:
            raise
            data['issues'] = data1
            return data

    else:
        data = {}
        data['isPhishing'] = False
        return data
