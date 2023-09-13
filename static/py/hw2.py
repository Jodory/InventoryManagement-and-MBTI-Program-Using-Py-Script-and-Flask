def hw1():
    # 프로그래밍응용(수5678) / 컴퓨터공학부 / 201812419 / 조성운
    # Problems 1
    total = 0   # 3 또는 5의 배수인 자연수의 합을 구할 변수초기화
    '''
    for문을 이용하여 1부터 999까지 반복되며
    매 반복 당 if문을 이용하여 현재 자연수 i가  3 또는 5의 배수인지 확인한다.
    만약 i가 3 또는 5의 배수라면, 초기화한 변수 total에 i값을 더해주고,
    그렇지 않을 시, 다시 반복문을 수행한다.
    '''
    for i in range(1, 1000):    
        if i % 3 == 0 or i % 5 == 0:
            total += i
    #결과 출력
    return print(f'Result: {total}')



def hw2():
    a = "This is EC736!"
    b = "So fun!"
    c = "Hello World!"
    d = "Print!"
    print(a)
    b
    print(c)
    d
    return