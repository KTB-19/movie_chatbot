from datetime import datetime
import pytz

def kor_today():
        # 한국 시간대 설정
    kst = pytz.timezone('Asia/Seoul')
    utc_now = datetime.now(pytz.utc)
    kst_now = utc_now.astimezone(kst)
    today = kst_now.strftime('%m/%d')
    weekday = kst_now.strftime('%A')

    return today, weekday
def format_date_time(date, time):
    formatted_date = date
    formatted_time = time

    if date:
        try:
            date_obj = datetime.strptime(date, '%m/%d')
            current_year = datetime.now().year
            formatted_date = date_obj.replace(year=current_year).strftime('%Y-%m-%d')
        except ValueError:
            # 날짜 형식이 예상과 다를 경우 원래 값 유지
            pass

    if time:
        try:
            time_obj = datetime.strptime(time, '%H시')
            formatted_time = time_obj.strftime('%H:%M')
        except ValueError:
            # 시간 형식이 예상과 다를 경우 원래 값 유지
            pass

    return formatted_date, formatted_time