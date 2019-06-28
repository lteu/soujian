from datetime import datetime
timestamp = 1394473386
a = datetime.fromtimestamp(timestamp)

s1 = a.strftime("%Y%m%d")
# mm/dd/YY H:M:S format
print("s1:", s1)



# print( a.year,a.month,)
# print("type(dt_object) =", type(dt_object))