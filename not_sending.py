import datetime
from datetime import datetime
import calendar
import asyncio
import time
import sqlite3
data = {
            "date": input("Введите дату (В формате DD.MM.YY)"),
            "time": input("Введите дату (В формате HH.MM)"),
            "task": input("Введите текст упоминания")
}

connection = sqlite3.connect("database.db")


async def time_sleep():

    ndate = f"{data["date"]} {data["time"]}".replace(".", "/")
    element = datetime.strptime(ndate, "%d/%m/%y %H/%M")
    tuple = element.timetuple()
    timestamp = int(time.mktime(tuple))
    dt = time.mktime(datetime.today().timetuple())
    sleept = timestamp - dt
    print(sleept)
    await asyncio.sleep(sleept)

def Check_Not():
    asyncio.run(time_sleep())
    print(data["task"])

Check_Not()



