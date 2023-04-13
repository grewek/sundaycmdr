#!/usr/bin/env python3
import os

import curses
from curses import wrapper

class View:
    
    def __init__(self, fileList, win, height):
        self.height = height
        self.selectionIndex = 0
        self.fileList = fileList 
        self.window = win

    def handle_command(self, pressed_key):
        if pressed_key == 'j':
            if self.selectionIndex + 1 >= self.height:
                self.selctionIndex = self.height
            else:
                self.selectionIndex += 1
        elif pressed_key == 'k':
            if self.selectionIndex - 1 < 0:
                self.selctionIndex = 0
            else:
                self.selectionIndex -= 1  

    def update(self):
        for i, file in enumerate(self.fileList[0:self.height]):
            if i == self.selectionIndex:
                curses.start_color()
                self.window.addstr(i, 0, file, curses.color_pair(curses.COLOR_RED))
            else:
                self.window.addstr(i, 0, file)       

        return True

    def draw(self, stdscr):
        stdscr.refresh()
        self.window.refresh()
    
def ReadAllFilesInHomeDirectory():
    #TODO: Add argument for different folders
    #TODO: We need this to work with every folder passed not just the homefolder..
    examplePath = os.path.expanduser('~')
    return os.listdir(examplePath)

    
def main(stdscr):
    stdscr.clear()

    winWidth = curses.COLS
    winHeight = curses.LINES

    splitRatio = .5
    viewWidth = int(winWidth * splitRatio)

    leftView = View(ReadAllFilesInHomeDirectory(), curses.newwin(winHeight, viewWidth, 0, 0), winHeight)
    rightView = View(ReadAllFilesInHomeDirectory(), curses.newwin(winHeight, viewWidth, 0, viewWidth), winHeight)

    views = [View(ReadAllFilesInHomeDirectory(), curses.newwin(winHeight, viewWidth, 0, 0), winHeight),
             View(ReadAllFilesInHomeDirectory(), curses.newwin(winHeight, viewWidth, 0, viewWidth), winHeight)]
    selectedView = 0
    
    #curses, incantations, song and dance...for colors
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    
    while(True):
        views[0].update()
        views[1].update()

        views[0].draw(stdscr)
        views[1].draw(stdscr)
        
        pressed_key = stdscr.getkey()
        views[selectedView].handle_command(pressed_key)

        if pressed_key == 'q':
            return
        elif pressed_key == 'h':
            selectedView = 0
        elif pressed_key == 'l':
            selectedView = 1
    return

wrapper(main)
