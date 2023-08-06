from time import sleep
from os import system
from rich import print as rich_print
from rich.console import Console
try:
    import traceback
except:
    import traceback2
m_list = []
m_time = []
rgbs = []
#创建console实例
console = Console()
try:
    # answer=input("请输入是否要用RGB表示颜色（1/0）：")
    # if answer == '1':
    #     r = input("请输入颜色RED度数（0~255）：")
    #     g = input("请输入颜色GREEN度数（0~255）：")
    #     b = input("请输入颜色BLUE度数（0~255）：")
    #     subject=input("请输入输出的内容：")
    #     yrgb="rgb("+r+","+g+","+b+")"
    #     console.print(subject,style=yrgb)
    # print("""\033
    # [1m[3m[4m[7m[9m
    #
    # （全部是底色）
    # """)
    # print("\033[1m1m加粗;\033[0m", end='');print("\033[3m3m斜体;\033[0m", end='')
    # print("\033[4m4m划线;\033[0m", end='');print("\033[7m7m白底;\033[0m", end='')
    # print("\033[9m9m划去;\033[0m", end='');print("\033[21m21m粗划线;\033[0m", end='')
    # print("\033[51m51m加方框;\033[0m", end='\n');print("\033[30m30m黑色;\033[0m", end='')
    # print("\033[31m31m红色;\033[0m", end='');print("\033[32m32m绿色;\033[0m", end='')
    # print("\033[33m33m黄色;\033[0m", end='');print("\033[34m34m蓝色;\033[0m", end='')
    # print("\033[35m35m紫色;\033[0m", end='');print("\033[36m36m淡蓝;\033[0m", end='')
    # print("\033[37m37m灰色;\033[0m", end='\n')
    # print("\033[41m41m红色;\033[0m", end='');print("\033[42m42m绿色;\033[0m", end='')
    # print("\033[43m43m黄色;\033[0m", end='');print("\033[44m44m蓝色;\033[0m", end='')
    # print("\033[45m45m紫色;\033[0m", end='');print("\033[46m46m淡蓝;\033[0m", end='')
    # print("\033[47m47m灰色\033[0m", end='');print("\033[40m40m黑底;\033[0m", end='\n')
    dict = {'1': "1m加粗", '3': "3m斜体", '4': "4m划线", '7': "7m白底", '9': "9m划去", '21': "21m粗划线", '51': "51m加方框",
            '30': "30m黑色", '31': "31m红色", '32': "32m绿色", '33': "33m黄色", '34': "34m蓝色", '35': "35m紫色", '36': "36m淡蓝",
            '37': "37m灰色",
            '41': "41m红色", '42': "42m绿色", '43': "43m黄色", '44': "44m蓝色", '45': "45m紫色", '46': "46m淡蓝", '47': "47m灰色",
            '40': "40m黑底"}
    for k, v in dict.items():
        if k == "51" or k == "37" or k == "40":
            print("\033[" + k + "m" + v + "\033[0m", end="\n")
        else:
            print("\033[" + k + "m" + v + "\033[0m", end="")
    object = input("\033[36m请输入逐字输出内容：\033[0m")
    oft = input("\033[35m请输入是否要彩色输出（0/1）：\033[0m")
    if oft == "1":
        mft = input("\033[34m请输入是否每个字的颜色不一样（0/1）：\033[0m")
        if mft == "1":
            m = -1
            for j in range(len(object)):
                question = "\033[36m请输入第" + str(j + 1) + "个字的颜色代码（不用写‘m’）：\033[0m"
                ml = input(question)
                m_list.append(ml)
        else:
            l = input("\033[33m请输入颜色代码（不用写‘m’）：\033[0m")
    else:
        m = -1
    tm = input("\033[32m请输入是否每个字等待秒数不一样（0/1）：\033[0m")
    if tm == "1":
        for n in range(len(object)):
            questions = "\033[35m请输入第" + str(n + 1) + "个字的等待秒数：\033[0m"
            tm = input(questions)
            m_time.append(tm)
            t = -1
            m = -1
    else:
        t = input("\033[35m请输入逐字输出等待秒数：\033[0m")
        t = float(t)
    def colorful_output(object, times, colorful_ft, color_m, list_m, time_m):
        x = 0
        object = list(object)
        if colorful_ft == 0:
            for i in object:
                print(i, end='')
                if times == -1:
                    sleep(float(time_m[x]))
                    x += 1
                else:
                    sleep(times)
        elif colorful_ft == 1:
            if color_m != -1:
                x = 0
                for i in object:
                    print("\033[" + str(color_m) + "m" + i + "\033[0m", end='')
                    if times == -1:
                        sleep(float(time_m[x]))
                        x += 1
                    else:
                        sleep(times)
                        x += 1
            elif color_m == -1:
                x = 0
                for i in object:
                    print("\033[" + str(list_m[x]) + "m" + i + "\033[0m", end='')
                    if times == -1:
                        sleep(float(time_m[x]))
                        x += 1
                    else:
                        sleep(times)
                        x += 1
            else:
                print("\033[31m不可以输入除了数以外的哦！\033[0m")
        else:
            print("\033[31m不可以输入0或者1以外的数哦！请重新运行一下吧！\033[0m")
    if len(m_list) == 0:
        if str(oft) == '1':
            m = l
    colorful_output(object=object, times=t, colorful_ft=int(oft), color_m=int(m), list_m=m_list, time_m=m_time)
