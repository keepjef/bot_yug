import datetime

data = {
            "date": "07.02.2025",
            "time": "18.04",
            "text": "hi"
}


def Check_Not():
    while True:
        ndate = f"{data["date"]} {data["time"]}"
        dater = datetime.datetime.now().strftime('%d.%m.%Y %H.%M')

        if ndate == dater:
            print(data["text"])
            break

Check_Not()
