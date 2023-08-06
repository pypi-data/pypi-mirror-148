import time


def guide():
    print('======================================================================')
    print('欢迎下载我的第三方模块0.0.2版')
    print('Welcome to download my third-party module-0.0.2')
    time.sleep(2)
    print('==========================================================================================')
    print('本模块是由多人连个完成的模块')
    print('==========================================================================================')
    print('author/name/connecting_point/connecting_point_tester')
    print('请输入需要查询的函数 ')
    print('Please enter the function that you want to query')
    guide_to_print = input('')
    print('==========================================================================================')
    print('正在查询')
    print('==========================================================================================')
    if guide_to_print == 'author':
        print('这是一个介绍开发者的函数，用法如下')
        print('This is a function that introduces author and is used as follows')
        print('==========================================================================================')
        print('guide.guide()')
        print('==========================================================================================')
    elif guide_to_print == 'name':
        print('这是一个名字检测函数,用法如下')
        print('This is a name detection function and is used as follows')
        print('==========================================================================================')
        print('name.name()')
        print('==========================================================================================')
    elif guide_to_print == 'connecting_point':
        print('这是一个连点器,用法如下')
        print('this is a connecting point and is used as follows')
        print('==========================================================================================')
        print('connecting_point.connecting_point()')
        print('==========================================================================================')
    elif guide_to_print == 'connecting_point_tester':
        print('这是一个连点器测试器,用法如下')
        print('This is a connecting point tester and is used as follows')
        print('==========================================================================================')
        print('connecting_point_tester.connecting_point_tester()')
        print('==========================================================================================')
    else:
        print('本模块暂时没有这个功能，尽情期待！')
        print('This module does not have this function for the time being, so enjoy it!')
        print('==========================================================================================')
    print('本模块将发展为很会玩的模块')
    print('This module will evolve into a very playable module')
    print('==========================================================================================')
    time.sleep(2)
    print('如果你有好的提议请联系开发者邮箱：liuniandexiaohuo@qq.com')
    print('If you have a good proposal, please contact the developer email: liuniandexiaohuo@qq.com')
    print('==========================================================================================')
    time.sleep(3)
    print('我会在看到邮件后第一时间回复你')
    print('I will reply to you as soon as I see the email')
    print('==========================================================================================')



