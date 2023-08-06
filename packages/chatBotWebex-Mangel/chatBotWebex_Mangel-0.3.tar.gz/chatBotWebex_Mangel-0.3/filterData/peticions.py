import requests
import json
from datetime import datetime


class Peticions :

    def getEdge(edgeID, url, token):

        payload = {"id": edgeID}
        header = {'Content-Type': 'application/json',
                'Authorization': token}
        response = requests.post(url + 'edge/getEdge', data=json.dumps(payload), headers=header)

        if response.status_code == 200:
            result = response.json()
            return result 


    def getEdgeLinkMetrics(edgeID, url, token, date= datetime.now().isoformat()+'Z'):

        print(date)

        payload = {
            "id": edgeID,
            "interval": {
                "start": date
            }
        }
        header = {'Content-Type': 'application/json',
                'Authorization': token}
        response = requests.post(url + 'metrics/getEdgeLinkMetrics', data=json.dumps(payload), headers=header)

        if response.status_code == 200:
            result = response.json()
            return result


    def getEdgeAppLinkSeries(edgeID, url, token, date= datetime.now().isoformat()+'Z'):

        payload = {
            "id": edgeID,
            "interval": {
                "start":  date
            }
        }
        header = {'Content-Type': 'application/json',
                'Authorization': token}
        response = requests.post(url + 'metrics/getEdgeAppLinkSeries', data=json.dumps(payload), headers=header)

        if response.status_code == 200:
            result = response.json()
            return result

    def test(number):
        print(number)