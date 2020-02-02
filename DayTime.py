import datetime



class workDays():
    def __init__(self, start_date, end_date, days_off=None):
        
        self.start_date = start_date
        self.end_date = end_date
        self.days_off = days_off
        if self.start_date > self.end_date:
            self.start_date, self.end_date = self.end_date, self.start_date
        if days_off is None:
            self.days_off = 5, 6
      
        self.days_work = [x for x in range(7) if x not in self.days_off]

    def workDays(self):
       
        # 还没排除法定节假日还有那些teacher trainingday...
        tag_date = self.start_date
        while True:
            if tag_date > self.end_date:
                break
            if tag_date.weekday() in self.days_work:
                yield tag_date
            tag_date += datetime.timedelta(days=1)

    def daysCount(self):
       
        return len(list(self.workDays()))


era = datetime.date(2019,11,11)
print('Please type in the current day number in the format of：YYYY-MM-DD')
dateinput = input()
dateinput = dateinput.split('-')
y = int(dateinput[0])
m = int(dateinput[1])
d = int(dateinput[2])

b = datetime.date(y,m,d)
work = workDays(era,b)
print(work.daysCount())
re = work.daysCount()%8
if re == 0 :
    print('It is : Day 8')
else:
    print('\nToday is: DAY', re)