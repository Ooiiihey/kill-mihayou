import os, re, sys, time, psutil, webbrowser
import ctypes

host_windows = r"C:\Windows\System32\drivers\etc\hosts"

HOST_BAN = ["127.0.0.1 ys.mihoyo.com",
            "127.0.0.1 mhyy.mihoyo.com",
            "127.0.0.1 ys.mihoyo.com/cloud/#/",
            "127.0.0.1 www.yuanshen.com",
            "127.0.0.1 www.miyoushe.com",
            "127.0.0.1 bh3.mihoyo.com",
            "127.0.0.1 api-static.mihoyo.com",
            "127.0.0.1 www.mihoyo.com",
            "127.0.0.1 cg.163.com",
            "127.0.0.1 genshin.hoyoverse.com",
            "127.0.0.1 user.mihoyo.com",
            "127.0.0.1 game.bilibili.com",
            "127.0.0.1 genshin.mihoyo.com",
            "127.0.0.1 api-takumi.mihoyo.com",
            "127.0.0.1 hk4e-api.mihoyo.com",
            "127.0.0.1 www.jiyoushe.cn",
            "127.0.0.1 start.qq.com",
            "127.0.0.1 gamer.qq.com",
            "127.0.0.1 yowa.huya.com",
            "127.0.0.1 www.suileyoo.com",
            "127.0.0.1 y.4399.com",
            "127.0.0.1 www.migufun.com",
            "127.0.0.1 www.movingcloudgame.com",
            "127.0.0.1 cloudgame.douyu.com",
            "127.0.0.1 box3.yunjiwan.com",
            "127.0.0.1 www.guguyu.com",
            "127.0.0.1 www.moguyouxi.cn",
            "127.0.0.1 www.dalongyun.com",
            "127.0.0.1 c.play.cn",
            "127.0.0.1 www.gloud.cn",
            "127.0.0.1 www.haixingcloud.com",
            "127.0.0.1 www.wegame.com.cn",
            "127.0.0.1 www.cloudpc.cn",
            "127.0.0.1 www.anygame.info",
            "127.0.0.1 www.ldyunos.com",
            "127.0.0.1 cpc.icloud.cn",
            "127.0.0.1 cg.yidianwan.cn",
            "127.0.0.1 game.lingwoyun.cn",
            "127.0.0.1 www.dxywk.com",
            "127.0.0.1 cg.xoyo.com",
            "127.0.0.1 sr.mihoyo.com",
            "127.0.0.1 webstatic.mihoyo.com",
            "127.0.0.1 www.bhsr.com",
            "0.0.0.0 www.360.cn",
            "0.0.0.0 fun.360.cn",
            "0.0.0.0 browser.360.cn",
            "0.0.0.0 sd.360.cn",
            "0.0.0.0 www.2345.com",
            "0.0.0.0 2345browser.cn",
            "0.0.0.0 ie.2345.cc",
            "0.0.0.0 www.2345liulanqi.com",
            "0.0.0.0 www.ijinshan.com"]

PROCESS_BAN = [ "Genshin Impact Cloud Game.exe",
                "launcher.exe",
                "360se.exe",
                "360seupdate.exe",
                "360bdoctor.exe",
                "360secore.exe",
                "sesvr.exe",
                "sesvc.exe",
                "sesvcr.exe",
                "doctor_2345Exploer.exe"]


def write_host(host_value, host_path):
    host = open(host_path, 'a' , encoding='UTF-8')
    for thing in host_value:
        host.write(thing)
        host.write(" #ban\n")
    host.close()


def delete_host(host_path):
    host = open(host_path, 'r' , encoding='UTF-8')
    temp_list = []
    Pattern = re.compile(r'#ban')
    temp_list = [line for line in host.readlines() if not(Pattern.search(line))]
    '''#old
    for thing in host.readlines():
        if Pattern.search(thing):
            pass
        else:
            temp_list.append(thing)
    '''
    host.close()
    host = open(host_path, 'w' , encoding='UTF-8')
    for i in temp_list:
        host.write(i)
    host.close()


