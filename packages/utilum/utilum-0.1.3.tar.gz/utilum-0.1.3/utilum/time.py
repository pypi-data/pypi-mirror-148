def splitStrDateTime(dash_datetime):
    year,month,day,hour,minute,second,msec=dash_datetime.split("_")
    return year,month,day,hour,minute,second,msec


def twentyFourToTwelveLower(hour, minute):
    ihour=int(hour)
    if(ihour>=12):
        ihour=ihour-12
        message=f'''{str(ihour)}:{minute} pm'''

    else:
        message=f'''{str(ihour)}:{minute} am'''

    return message


def twentyFourToTwelveUpper(hour, minute):
    ihour=int(hour)
    if(ihour>=12):
        ihour=ihour-12
        message=f'''{str(ihour)}:{minute} PM'''

    else:
        message=f'''{str(ihour)}:{minute} AM'''

    return message


def getStringDateTimeMessage(dash_datetime, number_to_month):
    year,month,day,hour,minute,second,msec=splitStrDateTime(dash_datetime)

    if(month[0]=="0"):month=month[1]
    month_stream=number_to_month[month]
    message=f'''{month_stream} {day}, {year} at {twentyFourToTwelveLower(hour, minute)}'''

    return message