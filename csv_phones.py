import re, csv, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='input', help='Store a simple value')
parser.add_argument('-c', action='store', dest='cells', help='Store a simple value')
#parser.add_argument('-p', action='append', dest='providers', help='Store a simple value')
parser.add_argument('-o', action='store', dest='output', help='Store a simple value')
results = parser.parse_args()
input = results.input
cells = results.cells
#providers = results.providers
output = results.output


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)


def handleNumber(num):
    number = re.sub('([\s+)(-])', '', num)
    return number


def getCell(num):
    cell = 0
    if num[0:3] == '380':
        cell = num[3:5]
    elif num[0:1] == '0':
        cell = num[1:3]
    else:
        cell = num[0:2]
    return cell


def toNormalView(num):
    # example +380 (66) 112-51-15
    if num[0:3] != '380':
        if num[0] != '0' and num[0:3] != '380':
            num = '380' + num
        else:
            num = '38' + num
    num = '+' + num
    num = num[0:4] + ' ' + num[4:len(num)]
    num = num[0:5] + '(' + num[5:7] + ') ' + num[7:len(num)]
    num = num[0:12] + '-' + num[13:15] + '-' + num[15:len(num)]

    return num


data_input = open("input.txt", "r", encoding="utf8")
data_phones = []
for line in data_input:
    if line != "\n":
        mask1 = "^\+.*"
        mask2 = "\(.+"
        res1 = re.findall(mask1, line)
        res2 = re.findall(mask2, line)
        if res1:
            nums = res1[0].split(',')
            for num in nums:
                handledNum = handleNumber(num)
                data_phones.append(handledNum)
        if res2:
            nums = res2[0].split(',')
            for num in nums:
                handledNum = handleNumber(num)
                data_phones.append(handledNum)

unique(data_phones)


with open('phones.csv', 'w', encoding="utf-8") as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(["phone"])
    for phone in data_phones:
        cell = getCell(phone)
        numbers = toNormalView(phone)
         print(phone)
