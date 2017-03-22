from datetime import datetime


class TimeGenerator:
    @staticmethod
    def generar_datetime(day=-1, month=-1, year=-1, hour=-1, minute=-1,
                         second=-1, microsecond=-1):
        today = datetime.today()
        day = today.day if day == -1 else day
        month = today.month if month == -1 else month
        year = today.year if year == -1 else year
        hour = today.hour if hour == -1 else hour
        minute = today.minute if minute == -1 else minute
        second = today.second if second == -1 else second
        microsecond = today.microsecond if microsecond == -1 else microsecond
        modificada = today.replace(day=day, month=month, year=year, hour=hour,
                                   minute=minute, second=second,
                                   microsecond=microsecond)
        return modificada

    @staticmethod
    def convert_datetime_to_string(datetime):
        hour = str(datetime.hour) if datetime.hour >= 10 else '0' + str(
            datetime.hour)
        minute = str(datetime.minute) if datetime.minute >= 10 else '0' + str(
            datetime.minute)
        second = str(datetime.second) if datetime.second >= 10 else '0' + str(
            datetime.second)
        fecha_str = hour + ':' + minute + ':' + second
        return fecha_str

    @staticmethod
    def generate_time_string(day=-1, month=-1, year=-1, hour=-1, minute=-1,
                    second=-1, microsecond=-1):
        datetime = TimeGenerator.generar_datetime(day, month, year, hour,
                                                  minute, second, microsecond)
        return TimeGenerator.convert_datetime_to_string(datetime)
