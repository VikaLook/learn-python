# task 2 - result display the least number of requests and hour of day
# log_data.txt
file_open = input('Enter the file name: ')
try:
    file_read = open(file_open, 'r', encoding='utf-8')
except FileNotFoundError:
    print('File cannot be opened:', file_open)

counts = dict()
for line in file_read:
    words = line.split()
    date = words[1]
    hours = date[1:15]
    counts[hours] = counts.get(hours, 0) + 1
sorted_d = [(v, k) for k, v in counts.items()]
print(min(sorted_d))
exit()
