def hw1():
    a = "This is EC736!"
    b = "So fun!"
    c = "Hello World!"
    d = "Print!"
    print(a)
    b
    print(c)
    return d

def hw2():
    #a.1 = 10
    #a.1
    return

def hw3():
    a = "Hello"
    return int(a)

def hw4():
    a = float('inf')
    return print(a)

def hw5():
    x = 1/3.0
    y = 7
    z = 'hi'
    return print('x = %.3f, y = %d, z = %s' % (x, y, z))
    

def hw6():
    myVariable = 3.21548
    print("myvariable = %3.2f" % myVariable)
    print("myvariable = %6.2f" % myVariable)
    print("myvariable = %9.2f" % myVariable)
    return

def hw7():
    a = 8.45296
    print(int(a))
    print(a)
    b = int(a)
    print(a,b)
    print('a = %.1f, b = %3.f' %(a,b))
    print('a = ', a, ', b = ', b)
    return

def hw8():
    a = [1,3,4]
    return a[3]

def hw9():
    myList = []
    myList.append(50)
    print(myList)
    myList[0] = 100
    print(myList)
    myList.append('Bulls')
    print(myList)
    return

def hw10():
    a = 12.7e14
    b = float('inf ')
    if( a<b):
        print(a)
    else:
        print('this is the greatest class ever ')
    return

def hw11():
    adj = ["red", "big", "tasty"]
    fruits = ["apple", "banana", "cherry"]
    for x in adj:
        for y in fruits:
            print(x, y)
    return