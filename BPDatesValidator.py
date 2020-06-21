from term_style import ctyle

import csv, sys, os, fnmatch
from datetime import datetime, date, timedelta


# This script helps with an application fo British Pasport / Citizenship.
# There are several requirements for you if willing to apply.
# In terms of your history of stay in the UK you must be:
#   *   not more than 450 days in total outside of the UK in last 5 years
#   *   not more than 3 months (~90 days) in total outside of the UK
#       in last 12 months
#   *   not more than 6 months in total (180 days) in total outside of
#       the UK in ANY 12-month period within last 5 years
#
# This script calculates that for you. 
# It needs a CSV file with list of your flights in format:
#
# DepartDateTime,DepartPlace,IsUK,ArrivePlace,IsUK,Airline,FlNumber,WasCancelled
#
#   where:
#       DepartDateTime => DD/MM/YY HH:MM or DD/MM/YYYY or DD/MM/YY
#       IsUK, IsUK, WasCancelled => "True" or "TRUE" or 1 for True, else False
#       DepartPlace, ArrivePlace, Airline, FlNumber => not critical
#
#   CSV file example (example.scv):
#       17/05/10 10:40,HHN,FALSE,EDI,TRUE,RyanAir,FR4382,TRUE
# 
# Please run script with date as additional arg, eg:
#   >   python3 BPDatesValidator.py 101220
#   where:
#       101220 translates to 10 October 2020 (format DDMMYY)


def colOrCol(color_1, color_2, condition, text):
    return f'{color_1 if condition else color_2}{text}{ctyle.END}'


def grnOrRed(condition, text):
    return colOrCol(ctyle.GRN, ctyle.RED, condition, text)


class dateX(date):
    def __str__(self):
        return f'{self:%d/%m/%Y}'
    def firstDay(self):
        return self.replace(day=1)
    def lastDay(self):
        next_month = self.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)
    def shiftDay(self, days):
        return self + timedelta(days=days)
    def shiftMonth(self, months):
        month = self.month - 1 + months
        year = self.year + month // 12
        month = month % 12 + 1
        return type(self)(year, month, self.day)
    def shiftYear(self, years):
        return self.shiftMonth(years * 12)
    def replace(self, year=None, month=None, day=None):
        """Return a new date with new values for the specified fields."""
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        return type(self)(year, month, day)

class datetimeX(datetime):
    def __str__(self):
        return f'{self:%d/%m/%Y %H:%M}'

class Flight:
    def __init__(self, date, origin, originUK, destin, destinUK):
        self.date = date
        self.origin = origin
        self.originUK = originUK
        self.destin = destin
        self.destinUK = destinUK

    def getDate(self):
        return self.date

class Period:
    def __init__(self, dateFrom, dateTo):
        self.dateFrom = dateFrom
        self.dateTo = dateTo

    def getDateFrom(self):
        return self.dateFrom

class Day:
    def __init__(self, date, abroad):
        self.date = date
        self.abroad = abroad

    def getDate(self):
        return self.date

    
#######################################################

if len(sys.argv)>1:
    dateTemp = datetimeX.strptime(sys.argv[1].strip(), '%d%m%y').date()
    dateApply = dateX(dateTemp.year, dateTemp.month, dateTemp.day)
else:  
    print(f'{ctyle._RED} Error:{ctyle.END}{ctyle.RED} Missing Argument{ctyle.END}{ctyle.G}\n\tEnter the date of UK passport application, '
          f'in format {ctyle.END}{ctyle.GRN}DDMMYY{ctyle.END}{ctyle.G}, e.g:{ctyle.END}\n\t> {ctyle.BLU}python3 {sys.argv[0].strip()} {ctyle.GRN}020223{ctyle.END}')
    sys.exit();
    
flights = []
errors = []
cancelled = []

counter = 0
totalUK = 0
totalEUR = 0
totalERR = 0
date5YStarDone = False
date5YDone = False
date1YStarDone = False
date1YDone = False

date5YStar = dateApply.lastDay().shiftYear(-5).shiftDay(1)
date1YStar = dateApply.lastDay().shiftYear(-1).shiftDay(1)

date5Y = dateApply.shiftYear(-5).shiftDay(1)
date1Y = dateApply.shiftYear(-1).shiftDay(1)
dateOld = date5Y.firstDay()

path = os.path.dirname(os.path.abspath(__file__))
my_file = [os.path.join(path, i) for i in os.listdir(path) if fnmatch.fnmatch(i, "*.csv")][0]

