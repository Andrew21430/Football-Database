def Hollow_diamond(size):
    row = []
    increase = 0
    for i in range(1,size+1):
        increase = increase - i
        spaces = size - i
        if i == 1:
            row.append(' '*spaces +'*'+ ' '*spaces)
        else:
            line = ' '*spaces + '*' + ' '*(((i-1)*2)-1) + '*' + ' '*spaces
            row.append(line)
            if i == size:
                for x in range(1 ,i):
                    spaces = size - (i-x)
                    if x == i-1:
                        row.append(' '*spaces + '*')
                    else:
                        line = ' '*spaces + '*' + ' '*((((i-x)-1)*2)-1) + '*'
                        row.append(line)
    return row



for i in range(0,len(Hollow_diamond(10))):
    print(Hollow_diamond(10)[i])

