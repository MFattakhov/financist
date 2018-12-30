from datetime import datetime


def dating():
    today = datetime.today()
    return '.'.join(str(today)[:10].split('-'))
