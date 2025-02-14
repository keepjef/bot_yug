import datetime
from datetime import datetime
import calendar
import asyncio
import time
data = {
            "date": input("Введите дату (В формате DD.MM.YY)"),
            "time": input("Введите дату (В формате HH.MM)"),
            "text": input("Введите текст упоминания")
}



async def time_sleep():

    ndate = f"{data["date"]} {data["time"]}".replace(".", "/")
    element = datetime.strptime(ndate, "%d/%m/%Y %H/%M")
    tuple = element.timetuple()
    timestamp = int(time.mktime(tuple))
    dt = time.mktime(datetime.today().timetuple())
    sleept = timestamp - dt
    print(sleept)
    await asyncio.sleep(sleept)

def Check_Not():
    asyncio.run(time_sleep())
    print(data["text"])

Check_Not()


