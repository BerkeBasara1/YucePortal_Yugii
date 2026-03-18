from datetime import datetime, timedelta
import calendar
from ssh_sabahraporu.ssh_excel_readers import ReturnHolidayDates

# En son çalışılan günün tarihi döner (gg.aa.yyyy format)
def last_work_day(prev_month=False):
    holiday_dates, holiday_dates_lastyear = ReturnHolidayDates('Copy of Tatil Günleri ve Hedef.xlsx', 'Tatil Günleri')
    if prev_month == True:
        current_date = datetime.now()
        first_day_of_current_month = current_date.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        today = last_day_of_previous_month
    else:
        today = datetime.today()

    days_passed = []
    for i in range(21):
        if i != 0 and prev_month == False:
            day = today - timedelta(days=i)
            day = day.strftime('%d-%m-%Y').replace("-", ".")
            days_passed.append(day)
        elif prev_month == True:
            day = today - timedelta(days=i)
            day = day.strftime('%d-%m-%Y').replace("-", ".")
            days_passed.append(day)

    for day in days_passed:
        if day not in holiday_dates:
            last_work_day = day
            break
    return last_work_day

# gg.aa.yyyy formatında verilen tarihi '05 Ağustos 2023' formatında döner
def convert_date_Turkish_num(date):
    if '.01.' in date:
        date = date.replace('.01.', ' Ocak ')
    elif '.02.' in date:
        date = date.replace('.02.', ' Şubat ')
    elif '.03.' in date:
        date = date.replace('.03.', ' Mart ')
    elif '.04.' in date:
        date = date.replace('.04.', ' Nisan ')
    elif '.05.' in date:
        date = date.replace('.05.', ' Mayıs ')
    elif '.06.' in date:
        date = date.replace('.06.', ' Haziran ')
    elif '.07.' in date:
        date = date.replace('.07.', ' Temmuz ')
    elif '.08.' in date:
        date = date.replace('.08.', ' Ağustos ')
    elif '.09.' in date:
        date = date.replace('.09.', ' Eylül ')
    elif '.10.' in date:
        date = date.replace('.10.', ' Ekim ')
    elif '.11.' in date:
        date = date.replace('.11.', ' Kasım ')
    elif '.12.' in date:
        date = date.replace('.12.', ' Aralık ')
    return date

# Ay sonuna kaç tane çalışılan gün kaldığını döner
def howmanydaysleft():
    import datetime
    import calendar
    Tatil_gunleri, holiday_dates_lastyear = ReturnHolidayDates('Copy of Tatil Günleri ve Hedef.xlsx', "Tatil Günleri")
    today = datetime.date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    month = today.month
    year = today.year
    date_list = []
    for day in range(1, days_in_month + 1):
        try:
            date = datetime.date(year, month, day)
            if date >= today and date.strftime('%d.%m.%Y') not in Tatil_gunleri:
                date_list.append(date.strftime('%d.%m.%Y'))
        except:pass
    return len(date_list)

# Günün ismini Türkçe formatta döner
def get_day_of_week(date_string):
    date_object = datetime.strptime(date_string, '%d.%m.%Y')
    days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
    day_index = date_object.weekday()
    return days[day_index]

#
def Return_lastyear_enddate():
    import datetime
    Tatil_gunleri, holiday_dates_lastyear = ReturnHolidayDates('Copy of Tatil Günleri ve Hedef.xlsx', "Tatil Günleri")

    excluded_dates = []
    for date_str in Tatil_gunleri:
        try:
            date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
            excluded_dates.append(date)
        except ValueError:
            print(f"Skipping invalid date: {date_str}")
            
    today = datetime.date.today()

    days_in_month = range(1, today.day)
    for date in excluded_dates:
        if date.month == today.month and date.day in days_in_month:
            days_in_month = [day for day in days_in_month if day != date.day]

    amount_ofdays_worked = len(days_in_month)

    today = date.today()
    import calendar
    last_day = calendar.monthrange(today.year, today.month)[1]
    if today.day == last_day:
        months_lastday = True
    else:
        months_lastday = False

    last_year = today.year - 1
    target_month = today.month
    dates_last_year = []

    current_day = datetime.date(last_year, target_month, 1)
    while current_day.month == target_month and current_day <= today:
        dates_last_year.append(current_day.strftime('%d.%m.%Y'))
        current_day += datetime.timedelta(days=1)

    dates_last_year = [date for date in dates_last_year if date not in holiday_dates_lastyear]

    if months_lastday:
        ending_date = dates_last_year[-1]
    else:
        if len(dates_last_year) > amount_ofdays_worked:
            ending_date = dates_last_year[amount_ofdays_worked - 1]
        else:
            ending_date = dates_last_year[-1]
    return ending_date, amount_ofdays_worked
