import sys
import datetime
import io

serverName = sys.argv[1]
os = sys.argv[2]
startDate = sys.argv[3]
endDate = sys.argv[4]
reportDir = '/root/server_availability_report/reports/'
fileName = reportDir + os + '/'  + 'serverdowntime_'+serverName+'.txt'

dtList = [line.rstrip('\n') for line in open(fileName)]

#print(dtList)

monthStr = { '01':'Jan', '02': 'Feb' , '03': 'Mar' ,'04' : 'Apr' , '05': 'May' ,'06': 'Jun'  , '07':'Jul' ,'08': 'Aug' , '09' : 'Sep' , '10': 'Oct' , '11':'Nov', '12' :'Dec'}


def find_missing(lst):
    return sorted(set(range(lst[0], lst[-1])) - set(lst))


def time_sum(timeList):
    totalSecs = 0
    for tm in timeList:
        timeParts = [int(s) for s in tm.split(':')]
        totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]

    totalSecs, sec = divmod(totalSecs, 60)
    hr, min = divmod(totalSecs, 60)
    #print(hr, min, sec)
    return "%d:%02d:%02d" % (hr, min, sec)


def getMonthList(startDate,endDate,os):
    numStartMonth = (startDate.split('-'))[1]
    numEndMonth = (endDate.split('-'))[1]
    intList = []
    intList.append(int(numStartMonth))
    intList.append(int(numEndMonth))
    missingSeqInList = find_missing(intList)
    #print('missingSeqInList::',missingSeqInList)
    if os in 'linux':
       startMonth =  monthStr[numStartMonth]
       endMonth = monthStr[numEndMonth]
    else:
       startMonth = str(numStartMonth)
       endMonth = str(numEndMonth)

    monthList = []
    monthList.append(startMonth)
    for num in missingSeqInList:
        strNum = str(num)
        if len(strNum) == 1:
           strNum = '0'+strNum
        if os in 'linux':
           monthList.append(monthStr[strNum])
        else:
           monthList.append(str(strNum))

    monthList.append(endMonth)
    monthList = list(set(monthList))
    #print(monthList)
    return monthList

def getAverageDTLinux(serverName,dtList,startDate,endDate,os):
    #print(os,':',serverName,startDate,endDate)
    monthList = getMonthList(startDate,endDate,os)
    #print(monthList)
    length = len(dtList) - 2
    time_list = []
    time_daysList = []
    for i in range(length):
        data = dtList[i]
        dataArr = data.split()
        if dataArr[5] in monthList:
           #dateSt = dataArr[6] + ' ' + (dataArr[7] if dataArr[7] != '' else dataArr[8])
           timeInHrsMin = dataArr[len(dataArr) - 1]
           timeInHrsMin = timeInHrsMin.replace('(','')
           timeInHrsMin = timeInHrsMin.replace(')','')
           #print(timeInHrsMin)
           if '+' in timeInHrsMin:
              time_daysList.append(int(timeInHrsMin[0:timeInHrsMin.index('+')]))
              timeInHrsMin = timeInHrsMin[timeInHrsMin.index('+') + 1:]
              #print(timeInHrsMin)
           time_list.append('00:'+timeInHrsMin)
    #print(time_list)
    #print("No. of days per month:::",time_daysList)
    totalNoOfDays =  sum(time_daysList)
    total = time_sum(time_list)
    totalShutDownPeriod = str(totalNoOfDays) + " Days and " + total + " hh:mm:ss"
    #print(totalShutDownPeriod)
    return totalShutDownPeriod


if os in ['linux']:
   totalShutDownPeriod = getAverageDTLinux(serverName,dtList,startDate,endDate,os)
   print(totalShutDownPeriod)
