#!/usr/bin/env python3
import os
from enum import Enum,IntEnum
from operator import itemgetter, attrgetter

import curses
from curses import wrapper

class PathType(Enum):
    Relative=0,
    Absolute=1,

class Direction(IntEnum):
    Inside=0,
    Outside=1,

class FileType(IntEnum):
    Directory=0,
    File=1,
    Link=2, #TODO: This is for much later

class Directory:
    def __init__(self, path, prev=None):
        self.prev = prev
        self.path = path
        self.longestFilename = 0
        
        self.content = []
        
        expanded = os.path.expanduser(path)
        fileListing = os.listdir(expanded)
        
        for i, filename in enumerate(fileListing):
            targetPath = expanded + "/" + filename
            filetype = FileType.Directory
            if not os.path.isdir(targetPath):
                filetype = FileType.File
            filenameLength = len(filename)
            if filenameLength > self.longestFilename:
                self.longestFilename = filenameLength
            self.content.append((filename, filetype, os.stat(targetPath).st_size))
        
        list.sort(self.content, key=itemgetter(0))
        list.sort(self.content, key=itemgetter(1))

    def FolderFromSelectionIndex(self, selectionIndex):
        if self.content[selectionIndex][1] == FileType.Directory:
            return self.path + "/" + self.content[selectionIndex][0]

        return None
    def DirectoryLength(self):
        return len(self.content) 

    def GenerateListing(self):
        return self.content
     
class View:
    def __init__(self, directory, width, height, startY=0, startX=0):
        self.height = height
        self.maxItems = self.height
        self.width = width
        self.selectionIndex = 0
        self.cwd = directory 
        #TODO: Test the Pad Window type from the curses lib, it seems to be a scrolling content window as well
        #      but with a very clunky API...
        self.window = curses.newwin(height, width, startY, startX) 
        self.minIndex = 0
        self.maxIndex = self.height
        
        self.startY = startY
        self.startX = startX

    def ValidateSelectionIndex(self):
        if self.selectionIndex < 0:
            self.selectionIndex = 0

        distanceToEnd = self.cwd.DirectoryLength() - self.selectionIndex
        if distanceToEnd <= 0:
            self.selectionIndex = self.cwd.DirectoryLength() - 1

    def HandleChangeDirectory(self, mode, direction):
        if mode == PathType.Relative:
            if direction == Direction.Inside:
                nextDirectory = self.cwd.FolderFromSelectionIndex(self.selectionIndex)
                prevPath = self.cwd
                if nextDirectory is None:
                    return

                self.cwd = Directory(nextDirectory, prevPath)
                self.selectionIndex = 0
            elif direction == Direction.Outside:
                if self.cwd.prev is None:
                    return
                
                self.cwd = self.cwd.prev
                self.selectionIndex = 0
        elif mode == PathType.Absolute:
            pass
        else:
            pass #TODO: Read the docs about the enum type

    def HandleKeyEvents(self, pressed_key):
        if pressed_key == 'j':
            self.selectionIndex += 1
        elif pressed_key == 'k':
            self.selectionIndex -= 1
        elif pressed_key == 'i':
            self.HandleChangeDirectory(PathType.Relative, Direction.Inside) #Change the current directory of this view into the selected folder.
        elif pressed_key == 'o':
            self.HandleChangeDirectory(PathType.Relative, Direction.Outside) #Change cwd to the previous directory in the filetree.

    def CalculateFileSliceRange(self):
        #NOTE: Change the divisior in the minIndex to get a different turnaround point
        self.minIndex = max(0, self.selectionIndex - int(self.height/2)) 
        self.maxIndex = self.minIndex + self.height
    
    #TODO: This should be really part of the Directory Class
    def FormatFileType(self, record):
        (fname, ftype, fsize) = record
        distance = abs(len(fname) - self.cwd.longestFilename)
        
        if ftype == FileType.Directory:
            return "<{}>{}{}".format(fname, " " * distance, fsize)
        return "{}{}{}".format(fname, " " * (distance + 2), fsize)
        
    def Update(self):
        self.window.clear()
        self.ValidateSelectionIndex()
        self.CalculateFileSliceRange()

        for i, record in enumerate(self.cwd.GenerateListing()[self.minIndex:self.maxIndex]):
            if i + self.minIndex == self.selectionIndex:
                curses.start_color()
                #TODO: Overflowing the width of the window seems to be a issue for curses so we need to find a way
                #      to not make it crash !
                self.window.addstr(i, 0, "{}".format(self.FormatFileType(record)), curses.color_pair(curses.COLOR_RED))
            else:
                self.window.addstr(i, 0, "{}".format(self.FormatFileType(record)))

    def Draw(self):
        self.window.refresh()
    
    
def main(stdscr):
    stdscr.clear()

    winWidth = curses.COLS
    winHeight = curses.LINES

    splitRatio = .5
    viewWidth = int(winWidth * splitRatio)

    testDirectory = Directory('~')
    
    views = [View(testDirectory, viewWidth, winHeight),
             View(testDirectory, viewWidth, winHeight, 0, viewWidth)]
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
            selectedView = 0 #Change the cursor to the left view pane
        elif pressed_key == 'l':
            selectedView = 1 #Change the cursor to the right view pane
    return


wrapper(main)
