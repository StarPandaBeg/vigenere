import curses
import string
import time
import re
from itertools import cycle, product

alp = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

TEXT = open("input.txt", encoding="utf-8").read()
KEY_LEN = 2
VARIANTS_IN_FILE = 1000000

ALL_VARIANTS = len(alp)**KEY_LEN
file_name = "text"
file_index = 0
directory = "out/"
words = []
l = 0

def putheader(stdscr):
    HEADING = "Взлом шифра Виженера"
    header = "="*((curses.COLS-1)-len(HEADING)-2)
    l = len(header) + 1
    header = header[0:l//2] + " " + HEADING + " " + header[l//2:]
    stdscr.addstr(0, 0, header)

    stdscr.addstr(2, 0, "Текущие настройки:")
    stdscr.addstr(4, 1, "* Длина исходного текста: "+str(len(TEXT)))
    stdscr.addstr(5, 1, "* Длина предпопогаемого ключа: "+str(KEY_LEN))
    stdscr.addstr(7, 1, "* Количество варинтов в одном файле: "+str(VARIANTS_IN_FILE))
    stdscr.addstr(8, 1, "* Всего варинтов: "+str(ALL_VARIANTS))
    stdscr.addstr(10, 0, "-----")

def waitforkey(stdscr):
    while True:
        c = stdscr.getch()
        if c == ord('s'):
            break
        elif c == ord('q'):
            exit(0)

def decode_vijn(text, key):
    global alp
    result = []
    space = 0
    for index, ch in enumerate(text):
        if ch != ' ':
            cj = alp.index(ch)
            kj = alp.index(key[(index - space) % len(key)])
            mj = (cj - kj) % len(alp)
            result.append(alp[mj])
        else:
            space += 1
            result.append(' ')
    return ''.join(result)

def save_table(table):
  global file_index
  with open(directory+file_name+str(file_index)+".txt", 'w', encoding="utf-8") as f:
    for i in table:
      f.write(i+"\n")
    file_index+=1

def run(stdscr):
    global alp, words, l

    TIME_REFRESH = 5000
    current_speed = 0
    current_time_pass = 0
    est_time = 0

    time_start = time.time()-1
    time_start_fixed = time_start

    win = curses.newwin(8, (curses.COLS-1), (curses.LINES-1)-7, 0)

    def refreshUI(key, i):
        win.clear()
        percent = round(i/ALL_VARIANTS*100)
        s = "#"*percent + "-"*(100-percent) + f" {percent}%"
        win.addstr(1, 0, f"Текущий код: {i} / {ALL_VARIANTS}")
        win.addstr(3, 0, f"Прошло времени: {current_time_pass} сек.")
        win.addstr(4, 0, f"Скорость: {current_speed} вар/сек.")
        win.addstr(5, 0, f"Оставшееся время: {est_time} сек.")
        win.addstr(7, 0, s)
        win.refresh()
    
    for i, key in enumerate(product(alp, repeat=KEY_LEN)):
        key = ''.join(key)
        word = decode_vijn(TEXT, key)
        words.append(key+ " ; " + word)
        l += 1

        # if (l >= VARIANTS_IN_FILE):
        #     save_table(words)
        #     words = []
        #     l = 0

        if (i % TIME_REFRESH == 0):
            time_end = time.time()
            current_speed = round(TIME_REFRESH / (time_end - time_start))
            est_time = round((ALL_VARIANTS - i)/current_speed)
            current_time_pass = round(time_end - time_start_fixed)
            time_start = time_end
            refreshUI(key, i)

    save_table(words)
        
def main(stdscr):
    stdscr.clear()
    curses.curs_set(False)

    putheader(stdscr)
    stdscr.addstr(12, 0, "Нажмите S чтобы начать, Q для выхода.")
    stdscr.refresh()
    waitforkey(stdscr)

    stdscr.move(12, 0)
    stdscr.clrtoeol() 
    stdscr.refresh()

    run(stdscr)

curses.wrapper(main)