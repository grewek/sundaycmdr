#!/usr/bin/env python3
import os

import curses
from curses import wrapper

class View:
    def __init__(self, fileList, width, height, startY=0, startX=0):
        self.height = height
        self.width = width
        self.selectionIndex = 0
        self.fileList = fileList 
        #TODO: Test the Pad Window type from the curses lib, it seems to be a scrolling content window as well
        #      but with a very clunky API...
        self.window = curses.newwin(height, width, startY, startX) 
        
        self.minIndex = 0
        self.maxIndex = self.height
        
        self.startY = startY
        self.startX = startX

    def ValidateSelectionIndex(self):
        if self.selectionIndex - 1 < 0:
            self.selectionIndex = 0

        distanceToEnd = len(self.fileList) - self.selectionIndex
        if self.selectionIndex > self.height and distanceToEnd <= 0:
            self.selectionIndex = len(self.fileList) - 1

            
    def HandleKeyEvents(self, pressed_key):
        if pressed_key == 'j':
            self.selectionIndex += 1
        elif pressed_key == 'k':
            self.selectionIndex -= 1  

    def CalculateFileSliceRange(self):
        #NOTE: Change the divisior in the minIndex to get a different turnaround point
        self.minIndex = max(0, self.selectionIndex - int(self.height/2)) 
        self.maxIndex = self.minIndex + self.height
        
    def Update(self):
        self.window.clear()
        self.ValidateSelectionIndex()
        self.CalculateFileSliceRange()

        for i, file in enumerate(self.fileList[self.minIndex:self.maxIndex]):
            if i + self.minIndex == self.selectionIndex:
                curses.start_color()
                self.window.addstr(i, 0, "{} {}".format(i + self.minIndex, file), curses.color_pair(curses.COLOR_RED))
            else:
                self.window.addstr(i, 0, "{} {}".format(i + self.minIndex, file))       

        return True

    def Draw(self):
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

    views = [View(ReadAllFilesInHomeDirectory(), viewWidth, winHeight),
             View(ReadAllFilesInHomeDirectory(), viewWidth, winHeight, 0, viewWidth)]
    selectedView = 0
    
    #curses, incantations, song and dance...for colors
    #jokes aside this tells curses it should use the terminal background color and a red foreground color
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    
    while(True):
        views[0].Update()
        views[1].Update()

        stdscr.refresh()
        views[0].Draw()
        views[1].Draw()
        
        pressed_key = stdscr.getkey()
        views[selectedView].HandleKeyEvents(pressed_key)

        if pressed_key == 'q':
            return
        elif pressed_key == 'h':
            selectedView = 0
        elif pressed_key == 'l':
            selectedView = 1
    return

wrapper(main)
