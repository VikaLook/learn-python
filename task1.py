from datetime import datetime

# log_data.txt
open_book = input('Enter the file name: ')
try:
    book = open(open_book)
except FileNotFoundError:
    print('File cannot be opened:', open_book)
# book = open('log_data.txt')

# fulfill the first array with data from the file
# cast date strings to real dates
my_list = []
for line in book:
    row = line.split()
    my_list.append((datetime.strptime(row[1], "[%d/%b/%Y:%H:%M:%S]").date(), row[0], row[2]))
# print(len(my_list))

# sort the list to be able to compare rows with previous rows and find sums of sizes for each ip on each date
my_list.sort()

# calculate sums of sizes for each ip on each date
my_list_2 = []
prev_date = my_list[0][0]
# print(prev_date)
prev_ip = my_list[0][1]
# print(prev_ip)
sizes_sum = 0
for row in my_list:
    if row[0] == prev_date and row[1] == prev_ip:
        sizes_sum = sizes_sum + int(row[2])
    else:
        my_list_2.append((prev_date, prev_ip, sizes_sum))
        prev_date = row[0]
        prev_ip = row[1]
        sizes_sum = int(row[2])

my_list_2.append((prev_date, prev_ip, sizes_sum))
# print(len(my_list_2))

# remove duplicates (leave ips with the same maximum sizes sum)
my_list_3 = []
prev_date = None
max_sizes_sum = 0
for row in my_list_2:
    if row[0] == prev_date:
        if row[2] > max_sizes_sum:
            max_sizes_sum = row[2]
    else:
        my_list_3.extend(item for item in my_list_2 if item[0] == prev_date and item[2] == max_sizes_sum)
        prev_date = row[0]
        max_sizes_sum = row[2]

my_list_3.extend(item for item in my_list_2 if item[0] == prev_date and item[2] == max_sizes_sum)

# print(my_list_3)
# print(len(my_list_3))

for x in my_list_3:
    # print("{} - {}: {}".format(x[0].strftime("%d/%b/%Y"), x[1], x[2]))
    print("{} - {}".format(x[0].strftime("%d/%b/%Y"), x[1]))

