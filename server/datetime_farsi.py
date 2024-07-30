from persiantools.jdatetime import JalaliDate
from persiantools import digits
import datetime


class DatetimeFarsi:
    def today_date(self):
        date_today_persian = JalaliDate.today()
        persian_day = digits.en_to_fa(str(date_today_persian.day))

        persian_months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                          'اسفند']
        persian_month = persian_months[int(date_today_persian.month) - 1]

        persian_year = digits.en_to_fa(str(date_today_persian.year))

        return f"{persian_day} {persian_month} {persian_year}"

    def today_day_name(self):
        all_week_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        persian_week_days = ["یک شنبه", "دو شنبه", "سه شنبه", "چهار شنبه", "پنج شنبه", "جمعه", "شنبه"]
        now = datetime.datetime.now()
        position_index = all_week_days.index(now.strftime("%A"))
        return persian_week_days[position_index]
