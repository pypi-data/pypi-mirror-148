from time import sleep
def colorful_output(object, times, colorful_ft, color_m, list_m, time_m):
    x=0
    object2=list(object)
    if colorful_ft == 0:
        for i in object2:
            print(i, end='')
            if times == -1:
                sleep(float(time_m[x]))
                x+=1
            else:
                sleep(times)
    elif colorful_ft == 1:
        if color_m != -1:
            x=0
            for i in object2:
                print("\033["+str(color_m)+"m"+i+"\033[0m", end='')
                if times == -1:
                    sleep(float(time_m[x]))
                    x+=1
                else:
                    sleep(times)
                    x+=1
        elif color_m == -1:
            x=0
            for i in object2:
                print("\033["+str(list_m[x])+"m"+i+"\033[0m", end='')
                if times == -1:
                    sleep(float(time_m[x]))
                    x+=1
                else:
                    sleep(times)
                    x+=1
        else:
            print("\033[31mWarning: PLease answer a number.\033[0m")
    else:
        print("\033[31mWarning: Please answer 1/0.\033[0m")