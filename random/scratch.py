from datetime import date

princ = 2500
rate = .05
runningInterest = 0
rateperday = rate/365
payment = 100
begin = date(2018, 8, 10)
p1 = date(2018, 8, 31)
p2 = date(2018, 9, 30)
p3 = date(2018, 10, 30)
p4 = date(2018, 12, 1)
p5 = date(2019, 1, 1)

paydays = [begin, p1, p2, p3, p4, p5]

for date in range(len(paydays)):
    while (date != len(paydays)-1):
        d0 = paydays[date]
        d1 = paydays[date+1]

        numberofdays = d1 - d0
        print("Number of days between " + str(d0) + " and " + str(d1) + ": " + str(numberofdays.days))

        interest = 0
        for i in range(numberofdays.days):
            total = runningInterest + princ
            runningInterest += (total * rateperday)
            interest += (total * rateperday)
        princ -= payment

        print("Interest accrued between above dates: " + str(interest))

        break
print("Final interest:" + str(runningInterest))
print("Final Principal: " +str(princ))

print("Final total: " + str(princ + runningInterest))
