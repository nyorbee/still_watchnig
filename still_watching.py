import psutil
import time
import ctypes
import pyautogui
import pystray
import PIL.Image
import os
import threading

script_dir = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(script_dir, 'eye.png')
image = PIL.Image.open(image_path)

is_checking = False
check_time = 1800

def on_clicked(icon, item):
    global is_checking, check_time
    if str(item) == 'Zacznij sprawdzać czy nie śpisz':
        is_checking = True
        t = threading.Thread(target=check_for_potplayer)
        t.daemon = True
        t.start()
    elif str(item) == 'Zakończ':
        is_checking = False
        os._exit(0)
    elif str(item) == 'Jak często sprawdzać?':
        pass
    elif str(item) == 'Co 5 minut':
        check_time = 300
    elif str(item) == 'Co 15 minut':
        check_time = 900
    elif str(item) == 'Co pół godziny':
        check_time = 1800
    elif str(item) == 'Co godzinę':
        check_time = 3600


def check_if_process_running(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name in proc.name():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def check_for_potplayer():
    global is_checking, check_time
    while is_checking:
        if check_if_process_running('PotPlayerMini64.exe') or check_if_process_running('zuikaku.exe') \
                or check_if_process_running("vlc.exe") \
                or check_if_process_running("wmplayer.exe") or check_if_process_running("mpc-hc.exe") \
                or check_if_process_running("GOM.exe") or check_if_process_running("KMPlayer.exe") \
                or check_if_process_running("5kplayer.exe") or check_if_process_running("smplayer.exe")\
                or check_if_process_running("DivX Player.exe") or check_if_process_running("PowerDVD.exe"):
            time.sleep(check_time)
            if check_if_process_running('PotPlayerMini64.exe') or check_if_process_running('zuikaku.exe')\
                    or check_if_process_running("vlc.exe") or check_if_process_running("wmplayer.exe") \
                    or check_if_process_running("mpc-hc.exe") or check_if_process_running("GOM.exe")\
                    or check_if_process_running("KMPlayer.exe") or check_if_process_running("5kplayer.exe")\
                    or check_if_process_running("smplayer.exe") or check_if_process_running("DivX Player.exe")\
                    or check_if_process_running("PowerDVD.exe"):
                pyautogui.press('space')
                ctypes.windll.user32.MessageBoxW(0, 'Oglądasz jeszcze?', 'Halo?', 0x00001000)
                pyautogui.press('space')
            time.sleep(10)

def tray_icon():
    menu_items = [
        pystray.MenuItem('Zacznij sprawdzać czy nie śpisz', on_clicked),
        pystray.MenuItem('Jak często sprawdzać?',
            pystray.Menu(pystray.MenuItem('Co 5 minut', on_clicked),
                          pystray.MenuItem('Co 15 minut', on_clicked),
                          pystray.MenuItem('Co pół godziny', on_clicked),
                          pystray.MenuItem('Co godzinę', on_clicked))),
        pystray.MenuItem('Zakończ', on_clicked)
    ]
    icon = pystray.Icon('eye', image, menu=pystray.Menu(*menu_items))

    icon.run()

threading.Thread(target=tray_icon).start()
