

def check():
    with open('districts.txt') as f:
        lines = f.read().splitlines()
    with open('districts_names.txt') as f:
        things = f.read().splitlines()
        dic = {}
        for x in things:
            y = x.split(':')
            dic[y[0]]=y[1]
    file1 = open('chosen_districts_names.txt', 'w')
    for x in lines:
        str = x + ': ' + dic[x] + '\n'
        file1.write(str)
        print(str)

check()