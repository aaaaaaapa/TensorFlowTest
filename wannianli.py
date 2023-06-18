import calendar


def show_calendar(year, month):
    # 获取指定年月的日历
    cal = calendar.monthcalendar(year, month)

    # 打印月份名称和年份
    print(calendar.month_name[month], year)

    # 打印星期名称
    print("Mo Tu We Th Fr Sa Su")

    # 遍历每周
    for week in cal:
        # 遍历每天
        for day in week:
            if day == 0:
                print("   ", end=" ")
            else:
                print("%2d" % day, end=" ")
        print()


# 输入年月
year = int(input("Enter year: "))
month = int(input("Enter month: "))

# 调用函数，显示万年历
show_calendar(year, month)
