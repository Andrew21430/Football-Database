def one_award(trophy):
    print(str(trophy))
    test=filter(str.isdecimal,str(trophy))
    print(str(test))
    fixedtest = "".join(test)
    singletest= list(fixedtest)
    for i in range(0,10):
        singletest.pop(0)
    print(singletest)
    print(singletest[-1])


one_award("http://127.0.0.1:5000/award/?tropies=6")