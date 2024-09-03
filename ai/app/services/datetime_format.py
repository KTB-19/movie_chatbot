from datetime import datetime
import pytz
import re

def kor_today():
        # 한국 시간대 설정
    kst = pytz.timezone('Asia/Seoul')
    utc_now = datetime.now(pytz.utc)
    kst_now = utc_now.astimezone(kst)
    today = kst_now.strftime('%m/%d')
    weekday = kst_now.strftime('%A')

    return today, weekday


# 사용자가 입력한 날짜, 시간 형식 변경
def format_date_time(date, time):
    formatted_date = format_date(date)
    formatted_time = format_time(time)
    return formatted_date, formatted_time

def format_date(date):
    if not date:
        return date
    try:
        # 입력된 date 파싱 + 현재 연도: YYYY-MM-DD 형식으로 변환
        date_obj = datetime.strptime(date, '%m/%d')
        return date_obj.replace(year=datetime.now().year).strftime('%Y-%m-%d')
    except ValueError:
        return date    # 파싱 실패 시 원래 입력값 리턴

def format_time(time):
    if not time:
        return time

    # 다양한 시간 입력 패턴 문자열
    time_patterns = {
        r'^\d{1,2}:\d{2}$': lambda t: t,    # HH:MM 형식
        r'^\d{1,2}시\s?\d{1,2}분$': lambda t: datetime.strptime(t, '%H시 %M분').strftime('%H:%M'),    # HH시 MM분 형식
        r'^\d{1,2}시$': lambda t: f"{(int(t[:-1]) % 12 + 12):02}:00",    # HH시 (우선 오후로 간주)
        r'^(오전|오후)\s?\d{1,2}시$': parse_am_pm,    # 오전/오후 HH시
        r'^(오전|오후|저녁|심야)$': lambda t: {'오전': '07:00', '오후': '12:00', '저녁': '18:00', '심야': '23:00'}[t]
    }

    for pattern, formatter in time_patterns.items():
        if re.match(pattern, time):
            return formatter(time)
    return time
    
# 오전/오후 시간을 HH:MM 형식으로 변환하기
def parse_am_pm(time):
    period, hour = re.match(r'^(오전|오후)\s?(\d{1,2})시$', time).groups()
    hour = int(hour)
    if period == '오전':
        return f"{hour:02}:00" if hour < 12 else "00:00"
    else:
        return f"{(hour % 12 + 12):02}:00"
