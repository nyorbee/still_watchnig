import psutil
import time
import ctypes
import pyautogui
import pystray
import PIL.Image
import os
import threading
import webbrowser
from PIL import ImageGrab, ImageChops
import pywinauto


versionNumber = "v.0.8-beta"

script_dir = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(script_dir, 'eye.png')
image = PIL.Image.open(image_path)

is_checking = False
check_time = 10

def on_clicked(icon, item):
    global is_checking, check_time
    if str(item) == "Start checking if you're not asleep.":
        is_checking = True
        t = threading.Thread(target=check_for_potplayer)
        t.daemon = True
        t.start()
    elif str(item) == 'Quit':
        is_checking = False
        os._exit(0)
    elif str(item) == 'How often should I check?':
        pass
    elif str(item) == 'Every 5 minutes':
        check_time = 300
    elif str(item) == 'Every 15 minutes':
        check_time = 900
    elif str(item) == 'Every half an hour':
        check_time = 1800
    elif str(item) == 'Every hour':
        check_time = 3600


def check_if_process_running(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name in proc.name():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def check_for_potplayer():
    playersApps = ['PotPlayerMini64.exe', 'zuikaku.exe', "vlc.exe", "wmplayer.exe", "mpc-hc.exe",\
                   "GOM.exe", "KMPlayer.exe", "5kplayer.exe", "smplayer.exe", "DivX Player.exe", "PowerDVD.exe"]
    global is_checking, check_time, playing
    while is_checking:
        for app in playersApps:
            if check_if_process_running(app):
                time.sleep(check_time)
                if check_if_process_running(app):
                    playing = False
                for i in range(2):
                    im1 = ImageGrab.grab()
                    time.sleep(30)
                    im2 = ImageGrab.grab()
                    diff = ImageChops.difference(im1, im2)
                    if diff.getbbox() is not None:
                        playing = True

                        break
                app_window = pywinauto.Application(backend='uia').connect(path=app).top_window()

                if playing and check_if_process_running(app) and app_window.is_active():
                    pyautogui.press('space')
                    ctypes.windll.user32.MessageBoxW(0, 'Are you still watching?', 'Hello?', 0x00001000)
                    pyautogui.press('space')
            else:
                time.sleep(10)

def open_github():
    webbrowser.open_new_tab('https://github.com/nyorbee')
def open_itguy():
    webbrowser.open_new_tab('https://www.facebook.com/ajtiguy')
created_path = os.path.join(script_dir, 'created.png')

def tray_icon():


    menu_items = [
        pystray.MenuItem('About',
                         pystray.Menu(
                         pystray.MenuItem(versionNumber, None),
                         pystray.MenuItem('GitHub', lambda: open_github()),
                         pystray.MenuItem('IT Guy Facebook Page', lambda : open_itguy())


                         )),


        pystray.MenuItem("Start checking if you're not asleep.", on_clicked),
        pystray.MenuItem('How often should I check?',
            pystray.Menu(pystray.MenuItem('Every 5 minutes', on_clicked),
                          pystray.MenuItem('Every 15 minutes', on_clicked),
                          pystray.MenuItem('Every half an hour', on_clicked),
                          pystray.MenuItem('Every hour', on_clicked))),

        pystray.MenuItem('Quit', on_clicked)
    ]



    icon = pystray.Icon('eye', image, menu=pystray.Menu(*menu_items))


    icon.run()




threading.Thread(target=tray_icon).start()


