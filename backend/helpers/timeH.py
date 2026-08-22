from datetime import date, datetime, timedelta

def now() -> datetime:
    return datetime.now()

def today() -> date:
    return date.today()

def calcDate(initDate: date, numOfDays: int) -> date:
    return initDate + timedelta(days=numOfDays)
