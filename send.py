import requests
import datetime
import calendar

today = datetime.date.today()

def send():
    weekday = today.weekday()
    youbi = [
            {'key': '月', 'value': '可燃ゴミ'},
            {'key': '火'},
            {'key': '水', 'value': '資源ゴミ'},
            {'key': '木', 'value': '可燃ゴミ'},
            {'key': '金'},
            {'key': '土', 'value': 'ペットボトル'},
            {'key':'日'}
    ]


    dutyMember = ['同居人のリスト']
    token = 'LINE Notifyから取得したトークン'
    url = 'https://notify-api.line.me/api/notify'
    gomiList = getGomiDay()
    gomiListLength = len(gomiList)

    ##年末年始はゴミ収集しない処理--start--
    newYearsList = []
    #年を跨ぐとその年の12-29から日付を取得してしまうので1年前の日付も用意
    #TODO:好きな書き方では無いから要リファクタリング
    startDay = datetime.date(today.year-1,12,29)
    startNewDay = datetime.date(today.year,12,29)
    deltaDay = datetime.timedelta(days=1)
    if (today.month == 12 or today.month == 1):
        for i in range(6):
            newYearsList.append(startDay)
            newYearsList.append(startNewDay)
            startDay += deltaDay
            startNewDay += deltaDay
        if datetime.date.today() in newYearsList:
            return
    #年末年始はゴミ収集しない処理--end--

    if today.day in gomiList:
        index = gomiList.index(today.day)
        message = '\n今日は{}月{}日({}) {}の日です。\n当番は{}さんです。'.format(today.month, today.day, youbi[weekday]['key'], youbi[weekday]['value'], dutyMember[index])
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + token}
        r = requests.post(url, data=payload, headers=headers)

def getGomiDay():
    month = today.month
    year = today.year
    monList = [x[calendar.MONDAY] for x in calendar.monthcalendar(year, month)]
    wedList = [x[calendar.WEDNESDAY] for x in calendar.monthcalendar(year, month)]
    thursList = [x[calendar.THURSDAY] for x in calendar.monthcalendar(year, month)]
    satList = [x[calendar.SATURDAY] for x in calendar.monthcalendar(year, month)]
    petSatList = [x for x in satList if x > 0]
    petSatList = petSatList[::2]
    gomiList = monList + wedList + thursList + petSatList
    gomiList = [x for x in gomiList if x > 0]
    gomiList.sort()
    return gomiList


if __name__ == '__main__':
    send()
