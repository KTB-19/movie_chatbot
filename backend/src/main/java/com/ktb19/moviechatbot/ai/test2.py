# -*- encoding: utf-8 -*-

def parseQueries(movieNameQuery, regionQuery, dateQuery):
    print(movieNameQuery)
    print(regionQuery)
    print(dateQuery)

    # 입력 값에서 추출할 수 없는 것은 None 반환
    movieName = None
    region = u"경기도 구리시"
    date = u"2024-07-27"

    # JSON 객체를 문자열로 직접 작성
    json_object = u"""
    {
        "movieName": "%s",
        "region": "%s",
        "date": "%s"
    }
    """ % (movieName, region, date)

    return json_object