except SyntaxError as Syntax_erorr:
    print("\033[31m代码有无法抵御的错误，请把错误原因发布在评论区，方便作者改进\n错误原因：" + str(Syntax_erorr) + "\033[0m", end='')
except Exception as e:
    print("\033[31m代码有错误，可以把错误原因发布在评论区，方便作者改进\n错误原因：" + str(e) + "\033[0m")
    chaosong_ft = input("\033[34m请输入是否要抄送一份错误信息给您？（1/0）\033[0m")
    if chaosong_ft == '1':
        chaosong_email = input("\033[34m请输入您的邮箱：\033[0m")
        chaosong = True
    else:
        chaosong = False
        print("\033[32m好的\033[0m")
    from tkinter import *
    import subprocess
    def printInfo(e):
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr
        try:
            traceback_object = traceback.format_exc()
        except:
            traceback_object = traceback2.format_exc()
        message = '作品<<<colorful_font_output>>>有错误。\n错误原因：' + str(e) + '\n具体信息：\n' + traceback_object
        def mail():
            ret = True
            try:
                msg = MIMEText(message, 'plain', 'utf-8')
                msg['From'] = formataddr(["Yuli Wang", 'winterland_yuli2@163.com'])
                msg['To'] = formataddr(["Yuli Wang", 'winterland_yuli2@163.com'])
                msg['Subject'] = "错误信息详情"
                server = smtplib.SMTP_SSL('smtp.163.com', 465)
                server.login('winterland_yuli2@163.com', 'AVVIZLIMJHEJRLQL')
                if chaosong:
                    try:
                        server.sendmail('winterland_yuli2@163.com', ['winterland_yuli2@163.com', chaosong_email],msg.as_string())
                    except:
                        print("\033[33m警告：您输入的邮箱是未注册的，请对照以后在输入，谢谢！\033[0m")
                else:
                    server.sendmail('winterland_yuli2@163.com', ['winterland_yuli2@163.com', ], msg.as_string())
                server.quit()
            except Exception:
                ret = False
            return ret
        ret = mail()
        if ret:
            print("\n\033[42m√已经发送给作者邮件：错误信息√\033[4m", end='')
            print("\033[0m\033[0m",end='')
        else:
            print("\n\033[41m×邮件：错误信息发送失败×\033[4m", end='')
    printInfo(e)