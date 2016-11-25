def manual():
    print('entering manual mode')
    while True:
        c = input('')
        x = c.split(' ')
        try:
            if x[0] == 'b':
                print('Manual buying')
            elif x[0] == 's':
                print('Manual selling')
            elif x[0] == 'q':
                return False
            elif x[0] == 'c':
                return True
        except:
            continue
