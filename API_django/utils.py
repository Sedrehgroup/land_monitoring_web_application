from dateutil.relativedelta import *
import jdatetime


def return_before(geom, after, month):
    before = after - relativedelta(months=month)
    before_jalali = jdatetime.date.fromgregorian(date=before)
    beforeURL = f'zamin2:{geom}_TCI_{before_jalali.strftime("%Y%m")}'
    return beforeURL


def return_all(geom, before, after):
    beforeURL = f'zamin2:{geom}_TCI_{before}'
    afterURL = f'zamin2:{geom}_TCI_{after}'
    return beforeURL, afterURL