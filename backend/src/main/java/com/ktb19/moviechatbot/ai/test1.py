# -*- encoding: utf-8 -*-

import json

def parseQuery(query):

    print(query)

    movieName = "코난"
    region = "경기도 구리시"
    date = "2024-07-24"

    json_object = {
        "movieName": movieName,
        "region": region,
        "date": date,
    }

    return json.dumps(json_object)