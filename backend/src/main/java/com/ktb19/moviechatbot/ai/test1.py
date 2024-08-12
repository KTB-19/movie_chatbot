# -*- encoding: utf-8 -*-

def parseQuery(query):
    print(query)

    movieName = u"코난"
    region = u"경기도 구리시"
    date = u"2024-07-24"

    # JSON 객체를 문자열로 직접 작성
    json_object = u"""
    {
        "movieName": "%s",
        "region": "%s",
        "date": "%s"
    }
    """ % (movieName, region, date)

    return json_object