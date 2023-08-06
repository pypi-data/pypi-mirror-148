def connecting_points():
    import pyautogui as pg
    import time
    print('请输入连点次数')
    print('Please enter the number of consecutive dots')
    times = input('')
    times = int(times)
    print('十秒后开始连点/Start in ten seconds')
    time.sleep(10)
    for x in range(times):
        pg.click()
