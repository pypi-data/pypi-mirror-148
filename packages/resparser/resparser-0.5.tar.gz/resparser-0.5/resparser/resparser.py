
import requests
import json
# from rest_framework.renderers import JSONRenderer
URL ="https://yashsonwane.pythonanywhere.com/resumeapi/"

#insert data
def resumeparser(data):
    #convert text into json
    data=data.replace('\n',' ')
    data = { 'text' : data}

    json_data = json.dumps(data)
    r = requests.post(url=URL, data = json_data)
    data = r.json()
    # print(data)
    return data

