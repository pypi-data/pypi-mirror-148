def to_time_string(estimated_time):
    time_string = ''
    if not estimated_time:
        time_string = 'N/A'
    elif 'H' in estimated_time and 'M' in estimated_time:
        hours = estimated_time.split('T')[1].split('H')[0]
        minutes = estimated_time.split('T')[1].split('H')[1].split('M')[0]
        time_string = hours + ' Hrs ' + minutes + ' Mins'
    elif 'H' in estimated_time and 'M' not in estimated_time:
        hours = estimated_time.split('T')[1].split('H')[0]
        minutes = 0
        time_string = hours + ' Hrs'
    else:
        hours = 0
        minutes = estimated_time.split('T')[1].split('M')[0]
        time_string = minutes + ' Mins'
    return time_string


def to_string(hours, minutes):
    data_string = ''
    if hours and minutes:
        data_string = 'PT' + str(hours) + 'H' + str(minutes) + 'M'
    elif hours and not minutes:
        data_string = 'PT' + str(hours) + 'H'
    elif not hours and minutes:
        data_string = 'PT' + str(minutes) + 'M'
    return data_string
