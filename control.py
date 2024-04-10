
import winshell, os, re, shutil, psutil, sys, getpass
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox, QFileDialog


host_windows = r"C:\Windows\System32\drivers\etc\hosts"

username = getpass.getuser()# 获取用户名
syspath = os.getenv("SystemDrive")# 系统盘符名称
startupPath = os.path.join(os.getenv("SystemDrive"),r"\users",getpass.getuser(),r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")# 自启动目录

install_path = "E:/"
install_folder = "NET_Framework_4.14"
dir_path = install_path + install_folder

program_name = "NET_Framework_4.14.exe"
option_name = "option"

#get path of things
program_path = dir_path + "/" + program_name
option_path = dir_path + "/" + option_name

#As spare
def delete_host(host_path):
    target = open(host_path, 'r' , encoding='UTF-8')
    temp_list = []
    Pattern = re.compile(r'#ban')
    for thing in target.readlines():
        if Pattern.search(thing):
            pass
        else:
            temp_list.append(thing)
    target.close()
    target = open(host_path, 'w' , encoding='UTF-8')
    for i in temp_list:
        target.write(i)
    target.close()


def kill_process(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            proc.kill()
        else:
            return False

#this is from ...(I forget it T.T)
def create_shortcut(bin_path: str, name: str, desc: str):
    shortcut =  name + ".lnk"
    winshell.CreateShortcut(
        Path=shortcut,
        Target=bin_path,
        Icon=(bin_path, 0),
        Description=desc
    )
'''
:param bin_path: exe路径
:param name: 需要创建快捷方式的路径
:param desc: 描述，鼠标放在图标上面会有提示
'''


def install():
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        shutil.copy2(option_name, dir_path)
        shutil.copy2(program_name, dir_path)
    except:
        msg_box = QMessageBox(QMessageBox.Critical, '错误Error', 'error')
        msg_box.exec_()

def uninstall():
    try:
        os.remove(option_path)
        os.remove(program_path)
    except:
        msg_box = QMessageBox(QMessageBox.Critical, '错误Error', 'error')
        msg_box.exec_()

def run():
    try:
        Pattern_switch = re.compile(r"switch01")
        option = open(option_path, 'r' , encoding="UTF-8")
        temp_list = []
        for thing in option.readlines():
            if Pattern_switch.search(thing) or thing == "\n":
                pass
            else:
                temp_list.append(thing)
        option.close()
        option = open(option_path, 'w' , encoding="UTF-8")
        option.write('switch01 = "on"')
        option.write("\n")
        for i in temp_list:
            option.write(i)
        option.close()
        os.startfile(program_path)
    except:
        os.startfile(program_path)


def stop():
    try:
        Pattern_switch = re.compile(r"switch01")
        option = open(option_path, 'r' , encoding="UTF-8")
        temp_list = []
        for thing in option.readlines():
            if Pattern_switch.search(thing) or thing == "\n":
                pass
            else:
                temp_list.append(thing)
        option.close()
        option = open(option_path, 'w' , encoding="UTF-8")
        option.write('switch01 = "off"')
        option.write("\n")
        for i in temp_list:
            option.write(i)
        option.close()
    except OSError:
        kill_process(program_name)
        delete_host(host_windows)
    except:
        msg_box = QMessageBox(QMessageBox.Critical, '错误Error', 'error')
        msg_box.exec_()

#This is from...(I forget it again)
# 将快捷方式添加到自启动目录
def asup():
    try:
        bin_path = program_path #此处未转换为原始不转义字符串，凑合用
        link_path = startupPath + "\\NET_Framework"
        desc = "NET_Framework"
        create_shortcut(bin_path, link_path, desc)
    except:
        msg_box = QMessageBox(QMessageBox.Critical, '错误Error', '权限不足或快捷方式已存在')
        msg_box.exec_()

def rm_asup():
    try:
        link_path = startupPath + "\\NET_Framework.lnk"
        os.remove(link_path)
    except:
        msg_box = QMessageBox(QMessageBox.Critical, '错误Error', '权限不足或快捷方式不存在')
        msg_box.exec_()

#Work in program
#change install_path
'''
def install_path():
    dir_path=QFileDialog.getExistingDirectory(self,"choose directory",None) 
    msg_box = QMessageBox(QMessageBox.information, 'msg', dir_path)
    msg_box.exec_()
'''

app = QApplication(sys.argv)
win = QMainWindow()
win.setGeometry(200, 200, 550, 400)
win.setWindowTitle("town_ban 镇禁")


label = QLabel(win)
label.resize(200, 20)
label.setText("version: 4.114.514")
label.move(20, 10)

label_2 = QLabel(win)
label_2.resize(200, 20)
label_2.setText("town_ban")
label_2.move(20, 30)


button_install = QPushButton(win)
button_install.resize(150, 50)
button_install.setText("install")
button_install.move(100, 100)
button_install.clicked.connect(install)

button_uninstall = QPushButton(win)
button_uninstall.resize(150, 50)
button_uninstall.setText("uninstall")
button_uninstall.move(300, 100)
button_uninstall.clicked.connect(uninstall)
'''
bt_install_path = QPushButton(win)
bt_install_path.resize(150, 50)
bt_install_path.setText("install path")
bt_install_path.move(500, 100)
bt_install_path.clicked.connect(install_path)
'''
button_add_stp = QPushButton(win)
button_add_stp.resize(200, 50)
button_add_stp.setText("add to startup")
button_add_stp.move(50, 200)
button_add_stp.clicked.connect(asup)

button_add_stp = QPushButton(win)
button_add_stp.resize(200, 50)
button_add_stp.setText("remove startup")
button_add_stp.move(300, 200)
button_add_stp.clicked.connect(rm_asup)

button_run = QPushButton(win)
button_run.resize(100, 50)
button_run.setText("run !")
button_run.move(100, 300)
button_run.clicked.connect(run)

button_stop = QPushButton(win)
button_stop.resize(100, 50)
button_stop.setText("stop !")
button_stop.move(350, 300)
button_stop.clicked.connect(stop)

win.show()
sys.exit(app.exec_())


