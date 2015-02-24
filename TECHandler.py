import win32gui
import win32ui
import time

import win32con
def f_click(pycwnd):
    x = 167
    y = 844


def get_whndl(window_name):
    whndl = win32gui.FindWindowEx(0, 0, None, window_name)
    return whndl


def make_pycwnd(hwnd):
    PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
    return PyCWnd


def send_input(pycwnd, msg):
    # f_click(pycwnd)
    for c in msg:
        if c == "\n":
            pycwnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            pycwnd.SendMessage(win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            pycwnd.SendMessage(win32con.WM_CHAR, ord(c), 0)
    pycwnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    pycwnd.SendMessage(win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    pycwnd.UpdateWindow()


def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        hwnds[win32gui.GetClassName(hwnd)] = hwnd
    return True


def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
