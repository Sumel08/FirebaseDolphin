import sched, time
import datetime
import requests
import json
import random

print('Hola')

def new_temperature(date, value):

    date_string = str(date.date())
    time_string = str(date.time()).split('.')[0]

    data = {
        'fields': {
            'date': {
                'stringValue': '{} {}'.format(date_string, time_string)
            },
            'temperature': {
                'stringValue': str(value)
            }
        }
    }

    url = "https://firestore.googleapis.com/v1beta1/projects/example-dba5e/databases/%28default%29/documents/temperatura/" + str(int(date.timestamp()))
    payload = json.dumps(data)
    print(payload)
    response = requests.request("PATCH", url, data=payload)
    print(response)

for x in range(10):
    time.sleep(1);
    new_temperature(datetime.datetime.now(), random.random()*100)