print(f'\n{ctyle.U}READING ENTRIES (FLIGHTS) IN THE CSV FILE, \n{my_file}:{ctyle.END}')
with open(my_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    flight_count = 0
    cancelled_count = 0
    for ro in csv_reader:
        try:
            dateTemp = datetime.strptime(ro[0].strip(), '%d/%m/%y %H:%M').date()
        except ValueError:
            try:
                dateTemp = datetime.strptime(ro[0].strip(), '%d/%m/%y').date()
                pass
            except ValueError:
                try:
                    dateTemp = datetime.strptime(ro[0].strip(), '%d/%m/%Y').date()
                    pass
                except ValueError:
                    errorTxt = f'{ctyle.RED}CSV file error: Flight Date {ro[0]} Has Wrong Format{ctyle.END}'
                    print(f'{ctyle._RED} Error {ctyle.END} {errorTxt}')
                    errors.append([flight_count+cancelled_count, errorTxt])
                    pass
            
        dt = dateX(dateTemp.year, dateTemp.month, dateTemp.day)
        ro[2] = True if ro[2] == "TRUE" or ro[2] == "True" or ro[2] == 1 else False
        ro[4] = True if ro[4] == "TRUE" or ro[4] == "True" or ro[4] == 1 else False
        ro[7] = True if ro[7] == "TRUE" or ro[7] == "True" or ro[7] == 1 else False

        if not ro[7]: # check if the flight not been cancelled
            flights.append(Flight(dt, ro[1], ro[2], ro[3], ro[4]))
            flight_count += 1
        else:
            cancelled.append([dt, ro[1], ro[2], ro[3], ro[4]])
            cancelled_count += 1
        ro[5] = ro[5] if ro[5] else f'{ctyle.PNK_D}unknown{ctyle.END}'
        ro[6] = ro[6] if ro[6] else f'{ctyle.PNK_D}unknown{ctyle.END}'
        print(f'{ctyle.G+"CANCELd" if ro[7] else flight_count}\tFlight on {dt}'
              f' from {grnOrRed(ro[2], ro[1])}'
              f'{ctyle.G if ro[7] else ""} to {grnOrRed(ro[4], ro[3])}'
              f'{ctyle.G if ro[7] else ""} by {ro[5]} with number {ro[6]}{ctyle.END}')
    print(f'Processed {flight_count + cancelled_count} lines ({flight_count} flights + {cancelled_count} cancelled).')

if cancelled:
    print(f'{ctyle.G}-----------------------------------------------{ctyle.END}')
    print("CANCELLED:")
    i = 0
    for ca in cancelled:
        i += 1
        print(f"{i}. \t{ca[0]:%d/%m/%y}: from {ca[1]} "
            f"({'UK' if ca[2] else 'NON-UK'}) to {ca[3]} "
            f"({'UK' if ca[4] else 'NON-Uk'}) ")

flights.sort(reverse=False, key=Flight.getDate)

print(f'{ctyle.G}-----------------------------------------------{ctyle.END}')
print(f'\n{ctyle.U}ANALYSING THE FLIGHTS:{ctyle.END}')
dateFirst = flights[0].date
wasUK = flights[0].originUK
destinOld = "UK" if wasUK else "NON-UK"
date1YDiff = False if date1YStar == date1Y else True
date5YDiff = False if date5YStar == date5Y else True
total5Y = 0
total1Y = 0
for ro in flights:
    
    txt2print = []
    delta_1 = (ro.date - dateOld).days if counter else (dateFirst - ro.date).days
    # print(f'{delta_1} test')
    error = True if (not wasUK and ro.originUK) or (wasUK and not ro.originUK) else False

    delta_2 = 0
    if ro.date > date5Y:
        
        if not date5YDone:
            date5YDone = True
            delta_2 = (ro.date - date5Y).days
            txt2print.append(f'{ctyle.YEL}------- {date5Y} 5 year --------{ctyle.END}')
            total5Y += 0 if wasUK else delta_2 
        else:
            total5Y += 0 if wasUK else delta_1 
        
        if ro.date > date5YStar:
            if not date5YStarDone:
                date5YStarDone = True
                delta_2 = delta_2 if delta_2 else (ro.date - date5YStar).days
                txt2print.append(f'{ctyle.G}------- {date5YStar} 5 year (*) ----{ctyle.END}')
        
            if ro.date > date1Y:
                if not date1YDone:
                    date1YDone = True
                    delta_2 = delta_2 if delta_2 else (ro.date - date1Y).days
                    txt2print.append(f'{ctyle.YEL}------- {date1Y} 12 month ------{ctyle.END}')
                    total1Y += 0 if wasUK else delta_2
                else:
                    total1Y += 0 if wasUK else delta_1 

                if ro.date > date1YStar:
                    if not date1YStarDone:
                        date1YStarDone = True
                        delta_2 = delta_2 if delta_2 else (ro.date - date1YStar).days
                        txt2print.append(f'{ctyle.G}------- {date1YStar} 12 month (*) --{ctyle.END}')

    
    delta_1 = delta_1 - delta_2
    
    if not error:
        if wasUK:  # UK
            print(f'{ctyle.BLU}UK \t{delta_1} days{ctyle.END}')
            totalUK += delta_1
        else:  # NON-UK
            print(f'{ctyle.PNK}NON-UK \t{delta_1} days{ctyle.END}')
            totalEUR += delta_1
    
    for line in txt2print:
        print(line)

    if not error and delta_2:
        if wasUK:  # UK
            print(f'{ctyle.BLU}UK \t{delta_2} days{ctyle.END}')
            totalUK += delta_1
        else:  # NON-UK
            print(f'{ctyle.PNK}NON-UK \t{delta_2} days{ctyle.END}')
            totalEUR += delta_1

    if error:
        errorTxt = (f'{ctyle.RED}{delta_1}d {destinOld}@{dateOld:%d/%m/%y}{ctyle.END} '
                    f'{"UK" if wasUK  else "NON-UK"} - {"UK" if ro.originUK  else "NON-UK"} '
                    f'{ro.origin}@{ro.date:%d/%m/%y}')
        print(f'{ctyle._RED} Error {ctyle.END} {errorTxt}')
        totalERR += delta_1
        errors.append([counter, errorTxt])
        

    print(f'\t{ro.date} from {ro.origin}'
          f' to {ro.destin} {ctyle.G}{total5Y}, {total1Y}{ctyle.END}')
    counter += 1
    dateOld = ro.date
    destinOld = ro.destin
    wasUK = ro.destinUK
print(f'{ctyle.GRN if wasUK else ctyle.RED}{(dateApply - dateOld).days} days stay in UK{ctyle.END}')
print(f'{ctyle.YEL}------- {dateApply} Applying ------{ctyle.END}')
dateApplyStar = dateApply.lastDay()
if not dateApply == dateApplyStar:
    print(f'{ctyle.GRN if wasUK else ctyle.RED}{(dateApplyStar - dateApply).days} days stay in UK{ctyle.END}')
    print(f'{ctyle.G}------- {dateApplyStar} Applying (*) --{ctyle.END}')



dayList = []
rangeList = []
counter = 0
for ro in flights:
    if ro.date > date5Y:
        if counter and not ro.originUK and not wasUK: 
            rangeList.append(Period(dateOld if date5Y < dateOld else date5Y, ro.date))
    counter += 1
    dateOld = ro.date
    destinOld = ro.destin
    wasUK = ro.destinUK

days = 0
while dateTemp<dateApplyStar:
    dateTemp = date5Y.shiftDay(days) 
    status = False
    for rg in rangeList:
        if dateTemp > rg.dateFrom and dateTemp < rg.dateTo:
            status = True
            break
    dayList.append(Day(dateTemp, status))
    days += 1

cuntMax = 0
for month in range(0,50):
    dateFrom = date5Y.shiftMonth(month).firstDay()
    dateTo = date5Y.shiftMonth(month+11).lastDay()
    
    cunt = 0 
    for day in dayList:
        if day.date >= dateFrom and day.date <= dateTo:
            cunt += 1 if day.abroad else 0
        
    # print(f'{month} \t{dateFrom} - {dateTo}: {cunt}')
    cuntMax = cuntMax if cuntMax > cunt else cunt
print(f'{ctyle.G}-----------------------------------------------{ctyle.END}')
print(f'Applying Period:        {date5Y} - {dateApply}')
print(f'12-Month Period:        {date1Y} - {dateApply}')
print(f'{ctyle.G}-----------------------------------------------{ctyle.END}')
print(f'Total outside UK (12M): '
      f'{ctyle.GRN if total1Y<90 else ctyle.RED}{total1Y}{ctyle.G}d (Max 3M) ≈> {10*total1Y/9:.1f}%{ctyle.END}')
print(f'Total outside UK (5Y):  '
      f'{ctyle.GRN if total5Y<450 else ctyle.RED}{total5Y}{ctyle.G}d (Max 450d) => {10*total5Y/45:.1f}%{ctyle.END}')
print(f'Outside UK (any 12-M):  '
      f'{ctyle.GRN if cuntMax<180 else ctyle.RED}{cuntMax}{ctyle.G}d (Max 6M) ≈> {10*cuntMax/18:.1f}%{ctyle.END}')
print(f'{ctyle.G}-----------------------------------------------{ctyle.END}')
print(f'Total outside UK:       {totalEUR}{ctyle.G}d ({totalEUR/365:.1f} year){ctyle.END}')
print(f'Total in UK:            {totalUK}{ctyle.G}d ({totalUK/365:.1f} year){ctyle.END}')
if errors:
    print(f'{ctyle.G}-----------------------------------------------{ctyle.END}')
    print(f'Total in ERR:           {totalERR}{ctyle.G}d ({totalERR/365:.1f} year){ctyle.END}')
    i = 0
    for er in errors:
        i += 1
        print(f'{i}. \t{er[1]}')
    
print()
# for ro in rangeList:
#     print(f'\t{ro.dateFrom} - {ro.dateTo}')
