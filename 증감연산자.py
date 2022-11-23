year = 2010
while year <= 2021:
    print(year)
    year += 1
    mon = 1
    while mon <= 12:
        print(mon)
        mon = format(mon, '02')
        mon = int(mon)
        mon += 1