# Convergence Jukebox is Python based codes that emulates a Jukebox and plays mp3 media.
# Copyright (C) 2012 by Brad Fortner
# This program is free software you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation;
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see http://www.gnu.org/licenses.
# The authour, information on, executable downloads and source code can be obtained via www.convergencejukebox.com

# Convergence Jukebox employs the hsaudiotag Python library which is released under an OSI BSD licence.
# hsaudiotag see: https://pypi.python.org/pypi/hsaudiotag
# Convergence Jukebox employs the playmp3.py Python library for windows Copyright (c) 2011 by James K. Lawless
# playmp3.py has been released under an MIT / X11 licence. See: http://www.mailsend-online.com/license.php.
# Convergence Jukebox employs the PyRSS2Gen Python Library.
# PyRSS2Gen is copyright (c) by Andrew Dalke Scientific, AB (previously
# Dalke Scientific Software, LLC) and is released under the BSD license.
# Info on PyRSS2Gen at http://www.dalkescientific.com/Python/PyRSS2Gen.html

# This Python script has been tested and compiles into a windows.exe using Pyinstaller.
# https://mborgerson.com/creating-an-executable-from-a-python-script

import kivy
kivy.require("1.9.1")  # used to alert user if this code is run on an earlier version of Kivy.
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
import sys  # Used for testing new code. Required to add sys.exit().
import re  # Used in searching Genre substrings. Specifically word-boundaries of regular expressions.
import subprocess
from subprocess import call
from subprocess import Popen, PIPE #  requred for mpg321 mp3 player for Rasberry Pi version
from Tkinter import *  # Used as message to alert users to place MP3's in music folder
import tkMessageBox
import Tkinter
import Tkinter as tk
from operator import itemgetter
import os
import datetime  # Used in RSS generation.
import PyRSS2Gen  # Used n RSS generation.
import getpass  # Gets user name http://stackoverflow.com/questions/4325416/how-do-i-get-the-username-in-python.
import keyboard # Used to simulated keyboard events to call screen update functions http://bit.ly/2qwRrTh
import glob
import datetime  # Used to convert song duration in seconds to minutes/seconds.
import random
import time  # Used in time_date_stamp. http://bit.ly/1MKPl5x and http://bit.ly/1HRKTMJ
import pickle  # Used to save and reload python lists
from hsaudiotag import auto  # Used to work with MP3 ID3 data https://pypi.python.org/pypi/hsaudiotag
from ctypes import *  # Used by playmp3.py windows based mp3 player http://bit.ly/1MgaGCh
import getpass  # Used to get user name http://stackoverflow.com/questions/4325416/how-do-i-get-the-username-in-python
# import os.path, time

print "Welcome To Convergence Jukebox 2"
print "Your Jukebox Is Being Configured"
print "This Could Take A Few Minutes"
# Variables
computer_account_user_name = getpass.getuser()
genre_file_changed = ""
random_change_list = ""
selectedArtists = []  # Used to select multiple artists in random play routine
artistSelectRoutine = 0  # Used to break Artist
artistSortRequired = "No"
genreYearSort = "No"
artistSortRequiredByYear = "No"
counter = 0
play_list = []  # Holds song numbers for paid selections.
build_list = []  # List temporarily holds ID3 data during song processing. Data later written to song_list then cleared.
remove_list = []  # Python List used to remove songs from random_list
random_list = []
flag_fourteen = ""
flag_fourteen_change = ""
output_list = []  # List is used to output information related to Jukebox functions. Contains information on songs
song_list = []  # List is used to build final list of all songs including ID3 information and file location.
file_time_old = "Wed Dec 30 22:56:15 2015"
file_time_check = ""

# song_list info locations: songTitle = song_list[x][0], songArtist = song_list[x][1], songAlbum = song_list[x][2]
# song_year = song_list[x][3], songDurationSeconds = song_list[x][4], songGenre = song_list[x][5],
# songDurationTime = song_list[x][6], songComment = song_list[x][7]

# settings

if sys.platform == 'win32':
    winmm = windll.winmm  # required by playMP3

current_directory = os.getcwd() # Gets current directory.

if current_directory == "/home/pi": # Changes home directory on Raspberry Pi
    os.chdir("/home/pi/python/jukebox")
    current_directory = os.getcwd()
