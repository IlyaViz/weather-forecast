import datetime

def date_str_to_date_instance(date_str):
    """ date_str in format like 2023-08-15 """
    return datetime.date(*map(lambda x: int(x), date_str.split("-")))