def check_host(host_value, host_path):
    quantity_now = 0
    quantity = len(host_value)
    Pattern = re.compile(r'#ban')
    host = open(host_path, 'r' , encoding='UTF-8')
    for line in host.readlines():
        if Pattern.search(line):
            quantity_now += 1
    if quantity_now != quantity:
        host.close()
        return True
    
    for url in host_value:
        host.seek(0)
        finding = False
        pattern_temp = re.compile(url + r" #ban")
        for line in host.readlines():
            if pattern_temp.search(line):
                finding = True
                break
        if not(finding):
            host.close()
            return True
    host.close()
    return False


        
def check_host_reban(host_value,host_path):
    host = open(host_path, 'r' , encoding='UTF-8')
    for url in host_value:
        host.seek(0)
        pattern = re.compile(r'#' + url)
        for line in host.readlines():
            if pattern.search(line):
                host.close()
                return True
    host.close()
    return False

    '''#old
    host = open(host_path, 'r' , encoding='UTF-8')
    for line in host.readlines():
        for url in host_value:
            Pattern = re.compile(r'#' + url)
            if Pattern.search(line):
                return True
    host.close()
    return False
    '''

#This is from...(I forget again)
def check_process_running(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False

def kill_process(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            proc.kill()

def open_web():
    webbrowser.open("https://www.bilibili.com/video/BV18X4y197tv")

def main_inside():
    if check_host(HOST_BAN, host_windows) or check_host_reban(HOST_BAN,host_windows):
        delete_host(host_windows)
        write_host(HOST_BAN, host_windows)
        os.system('ipconfig /flushdns')
    
    for name in PROCESS_BAN:
        if check_process_running(name):
            kill_process(name)
            open_web()

#old 
'''
time.sleep(100)
Pattern_switch = re.compile(r'switch01')
Pattern_process = re.compile(r'PB_from_option')
Pattern_ban1 = re.compile(r'127.0.0.1')
Pattern_ban2 = re.compile(r'0.0.0.0')
while True:
    try:
        option = open("option", 'r', encoding='UTF-8')
        HB_from_option = []
        PB_from_option = []
        switch01 = ""
        for thing in option.readlines():
            if Pattern_switch.search(thing) or Pattern_process.search(thing):
                exec(thing)
                # do not add print(switch01) here!!
                if switch01 == "off":
                    delete_host(host_windows)
                    os.system('ipconfig /flushdns')
                    sys.exit(0)
            if Pattern_ban1.search(thing) or Pattern_ban2.search(thing):
                temp_str = thing.replace("\n","")
                HB_from_option.append(temp_str)
        option.close()

        if check_host(HB_from_option, host_windows) or check_host_reban(HB_from_option,host_windows):
            delete_host(host_windows)
            write_host(HB_from_option, host_windows)
            os.system('ipconfig /flushdns')
        for name in PB_from_option:
            if check_process_running(name):
                kill_process(name)
                open_web()
    except OSError :
        main_inside()
    time.sleep(20)
'''


#the codes that are used to get admin power are from others
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    #time.sleep(100)
    #main start
    Pattern_switch = re.compile(r'switch01')
    Pattern_process = re.compile(r'PB_from_option')
    Pattern_ban1 = re.compile(r'127.0.0.1 ')
    Pattern_ban2 = re.compile(r'0.0.0.0 ')
    PB_from_option = []
    switch01 = ""
    while True:
        print("check")
        HB_from_option = []
        try:
            option = open("option", 'r', encoding='UTF-8')
            for th in option.readlines():
                if Pattern_switch.search(th) or Pattern_process.search(th):
                    exec(th)
                    # do not add print(switch01) here!! It will maybe cause a bug
                    if switch01 == "off":
                        delete_host(host_windows)
                        os.system('ipconfig /flushdns')
                        sys.exit(0)
                if Pattern_ban1.search(th) or Pattern_ban2.search(th):
                    temp_str = th.replace("\n","")
                    HB_from_option.append(temp_str)
            option.close()

            if check_host(HB_from_option, host_windows) or check_host_reban(HB_from_option,host_windows):
                delete_host(host_windows)
                write_host(HB_from_option, host_windows)
                os.system('ipconfig /flushdns')
            for name in PB_from_option:
                if check_process_running(name):
                    kill_process(name)
                    open_web()
        except OSError :
            main_inside()
        time.sleep(20)
        #main end
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)







