#from ctypes import *  # Used by playmp3.py windows based mp3 player.
# http://www.mailsend-online.com/blog/play-mp3-files-with-python-on-windows.html
from ctypes import *  # Used by playmp3.py windows based mp3 player http://bit.ly/1MgaGCh
import datetime  # Used in RSS generation and to convert song duration in seconds to minutes/seconds.
import getpass  # Gets user name http://stackoverflow.com/questions/4325416/how-do-i-get-the-username-in-python.
import glob
from hsaudiotag import auto  # Used to work with MP3 ID3 data https://pypi.python.org/pypi/hsaudiotag
import keyboard  # Used to simulated keyboard events to call screen update functions http://bit.ly/2qwRrTh
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.clock import Clock
Clock.max_iteration = 20
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.core.window import Window
from operator import itemgetter
import os
import os.path, time
import pickle
import PyRSS2Gen  # Used n RSS generation.
import random
import re  # Used in searching Genre substrings. Specifically word-boundaries of regular expressions.
import subprocess
from subprocess import call
from subprocess import Popen, PIPE #  requred for mpg321 mp3 player for Rasberry Pi version
import sys  # Used to check and switch resolutions for convergence jukebox.
import time, threading
kivy.require("1.9.1")  # used to alert user if this code is run on an earlier version of Kivy.


###### Variables #####
global title
global artist
global album
global year
global ptime
global randomplay
artist_list = []
artistSelectRoutine = 0  # Used to break Artist
artistSortRequired = "No"
artistSortRequiredByYear = "No"
adder = 0
build_list = []  # List temporarily holds ID3 data during song processing. Data later written to song_list then cleared.
computer_account_user_name = getpass.getuser()  # Used to write various log and RSS files to local directories.
counter = 0
credit_amount = 0
current_directory = os.getcwd() # Gets current directory.
current_file_count = 0
cursor_position = 0
delete_indicator = ""
database_indicator = ""
delete_indicator = ""
file_name_with_error = ""
file_time_check = ""
file_time_old = "Wed Dec 30 22:56:15 2015"
flag_fourteen = ""
flag_fourteen_change = ""
genre_file_changed = ""
genreYearSort = "No"
last_pressed = ""
output_list = []  # List is used to output information related to Jukebox functions. Contains information on songs
play_list = []  # Holds song numbers for paid selections.
random_list = []
random_change_list = ""
remove_list = []  # Python List used to remove songs from random_list
screen_number = 0
selectedArtists = []  # Used to select multiple artists in random play routine
song_list = []  # List is used to build final list of all songs including ID3 information and file location.
song_selection_number = ""
song_status = "none"
start_up = 0
x = 0

# song_list info locations: songTitle = song_list[x][0], songArtist = song_list[x][1], songAlbum = song_list[x][2]
# song_year = song_list[x][3], songDurationSeconds = song_list[x][4], songGenre = song_list[x][5],
# songDurationTime = song_list[x][6], songComment = song_list[x][7]

#####Program Initialization#####

if sys.platform == 'win32':
    winmm = windll.winmm  # Variable used in playmp3.py.

if current_directory == "/home/pi": # Changes home directory on Raspberry Pi
    os.chdir("/home/pi/python/jukebox")
    current_directory = os.getcwd()

full_path = os.path.realpath('__file__')  # http://bit.ly/1RQBZYF
print current_directory
print full_path

try:
    song_list_recover = open('song_list.pkl', 'rb')
    song_list = pickle.load(song_list_recover)
    song_list_recover.close()
    del song_list_recover
except IOError:
    print song_list
    for i in range(0, 16):  # Adds blank songs to end of sont_list
        song_list.append([u'zzzzz', u'zzzzz', u' ', u' ', u' ', u' ', u' ', u' ', 'zzzzz - zzzzz.mp3', u' '])
    print song_list
    song_list_save = open('song_list.pkl', 'wb')  # song_list saved as binary pickle file
    pickle.dump(song_list, song_list_save)
    song_list_save.close()
    file_count_update = open("file_count.txt", "w+")  # Writes new filecount to filecount.txt.
    file_count_update.write("-1")
    file_count_update.close()
    keyboard.press_and_release('o')

try:
    song_list_recover = open('song_list.pkl', 'rb')
    song_list = pickle.load(song_list_recover)
    song_list_recover.close()
    del song_list_recover
except EOFError:
    print song_list
    for i in range(0, 16):  # Adds blank songs to end of sont_list
        song_list.append([u'zzzzz', u'zzzzz', u' ', u' ', u' ', u' ', u' ', u' ', 'zzzzz - zzzzz.mp3', u' '])
    print song_list
    song_list_save = open('song_list.pkl', 'wb')  # song_list saved as binary pickle file
    pickle.dump(song_list, song_list_save)
    song_list_save.close()
    file_count_update = open("file_count.txt", "w+")  # Writes new filecount to filecount.txt.
    file_count_update.write("-1")
    file_count_update.close()
    keyboard.press_and_release('o')

song_list.sort(key=itemgetter(1), reverse=False)
display_info_recover = open("output_list.txt", 'r+')
output_list_read = display_info_recover.read()
display_info_recover.close()
display_info = output_list_read.split(",")

the_bands_file_open = open("the_bands.txt", 'r+')
to_be_split = the_bands_file_open.read()
the_bands_file_open.close()
the_bands_list = to_be_split.split(",")
the_bands_list_lower_case = []
for s in the_bands_list:
    the_bands_list_lower_case.append(s.lower())

licence = "Convergence Jukebox is Python\n" + \
          "based code that emulates a\n" + \
          "Jukebox and plays mp3 media.\n" + " \n" + \
          "Copyright (C) 2012-2017\n" + \
          "by Brad Fortner.\n" + \
          " \n" + "This program is free software you can\n" + \
          "redistribute it and\or modify it\n" + \
          "under the terms of the GNU General\n" + \
          "Public License as published by the\n" + \
          "Free Software Foundation; either\n" + \
          "version 3 of the License, or (at your\n" + \
          "option) any later version.\n" + " \n" + \
          "This program is distributed in the\n" + \
          "hope that it will be useful, but\n" + \
          "WITHOUT ANY WARRANTY; without\n" + \
          "even the implied warranty of\n" + \
          "MERCHANTABILITY or FITNESS FOR\n" + \
          "A PARTICULAR PURPOSE. Details:\n" + \
          "see the GNU General Public License.\n" + " \n" + \
          "Info: www.convergencejukebox.com"
upcoming_list_recover = open('upcoming_list.pkl', 'rb')
upcoming_list = pickle.load(upcoming_list_recover)
upcoming_list_recover.close()
selections_available = len(song_list)
del upcoming_list_recover

Window.fullscreen = True  # does not force full screen
Window.size = (1280, 720)  # sets 720p

Builder.load_string('''
<Label>:
    color: 0,.7,0,1 # Sets text colour to green.
    font_size: 18
    valign: 'middle'
    halign: 'left'
    text_size: self.size
<Button>:
    font_size: 16
    color: 1,1,1,1 # Sets text colour to white.
    bold: True
    background_normal: "" # Button background defalts to grey. This sets the background to plain.
    background_color: (0.0, 0.0, 0.0, 0.0)# Sets the buttons colour to black.
    halign: 'center'
    valign: 'middle'
    text_size: self.size
    size_hint: .255, .0620
<FloatLayout>:
    id: selection
    canvas.before:
        BorderImage:
            source: 'jukebox.png'
            pos: self.pos
            size: self.size
    Label:
        id: jukebox_name
        text: "Convergence Music System 2.0"
        color: 0,0,0,1 # Sets text colour to black.
        font_size: 38
        bold: True
        halign: 'center'
        size_hint: .7, 1
        pos: 390,292
<PopupBox>:
    pop_up_text: _pop_up_text
    size_hint: 1, 1
    auto_dismiss: True
    title: 'Status'

    BoxLayout:
        orientation: "vertical"
        Label:
            id: _pop_up_text
            text: ''
''')

'''class PopupBox(Popup):
    pop_up_text = ObjectProperty()
    def update_pop_up_text(self, p_message):
        self.pop_up_text.text = p_message'''

class JukeboxScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(JukeboxScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.file_reader, 5)
        Window.bind(on_key_down=self.key_action)
        set_up_user_files_first_time()
        write_jukebox_startup_to_log()
        genre_read_and_select_engine()
        count_number_mp3_songs()
        '''progress_bar = ObjectProperty()  # Kivy properties classes are used when you create an EventDispatcher.
        self.progress_bar = ProgressBar()  # instance of ProgressBar created.
        self.popup = Popup(title='New Songs Detected: Updating Song Library',
                           content=self.progress_bar)  # progress bar assigned to popup
        self.popup.bind(on_open=self.puopen)  # Binds super widget to on_open.
        Clock.schedule_once(self.progress_bar_start)  # Uses clock to call progress_bar_start() (callback) one time only'''
        #popup = Popup(title='Test popup',content=Label(text='Hello world'),size_hint=(None, None), size=(400, 400))
        #popup.open()
        self.song_playing_name = Button(text=str(display_info[0]), pos=(580, 540), font_size=30, size_hint=(None, None),
                                        width=500)
        self.song_playing_artist = Button(text=str(display_info[1]), pos=(430, 490), font_size=30,
                                          size_hint=(None, None), width=800, halign="center", valign="middle")
        if len(display_info[0]) > 25:
            self.song_playing_name.font_size = 25
        elif len(display_info[0]) > 18:
            self.song_playing_name.font_size = 35
        else:
            self.song_playing_name.font_size = 50
        if len(display_info[1]) > 25:
            self.song_playing_artist.font_size = 25
        elif len(display_info[1]) > 18:
            self.song_playing_artist.font_size = 35
        else:
            self.song_playing_artist.font_size = 50
        self.sort_mode = Label(text="Sort Mode By Artist", pos=(42, 278), font_size=38)
        self.opening_message = Label(text=" ", color=(1, 1, 1, 1), pos=(200, 205), font_size=50, width=500,
                                     halign="center", valign="middle")
        self.licence_message = Label(text=" ", color=(1, 1, 1, 1), pos=(40, -66), font_size=20, width=500,
                                     halign="left", valign="top")
        self.my_first_title = Button(text=str(song_list[adder][0]), pos=(495, 456))
        self.my_first_artist = Button(text=str(song_list[adder][1]), pos=(495, 433))
        self.my_second_title = Button(text=str(song_list[adder + 1][0]), pos=(495, 403))
        self.my_second_artist = Button(text=str(song_list[adder + 1][1]), pos=(495, 380))
        self.my_third_title = Button(text=str(song_list[adder + 2][0]), pos=(495, 348))
        self.my_third_artist = Button(text=str(song_list[adder + 2][1]), pos=(495, 325))
        self.my_fourth_title = Button(text=str(song_list[adder + 3][0]), pos=(495, 293))
        self.my_fourth_artist = Button(text=str(song_list[adder + 3][1]), pos=(495, 270))
        self.my_fifth_title = Button(text=str(song_list[adder + 4][0]), pos=(495, 238))
        self.my_fifth_artist = Button(text=str(song_list[adder + 4][1]), pos=(495, 216))
        self.my_sixth_title = Button(text=str(song_list[adder + 5][0]), pos=(495, 185))
        self.my_sixth_artist = Button(text=str(song_list[adder + 5][1]), pos=(495, 162))
        self.my_seventh_title = Button(text=str(song_list[adder + 6][0]), pos=(495, 132))
        self.my_seventh_artist = Button(text=str(song_list[adder + 6][1]), pos=(495, 109))
        self.my_eigth_title = Button(text=str(song_list[adder + 7][0]), pos=(495, 77))
        self.my_eigth_artist = Button(text=str(song_list[adder + 7][1]), pos=(495, 54))
        self.my_ninth_title = Button(text=str(song_list[adder + 8][0]), pos=(835, 456))
        self.my_ninth_artist = Button(text=str(song_list[adder + 8][1]), pos=(835, 433))
        self.my_tenth_title = Button(text=str(song_list[adder + 9][0]), pos=(835, 403))
        self.my_tenth_artist = Button(text=str(song_list[adder + 9][1]), pos=(835, 380))
        self.my_eleventh_title = Button(text=str(song_list[adder + 10][0]), pos=(835, 348))
        self.my_eleventh_artist = Button(text=str(song_list[adder + 10][1]), pos=(835, 325))
        self.my_twelfth_title = Button(text=str(song_list[adder + 11][0]), pos=(835, 293))
        self.my_twelfth_artist = Button(text=str(song_list[adder + 11][1]), pos=(835, 270))
        self.my_thirteenth_title = Button(text=str(song_list[adder + 12][0]), pos=(835, 238))
        self.my_thirteenth_artist = Button(text=str(song_list[adder + 12][1]), pos=(835, 216))
        self.my_fourteenth_title = Button(text=str(song_list[adder + 13][0]), pos=(835, 185))
        self.my_fourteenth_artist = Button(text=str(song_list[adder + 13][1]), pos=(835, 162))
        self.my_fifteenth_title = Button(text=str(song_list[adder + 14][0]), pos=(835, 132))
        self.my_fifteenth_artist = Button(text=str(song_list[adder + 14][1]), pos=(835, 109))
        self.my_sixteenth_title = Button(text=str(song_list[adder + 15][0]), pos=(835, 77))
        self.my_sixteenth_artist = Button(text=str(song_list[adder + 15][1]), pos=(835, 54))
        self.my_play_mode = Label(text=str(display_info[5]), pos=(40, 245))
        self.my_title_song = Label(text="Title: " + str(display_info[0]), pos=(40, 225))
        self.my_title_artist = Label(text="Artist: " + str(display_info[1]), pos=(40, 205))
        self.my_title_year = Label(text="Year: " + str(display_info[3]), pos=(40, 185))
        self.my_title_length = Label(text="Length: " + str(display_info[4]), pos=(135, 185))
        self.my_title_album = Label(text="Album: " + str(display_info[2]), pos=(40, 165))
        selections_screen_starter(self)
        selections_screen_updater(self)
        self.my_upcoming_selections = Label(text="UPCOMING SELECTIONS", font_size=28, pos=(48, 132))
        self.my_play_cost = Label(text="Twenty-Five Cents Per Selection", pos=(50, -265), font_size=22)
        self.my_credit_amount = Label(text="CREDITS " + str(credit_amount), pos=(117, -236), font_size=35)
        self.selections_available = Label(text="Selections Available: " + str(selections_available), pos=(97, -287))
        self.my_blackout = Button(size_hint=(.547, .613), text=" ", background_color=(0, 0, 0, 0), pos=(480, 56),
                                  valign="top")
        self.add_widget(self.my_blackout)
        self.add_widget(self.my_upcoming_selections)
        self.add_widget(self.my_play_cost)
        self.add_widget(self.song_playing_name)
        self.add_widget(self.song_playing_artist)
        self.add_widget(self.my_selection_one)
        self.add_widget(self.my_selection_two)
        self.add_widget(self.my_selection_three)
        self.add_widget(self.my_selection_four)
        self.add_widget(self.my_selection_five)
        self.add_widget(self.my_selection_six)
        self.add_widget(self.my_selection_seven)
        self.add_widget(self.my_selection_eight)
        self.add_widget(self.my_selection_nine)
        self.add_widget(self.my_selection_ten)
        self.add_widget(self.my_selection_eleven)
        self.add_widget(self.my_selection_twelve)
        self.add_widget(self.my_selection_thirteen)
        self.add_widget(self.my_selection_fourteen)
        self.add_widget(self.my_selection_fifteen)
        self.add_widget(self.my_selection_sixteen)
        self.add_widget(self.my_selection_seventeen)
        self.add_widget(self.my_credit_amount)
        self.add_widget(self.selections_available)
        self.add_widget(self.sort_mode)
        self.add_widget(self.my_play_mode)
        self.add_widget(self.my_title_song)
        self.add_widget(self.my_title_artist)
        self.add_widget(self.my_title_year)
        self.add_widget(self.my_title_length)
        self.add_widget(self.my_title_album)
        self.add_widget(self.my_first_title)
        self.add_widget(self.my_first_artist)
        self.add_widget(self.my_second_title)
        self.add_widget(self.my_second_artist)
        self.add_widget(self.my_third_title)
        self.add_widget(self.my_third_artist)
        self.add_widget(self.my_fourth_title)
        self.add_widget(self.my_fourth_artist)
        self.add_widget(self.my_fifth_title)
        self.add_widget(self.my_fifth_artist)
        self.add_widget(self.my_sixth_title)
        self.add_widget(self.my_sixth_artist)
        self.add_widget(self.my_seventh_title)
        self.add_widget(self.my_seventh_artist)
        self.add_widget(self.my_eigth_title)
        self.add_widget(self.my_eigth_artist)
        self.add_widget(self.my_ninth_title)
        self.add_widget(self.my_ninth_artist)
        self.add_widget(self.my_tenth_title)
        self.add_widget(self.my_tenth_artist)
        self.add_widget(self.my_eleventh_title)
        self.add_widget(self.my_eleventh_artist)
        self.add_widget(self.my_twelfth_title)
        self.add_widget(self.my_twelfth_artist)
        self.add_widget(self.my_thirteenth_title)
        self.add_widget(self.my_thirteenth_artist)
        self.add_widget(self.my_fourteenth_title)
        self.add_widget(self.my_fourteenth_artist)
        self.add_widget(self.my_fifteenth_title)
        self.add_widget(self.my_fifteenth_artist)
        self.add_widget(self.my_sixteenth_title)
        self.add_widget(self.my_sixteenth_artist)
        self.add_widget(self.opening_message)
        self.add_widget(self.licence_message)
        if start_up != 0:
            self.my_first_title.background_color = (160, 160, 160, .2)
            self.my_first_artist.background_color = (160, 160, 160, .2)
        selection_font_size(self)
        os.system("RunConvergencePlayer2.exe")  # Launches Convergence Jukebox Player

    '''def show_popup(self):
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text('Running some task...')
        self.pop_up.open()'''

    '''def process_button_click(self):
        # Open the pop up
        self.show_popup()
        mythread = threading.Thread(target=self.something_that_takes_5_seconds_to_run)
        mythread.start()

    def something_that_takes_5_seconds_to_run(self):
        thistime = time.time()
        while thistime + 5 > time.time():  # 5 seconds
            print "Hello, world!"
            time.sleep(1)
        self.pop_up.dismiss()'''

    ''' def progress_bar_start(self, instance):  # Provides initial value of of progress bar and lanches popup
        self.progress_bar.value = 1  # Initial value of progress_bar
        self.popup.open()  # starts puopen()

    def next(self, dt):  # Updates Project Bar
        if self.progress_bar.value >= 100:  # Checks to see if progress_bar.value has met 100
            return False  # Returning False schedule is canceled and won't repeat
        self.progress_bar.value += 1  # Updates progress_bar's progress

    def puopen(self, instance):  # Called from bind.
        Clock.schedule_interval(self.next, 1)  # Creates Clock event scheduling next() every 5-1000th of a second.'''

    def key_action(self, *args):  # Keyboard Reader Code. https://gist.github.com/tshirtman/31bb4d3e482261191a1f
        global adder
        global screen_number
        global cursor_position
        global last_pressed
        global song_selection_number
        key_event = list(args)
        global display_info
        global upcoming_list
        global start_up
        global full_path
        global current_file_count
        global song_list
        global delete_indicator
        global random_list
        print "Key Number Pressed Is: " + str(key_event[1])
        if str(key_event[1]) == '122':  # test
            popup = Popup(title='Test popup', content=Label(text='Hello world'), size_hint=(None, None),
                          size=(400, 400))
            popup.open()

        if str(key_event[1]) == '111':  # Opening Screen
            last_pressed = "o"
            screen_message = "Welcome To Convergence Jukebox\nYour Jukebox Is Being Configured\nThis Could Take A Few Minutes\n\n"
            self.opening_message.text = "Welcome To Convergence\n Jukebox Windows Edition"
            self.licence_message.text = str(licence)
            # self.process_button_click()
            # self.parent.remove_widget(self.my_progress_bar)
            # self.remove_widget(self.my_progress_bar)
            self.my_first_title.background_color = (160, 160, 160, 0)
            self.my_first_artist.background_color = (160, 160, 160, 0)
            self.my_blackout.background_color = (0, 0, 0, 1)
            self.my_blackout.text = screen_message
            self.my_blackout.color = (1, 1, 1, 1)
            self.my_blackout.font_size = 25
            self.my_upcoming_selections.color = (0, .7, 0, 0)
            self.my_play_cost.color = (0, .7, 0, 0)
            self.my_credit_amount.color = (0, .7, 0, 0)
            self.selections_available.color = (0, .7, 0, 0)
            self.song_playing_name.color = (1, 1, 1, 0)
            self.song_playing_artist.color = (1, 1, 1, 0)
            self.my_play_mode.color = (0, .7, 0, 0)
            self.my_title_song.color = (0, .7, 0, 0)
            self.my_title_artist.color = (0, .7, 0, 0)
            self.my_title_year.color = (0, .7, 0, 0)
            self.my_title_length.color = (0, .7, 0, 0)
            self.my_title_album.color = (0, .7, 0, 0)
            self.sort_mode.color = (0, .7, 0, 0)
            self.my_first_title.color = (1, 1, 1, 0)
            self.my_first_artist.color = (1, 1, 1, 0)
            self.my_second_title.color = (1, 1, 1, 0)
            self.my_second_artist.color = (1, 1, 1, 0)
            self.my_third_title.color = (1, 1, 1, 0)
            self.my_third_artist.color = (1, 1, 1, 0)
            self.my_fourth_title.color = (1, 1, 1, 0)
            self.my_fourth_artist.color = (1, 1, 1, 0)
            self.my_fifth_title.color = (1, 1, 1, 0)
            self.my_fifth_artist.color = (1, 1, 1, 0)
            self.my_sixth_title.color = (1, 1, 1, 0)
            self.my_sixth_artist.color = (1, 1, 1, 0)
            self.my_seventh_title.color = (1, 1, 1, 0)
            self.my_seventh_artist.color = (1, 1, 1, 0)
            self.my_eigth_title.color = (1, 1, 1, 0)
            self.my_eigth_artist.color = (1, 1, 1, 0)
            self.my_ninth_title.color = (1, 1, 1, 0)
            self.my_ninth_artist.color = (1, 1, 1, 0)
            self.my_tenth_title.color = (1, 1, 1, 0)
            self.my_tenth_artist.color = (1, 1, 1, 0)
            self.my_eleventh_title.color = (1, 1, 1, 0)
            self.my_eleventh_artist.color = (1, 1, 1, 0)
            self.my_twelfth_title.color = (1, 1, 1, 0)
            self.my_twelfth_artist.color = (1, 1, 1, 0)
            self.my_thirteenth_title.color = (1, 1, 1, 0)
            self.my_thirteenth_artist.color = (1, 1, 1, 0)
            self.my_fourteenth_title.color = (1, 1, 1, 0)
            self.my_fourteenth_artist.color = (1, 1, 1, 0)
            self.my_fifteenth_title.color = (1, 1, 1, 0)
            self.my_fifteenth_artist.color = (1, 1, 1, 0)
            self.my_sixteenth_title.color = (1, 1, 1, 0)
            self.my_sixteenth_artist.color = (1, 1, 1, 0)
            self.my_selection_one.text = " "
            self.my_selection_two.text = " "
            self.my_selection_three.text = " "
            self.my_selection_four.text = " "
            self.my_selection_five.text = " "
            self.my_selection_six.text = " "
            self.my_selection_seven.text = " "
            self.my_selection_eight.text = " "
            self.my_selection_nine.text = " "
            self.my_selection_ten.text = " "
            self.my_selection_eleven.text = " "
            self.my_selection_twelve.text = " "
            self.my_selection_thirteen.text = " "
            self.my_selection_fourteen.text = " "
            self.my_selection_fifteen.text = " "
            self.my_selection_sixteen.text = " "
            self.my_selection_seventeen.text = " "
            if sys.platform.startswith('linux'):
                # Needs to be written when testing on Raspberry Pi
                # This needs to heck Raspberry Pi has 720p resolution.
                pass
            if sys.platform == 'win32':  # Checks if music directory exists. If not it creates it and advises of mp3 need.
                if os.path.exists(str(os.path.dirname(full_path)) + "\music"):
                    screen_message_update = screen_message + " Music directory exists at " \
                                            + str(os.path.dirname(full_path)) + "\music.\nNothing to do here"
                    self.my_blackout.text = screen_message_update
                else:
                    screen_message_update = screen_message + "Music directory does not exist\n" + " Program Stopped" \
                                                                                                  " And Will Terminate In Ten Seconds.\nPlease place fifty mp3's in the\n" \
                                                                                                  "Convergence Jukebox music directory at\n" + str(
                        os.path.dirname(full_path)) + "\music\n" \
                                                      "and then re-run the Convergence Jukebox software"
                    self.my_blackout.background_color = (1, 0, 0, 1)
                    self.my_blackout.text = screen_message_update
                    os.makedirs(str(os.path.dirname(full_path)) + "\music")
            if sys.platform.startswith('linux'):  # Needs to be rewritten during Raspberry Pi testing.
                if os.path.exists(str(os.path.dirname(full_path)) + "/music"):
                    print "music directory exists at " + str(
                        os.path.dirname(full_path)) + "Adding underscores to MP3 Files."
                    current_path = os.getcwd()
                    path = str(current_path) + "/music"
                    os.chdir(path)  # sets path for mpg321
                    [os.rename(f, f.replace(' ', '_')) for f in os.listdir('.') if not f.startswith('.')]
                else:
                    print "music directory does not exist."
                    os.makedirs(str(os.path.dirname(full_path)) + "/music")
            print "last_file_count = " + str(last_file_count)
            print "current_file_count  " + str(current_file_count)
            print "len song_list = " + str(len(song_list))
            # sys.exit()
            #popup = Popup(title='Test popup', content=Label(text='Hello world'), size_hint=(None, None), size=(400, 400))
            #popup.open()

            '''if len(song_list) == 16:
                sys.exit()'''
            if last_file_count == current_file_count or len(song_list) != 16:  # If matched the song_list is loaded from file
                screen_message_update = screen_message + "Jukebox music files same as last startup.\n" \
                                                         "Using existing song database."
                self.my_blackout.text = screen_message_update
                print "Jukebox music files same as last startup. Using existing song database."  # Message to console.
            else:  # New song_list, filecount and location_list generated and saved.
                print "I'm here."
                #sys.exit()
                song_list_generate = []
                build_list = []
                location_list = []
                time_date_stamp = datetime.datetime.now().strftime(
                    "%A. %d. %B %Y %I:%M%p")  # Timestamp generate bit.ly/1MKPl5x
                log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                log_file_entry.write(str(time_date_stamp + ',' + 'New song_list generated' + ',' + '\n'))
                log_file_entry.close()
                # Code below writes log entry to computers dropbox public directory for remote log access
                if os.path.exists(
                        str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"))):
                    log_file_update = open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                                           + computer_account_user_name.lower() + "log.txt", "a+")
                    log_file_update.write(str(time_date_stamp + ',' + 'New song_list generated' + ',' + '\n'))
                    log_file_update.close()
                file_count_update = open("file_count.txt", "w+")  # Writes new filecount to filecount.txt.
                s = str(current_file_count)
                file_count_update.write(s)
                file_count_update.close()
                location_list = []  # Creates temporary location_list used for initial song file names for mp3 player.
                # File names later inserted in song_list to be used to play mp3's
                full_path = os.path.realpath('__file__')
                if sys.platform == 'win32':
                    for name in os.listdir(str(
                            os.path.dirname(full_path)) + "\music" + "\\"):  # Reads files in the music dir.
                        if name.endswith(".mp3"):  # If statement searching for files with mp3 designation
                            title = name  # Name of mp3 transferred to title variable
                            location_list.append(title)  # Name of song appended to location_list
                if sys.platform.startswith('linux'):
                    for name in os.listdir(
                                    str(os.path.dirname(full_path)) + "/music"):  # Reads files in the music dir.
                        if name.endswith(".mp3"):  # If statement searching for files with mp3 designation
                            title = name  # Name of mp3 transferred to title variable
                            location_list.append(title)  # Name of song appended to location_list
                x = 0  # hsaudiotag 1.1.1 code begins here to pull out ID3 information
                while x < len(
                        location_list):  # Python List len function http://docs.python.org/2/library/functions.html#len
                    if sys.platform == 'win32':
                        myfile = auto.File(
                            str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x] + "")
                    if sys.platform.startswith('linux'):
                        myfile = auto.File(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x] + "")
                    # Note "" Quotes Required in above string.
                    # hsaudiotag function that assigns mp3 song to myfile object
                    screen_message_update = screen_message + "Building Song Database. Stand By.\n" \
                                                             "This can take some time."
                    self.my_blackout.text = screen_message_update
                    print "Building Song Database. Stand By. This can take some time"
                    albumorg = myfile.album  # Assigns above mp3 ID3 Album name to albumorg variable
                    yearorg = myfile.year  # Assigns above mp3 ID3 Year info to yearorg variable
                    durationorgseconds = myfile.duration  # Assigns mp3 Duration (in seconds) info to durationorgseconds var.
                    genreorg = myfile.genre  # Assigns above mp3 Genre info to genreorg variable
                    commentorg = myfile.comment  # Assigns above mp3 Comment info to commentorg variable
                    build_list.append(myfile.title)  # Title of song appended to build_list
                    try:  # http://www.pythonlovers.net/python-exceptions-handling
                        unicode_crash_test = str(myfile.title)  # Causes crash if Unicode found in Artist Name
                    except UnicodeEncodeError:
                        print str(location_list[x])
                        # bad_file_name = str(location_list[x])
                        file_name_with_error = str(location_list[x])
                        log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                        log_file_entry.write(str(
                            file_name_with_error + ' was deleted because of a Unicode character in its ID3 Title data.' + '\n'))
                        log_file_entry.close()
                        print "Title Unicode Error"
                        if sys.platform == 'win32':
                            print "Removing " + str(location_list[x])
                            os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                        if sys.platform.startswith('linux'):
                            os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                        delete_indicator = "yes"
                        if location_list[x] in build_list:
                            print "We need to delete " + str(location_list[x]) + " here Unicode title."
                    try:  # http://www.pythonlovers.net/python-exceptions-handling
                        unicode_crash_test = str(myfile.artist)  # Causes crash if Unicode found in Artist Name
                    except UnicodeEncodeError:
                        print str(location_list[x])
                        # bad_file_name = str(location_list[x])
                        file_name_with_error = str(location_list[x])
                        log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                        log_file_entry.write(str(
                            file_name_with_error + ' was deleted because of a Unicode character in its ID3 Artist data.' + '\n'))
                        log_file_entry.close()
                        print "Artist Unicode Error"
                        if sys.platform == 'win32':
                            print "Removing " + str(location_list[x])
                            os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                        if sys.platform.startswith('linux'):
                            os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                        delete_indicator = "yes"
                        if location_list[x] in build_list:
                            print "We need to delete " + str(location_list[x]) + " here Unicode title."
                    try:  # http://www.pythonlovers.net/python-exceptions-handling
                        unicode_crash_test = str(myfile.comment)  # Causes crash if Unicode found in Artist Name
                    except UnicodeEncodeError:
                        print str(location_list[x])
                        # bad_file_name = str(location_list[x])
                        file_name_with_error = str(location_list[x])
                        log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                        log_file_entry.write(str(
                            file_name_with_error + ' was deleted because of a Unicode character in its ID3 Comment data.' + '\n'))
                        log_file_entry.close()
                        print "Comment Unicode Error"
                        if sys.platform == 'win32':
                            print "Removing " + str(location_list[x])
                            os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                        if sys.platform.startswith('linux'):
                            os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                        delete_indicator = "yes"
                        if location_list[x] in build_list:
                            print "We need to delete " + str(location_list[x]) + " here Unicode title."
                    if myfile.artist == "":  # Check for invalid Artist mp3 ID tag
                        print str(location_list[x])
                        # bad_file_name = str(location_list[x])
                        file_name_with_error = str(location_list[x])
                        print str(location_list[
                                      x]) + "'s Artist ID3 tag is not valid for Convergence Jukebox. Please correct or remove from media folder."
                        log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                        log_file_entry.write(
                            str(
                                file_name_with_error + ' was deleted because its ID3 Artist data is not valid.' + '\n'))
                        log_file_entry.close()
                        if sys.platform == 'win32':
                            print "Removing " + str(location_list[x])
                            os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                        if sys.platform.startswith('linux'):
                            os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                        delete_indicator = "yes"
                        if location_list[x] in build_list:
                            print "We need to delete " + str(location_list[x]) + " here Unicode title."
                    if myfile.title == "":  # Check for invalid mp3 Title ID tag
                        print str(location_list[x])
                        # bad_file_name = str(location_list[x])
                        file_name_with_error = str(location_list[x])
                        print str(location_list[
                                      x]) + "'s Title ID3 tag is not valid for Convergence Jukebox. Please correct or remove from media folder."
                        log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                        log_file_entry.write(
                            str(
                                file_name_with_error + ' was deleted because its ID3 Title data is not valid.' + '\n'))
                        log_file_entry.close()
                        if sys.platform == 'win32':
                            print "Removing " + str(location_list[x])
                            os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                        if sys.platform.startswith('linux'):
                            os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                        delete_indicator = "yes"
                        if location_list[x] in build_list:
                            print "We need to delete " + str(location_list[x]) + " here Unicode title."
                    if x == 0:
                        database_indicator()
                    if delete_indicator == "yes":
                        file_count_update = open("file_count.txt", "w+")  # Writes new filecount to filecount.txt.
                        s = str(0)
                        file_count_update.write(s)
                        file_count_update.close()
                    if delete_indicator != "yes":
                        build_list.append(myfile.artist)  # Artist of song appended to build_list
                        build_list.append(myfile.album)  # Album title of song appended to build_list
                        build_list.append(myfile.year)  # Year of song appended to build_list
                        build_list.append(myfile.duration)  # Duration of song in seconds appended to build_list
                        build_list.append(myfile.genre)  # Genre of song appended to build_list
                        durationtimefull = str(
                            datetime.timedelta(seconds=durationorgseconds))  # Info at http://bit.ly/1L5pU9t
                        durationtime = durationtimefull[
                                       3:7]  # Slices string to minute:second notation. http://bit.ly/1QphhOW
                        build_list.append(
                            durationtime)  # Time of song in minutes/seconds of song appended to build_list
                        build_list.append(myfile.comment)  # Comment in ID3 data appended to build_list
                        full_file_name = str(location_list[x])
                        if sys.platform.startswith('linux'):
                            title_with_whitespace = full_file_name
                            title_without_whitespace = title_with_whitespace.replace(" ", "_")
                            full_file_name = title_without_whitespace
                            current_path = os.getcwd()
                            temp_path = str(current_path) + '/music'
                            os.chdir(temp_path)  # resets path
                            os.rename(str(title_with_whitespace), str(title_without_whitespace))
                            os.chdir(current_path)  # resets path
                        build_list.append(full_file_name)
                        song_list_generate.append(build_list)
                        build_list.append(x)
                        print location_list[x]
                        print "Name: " + str(build_list[8])
                        print build_list
                        screen_message_update = screen_message + "Building Song Database. Stand By.\n" \
                                                                 "This can take some time.\nAdding: " + str(
                            build_list[8])
                        self.my_blackout.text = screen_message_update
                        build_list = []
                        y = len(location_list) - x
                        # print "www.convergencejukebox.com Building your database " + str(full_file_name) + ". " + str(y) + \
                        # " files remaining to process."
                    delete_indicator = ""
                    print x
                    x += 1
                for i in range(0, 16):  # Adds blank songs to end of sont_list
                    song_list_generate.append(
                        [u'zzzzz', u'zzzzz', u' ', u' ', u' ', u' ', u' ', u' ', 'zzzzz - zzzzz.mp3', u' '])

                song_list_save = open('song_list.pkl', 'wb')  # song_list saved as binary pickle file
                pickle.dump(song_list_generate, song_list_save)
                song_list_save.close()
                song_list = song_list_generate
                song_list.sort(key=itemgetter(1), reverse=False)

            mp3_counter = len(
                glob.glob1(str(os.path.dirname(full_path)) + "/music", "*.mp3"))  # Counts number of MP3 files
            current_file_count = int(mp3_counter)  # provides int output for later comparison
            screen_message_update = screen_message + " Number of songs at startup: " + str(current_file_count)
            self.my_blackout.text = screen_message_update

            if int(mp3_counter) < 50:
                screen_message_update = screen_message + "Not Enough MP3's To Start Convergence Jukebox\n" \
                                        + " Program Stopped" \
                                          " And Will Terminate In Ten Seconds.\nPlease place fifty mp3's in the\n" \
                                          "Convergence Jukebox music directory at\n" + str(
                    os.path.dirname(full_path)) + "\music\n" \
                                                  "and then re-run the Convergence Jukebox software"
                self.my_blackout.background_color = (1, 0, 0, 1)
                self.my_blackout.text = screen_message_update

        if str(key_event[1]) == '114':
            global song_status
            global random_list
            x = random_list[0]
            print "About to randomly play: " + str(song_list[x][8])
            print song_status
            print "Letter r pressed. "

            title = str(song_list[x][0])
            artist = str(song_list[x][1])
            album = str(song_list[x][2])
            year = str(song_list[x][3])
            time = str(song_list[x][4])

            mode = "Mode: Playing Song"
            print "Title: " + title
            print "Artist: " + artist
            print "Album: " + album
            print "Year Released: " + year + " Time: " + time
            output_prep = title + "," + artist + "," + album + "," + year + "," + time + "," + mode
            output_list_save = open("output_list.txt", "w")
            output_list_save.write(str(output_prep))
            output_list_save.close()
            time_date_stamp = datetime.datetime.now().strftime("%A. %d. %B %Y %I:%M%p")
            log_file_entry = open("log.txt", "a+")
            log_file_entry.write(
                str(time_date_stamp + ',' + str(song_list[x][8]) + ',' + str(mode) + ',' + '0' + '\n'))
            log_file_entry.close()
            # Code below writes log entry to computers dropbox public directory for remote log access
            if os.path.exists(
                    str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"))):
                log_file_update = open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                                       + computer_account_user_name.lower() + "log.txt", "a+")
                log_file_update.write(
                    str(time_date_stamp + ',' + str(song_list[x][8]) + ',' + str(mode) + ',' + '0' + '\n'))
                log_file_update.close()
            full_path = os.path.realpath('__file__')
            print "Now playing: " + str(x)

            playMP3(
                str(os.path.dirname(full_path)) + '\music' + '\\\\' + song_list[x][8])  # Plays song using mp3Play.
            del random_list[0]
            song_status = "finished"
            print song_status

        if str(key_event[1]) == '47':  # Changes sort mode to title
            last_pressed = "forward slash"
            if self.sort_mode.text != "Sort Mode By Title":
                print "Sorting by Title"
                song_list.sort(key=itemgetter(0), reverse=False)
                self.sort_mode.text = "Sort Mode By Title"
            else:
                print "Sorting by Artist"
                song_list.sort(key=itemgetter(1), reverse=False)
                self.sort_mode.text = "Sort Mode By Artist"
            screen_number_base = .9  # This triggers a reset of the title/artist display
        try:
            if str(key_event[1]) == '97':
                print 'a'
                if self.sort_mode.text == "Sort Mode By Title":
                    if last_pressed == "aa":
                        print "I should be b"
                        last_pressed = "aaa"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "B":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "aaa":
                        print "I should be c"
                        last_pressed = "a"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "C":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be a"
                        last_pressed = "aa"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "A":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                else:
                    if last_pressed == "aa":
                        print "I should be b"
                        last_pressed = "aaa"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "B":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "aaa":
                        print "I should be c"
                        last_pressed = "a"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "C":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be the letter a"
                        print adder
                        print cursor_position
                        last_pressed = "aa"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "A":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
        except IndexError:
            return
        if str(key_event[1]) == '98':  # b keyboard key updates display on song change
            print upcoming_list
            # my_old_infinite_loop()
            self.my_blackout.color = (1, 1, 1, 0)
            self.my_first_title.color = (1, 1, 1, 1)
            self.my_first_artist.color = (1, 1, 1, 1)
            self.my_second_title.color = (1, 1, 1, 1)
            self.my_second_artist.color = (1, 1, 1, 1)
            self.my_third_title.color = (1, 1, 1, 1)
            self.my_third_artist.color = (1, 1, 1, 1)
            self.my_fourth_title.color = (1, 1, 1, 1)
            self.my_fourth_artist.color = (1, 1, 1, 1)
            self.my_fifth_title.color = (1, 1, 1, 1)
            self.my_fifth_artist.color = (1, 1, 1, 1)
            self.my_sixth_title.color = (1, 1, 1, 1)
            self.my_sixth_artist.color = (1, 1, 1, 1)
            self.my_seventh_title.color = (1, 1, 1, 1)
            self.my_seventh_artist.color = (1, 1, 1, 1)
            self.my_eigth_title.color = (1, 1, 1, 1)
            self.my_eigth_artist.color = (1, 1, 1, 1)
            self.my_ninth_title.color = (1, 1, 1, 1)
            self.my_ninth_artist.color = (1, 1, 1, 1)
            self.my_tenth_title.color = (1, 1, 1, 1)
            self.my_tenth_artist.color = (1, 1, 1, 1)
            self.my_eleventh_title.color = (1, 1, 1, 1)
            self.my_eleventh_artist.color = (1, 1, 1, 1)
            self.my_twelfth_title.color = (1, 1, 1, 1)
            self.my_twelfth_artist.color = (1, 1, 1, 1)
            self.my_thirteenth_title.color = (1, 1, 1, 1)
            self.my_thirteenth_artist.color = (1, 1, 1, 1)
            self.my_fourteenth_title.color = (1, 1, 1, 1)
            self.my_fourteenth_artist.color = (1, 1, 1, 1)
            self.my_fifteenth_title.color = (1, 1, 1, 1)
            self.my_fifteenth_artist.color = (1, 1, 1, 1)
            self.my_sixteenth_title.color = (1, 1, 1, 1)
            self.my_sixteenth_artist.color = (1, 1, 1, 1)
            self.my_blackout.background_color = (0, 0, 0, 0)
            self.my_upcoming_selections.color = (0, .7, 0, 1)
            self.my_play_cost.color = (0, .7, 0, 1)
            self.my_credit_amount.color = (0, .7, 0, 1)
            self.selections_available.color = (0, .7, 0, 1)
            self.song_playing_name.color = (1, 1, 1, 1)
            self.song_playing_artist.color = (1, 1, 1, 1)
            self.my_play_mode.color = (0, .7, 0, 1)
            self.my_title_song.color = (0, .7, 0, 1)
            self.my_title_artist.color = (0, .7, 0, 1)
            self.my_title_year.color = (0, .7, 0, 1)
            self.my_title_length.color = (0, .7, 0, 1)
            self.my_title_album.color = (0, .7, 0, 1)
            self.sort_mode.color = (0, .7, 0, 1)
            self.opening_message.text = " "
            self.licence_message.text = " "
            self.my_selection_one.text = " "
            self.my_selection_two.text = " "
            self.my_selection_three.text = " "
            self.my_selection_four.text = " "
            self.my_selection_five.text = " "
            self.my_selection_six.text = " "
            self.my_selection_seven.text = " "
            self.my_selection_eight.text = " "
            self.my_selection_nine.text = " "
            self.my_selection_ten.text = " "
            self.my_selection_eleven.text = " "
            self.my_selection_twelve.text = " "
            self.my_selection_thirteen.text = " "
            self.my_selection_fourteen.text = " "
            self.my_selection_fifteen.text = " "
            self.my_selection_sixteen.text = " "
            self.my_selection_seventeen.text = " "
            try:
                if upcoming_list:
                    if upcoming_list[0]:
                        self.my_selection_one.text = upcoming_list[0]
                    if upcoming_list[1]:
                        self.my_selection_two.text = upcoming_list[1]
                    if upcoming_list[2]:
                        self.my_selection_three.text = upcoming_list[2]
                    if upcoming_list[3]:
                        self.my_selection_four.text = upcoming_list[3]
                    if upcoming_list[4]:
                        self.my_selection_five.text = upcoming_list[4]
                    if upcoming_list[5]:
                        self.my_selection_six.text = upcoming_list[5]
                    if upcoming_list[6]:
                        self.my_selection_seven.text = upcoming_list[6]
                    if upcoming_list[7]:
                        self.my_selection_eight.text = upcoming_list[7]
                    if upcoming_list[8]:
                        self.my_selection_nine.text = upcoming_list[8]
                    if upcoming_list[9]:
                        self.my_selection_ten.text = upcoming_list[9]
                    if upcoming_list[10]:
                        self.my_selection_eleven.text = upcoming_list[10]
                    if upcoming_list[11]:
                        self.my_selection_twelve.text = upcoming_list[11]
                    if upcoming_list[12]:
                        self.my_selection_thirteen.text = upcoming_list[12]
                    if upcoming_list[13]:
                        self.my_selection_fourteen.text = upcoming_list[13]
                    if upcoming_list[14]:
                        self.my_selection_fifteen.text = upcoming_list[14]
                    if upcoming_list[15]:
                        self.my_selection_sixteen.text = upcoming_list[15]
                    if upcoming_list[16]:
                        self.my_selection_seventeen.text = upcoming_list[16]
            except IndexError:
                pass
            display_info_recover = open("output_list.txt", 'r+')
            output_list_read = display_info_recover.read()
            display_info_recover.close()
            display_info = output_list_read.split(",")
            print display_info
            self.song_playing_name.text = str(display_info[0])
            self.song_playing_artist.text = str(display_info[1])
            if len(display_info[0]) > 25:
                self.song_playing_name.font_size = 25
            elif len(display_info[0]) > 18:
                self.song_playing_name.font_size = 35
            else:
                self.song_playing_name.font_size = 50
            if len(display_info[1]) > 25:
                self.song_playing_artist.font_size = 25
            elif len(display_info[1]) > 18:
                self.song_playing_artist.font_size = 35
            else:
                self.song_playing_artist.font_size = 50

            x = self.song_playing_artist.text
            if x.lower() in the_bands_list_lower_case:
                x = "The " + str(x)
                self.song_playing_artist.text = str(x)

            self.my_title_song.text = "Title: " + str(display_info[0])
            self.my_title_artist.text = "Artist: " + str(display_info[1])
            self.my_title_album.text = "Release: " + str(display_info[2])
            self.my_title_year.text = "Year: " + str(display_info[3])
            self.my_title_length.text = "Length: " + str(display_info[4])
            self.my_play_mode.text = str(display_info[5])

        try:
            if str(key_event[1]) == '100':
                print 'd'
                if self.sort_mode.text == "Sort Mode By Title":
                    if last_pressed == "dd":
                        print "I should be e"
                        last_pressed = "ddd"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "E":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "ddd":
                        print "I should be f"
                        last_pressed = "d"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "F":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be d"
                        last_pressed = "dd"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "D":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                else:
                    if last_pressed == "dd":
                        print "I should be e"
                        last_pressed = "ddd"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "E":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "ddd":
                        print "I should be f"
                        last_pressed = "d"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "F":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be the letter d"
                        print adder
                        print cursor_position
                        last_pressed = "dd"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "D":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
            if str(key_event[1]) == '103':
                print 'g'
                if self.sort_mode.text == "Sort Mode By Title":
                    if last_pressed == "gg":
                        print "I should be h"
                        last_pressed = "ggg"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "H":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "ggg":
                        print "I should be i"
                        last_pressed = "g"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "I":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be g"
                        last_pressed = "gg"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "G":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                else:
                    if last_pressed == "gg":
                        print "I should be h"
                        last_pressed = "ggg"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "H":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "ggg":
                        print "I should be i"
                        last_pressed = "d"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "I":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be the letter g"
                        print adder
                        print cursor_position
                        last_pressed = "gg"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "G":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
            if str(key_event[1]) == '106':
                print 'j'
                if self.sort_mode.text == "Sort Mode By Title":
                    if last_pressed == "jj":
                        print "I should be k"
                        last_pressed = "jjj"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "K":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "jjj":
                        print "I should be l"
                        last_pressed = "j"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "L":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be j"
                        last_pressed = "jj"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "J":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                else:
                    if last_pressed == "jj":
                        print "I should be k"
                        last_pressed = "jjj"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "K":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "jjj":
                        print "I should be l"
                        last_pressed = "j"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "L":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be the letter j"
                        print adder
                        print cursor_position
                        last_pressed = "jj"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "J":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
            if str(key_event[1]) == '109':
                print 'm'
                if self.sort_mode.text == "Sort Mode By Title":
                    if last_pressed == "mm":
                        print "I should be n"
                        last_pressed = "mmm"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "N":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "mmm":
                        print "I should be o"
                        last_pressed = "m"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "O":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be m"
                        last_pressed = "mm"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "M":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                else:
                    if last_pressed == "mm":
                        print "I should be n"
                        last_pressed = "mmm"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "N":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "mmm":
                        print "I should be o"
                        last_pressed = "m"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "O":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be the letter m"
                        print adder
                        print cursor_position
                        last_pressed = "mm"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "M":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
            if str(key_event[1]) == '112':
                print 'p'
                if self.sort_mode.text == "Sort Mode By Title":
                    if last_pressed == "pp":
                        print "I should be q"
                        last_pressed = "ppp"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "Q":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "ppp":
                        print "I should be r"
                        last_pressed = "p"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "R":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be p"
                        last_pressed = "pp"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "P":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                else:
                    if last_pressed == "pp":
                        print "I should be q"
                        last_pressed = "ppp"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "Q":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "ppp":
                        print "I should be r"
                        last_pressed = "p"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "R":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be the letter p"
                        print adder
                        print cursor_position
                        last_pressed = "pp"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "P":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
            if str(key_event[1]) == '115':
                print 'p'
                if self.sort_mode.text == "Sort Mode By Title":
                    print "I should be s"
                    last_pressed = "s"
                    first_index_of_letter = []
                    for x in range(0, len(song_list)):
                        if song_list[x][0][0] == "S":
                            first_index_of_letter.append(x)
                    adder = first_index_of_letter[0]
                else:
                    print "I should be the letter s"
                    print adder
                    print cursor_position
                    last_pressed = "s"
                    first_index_of_letter = []
                    for x in range(0, len(song_list)):
                        if song_list[x][1][0] == "S":
                            first_index_of_letter.append(x)
                    adder = first_index_of_letter[0]
            if str(key_event[1]) == '116':
                print 't'
                if self.sort_mode.text == "Sort Mode By Title":
                    if last_pressed == "tt":
                        print "I should be u"
                        last_pressed = "ttt"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "U":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "ttt":
                        print "I should be v"
                        last_pressed = "t"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "V":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be t"
                        last_pressed = "tt"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "T":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                else:
                    if last_pressed == "tt":
                        print "I should be u"
                        last_pressed = "ttt"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "U":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "ttt":
                        print "I should be v"
                        last_pressed = "t"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "V":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be the letter t"
                        print adder
                        print cursor_position
                        last_pressed = "tt"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "T":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
            if str(key_event[1]) == '119':
                print 'w'
                if self.sort_mode.text == "Sort Mode By Title":
                    if last_pressed == "ww":
                        print "I should be x"
                        last_pressed = "www"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "X":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "www":
                        print "I should be y"
                        last_pressed = "wwww"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "Y":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "wwww":
                        print "I should be z"
                        last_pressed = "w"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "Z":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be w"
                        last_pressed = "ww"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][0][0] == "W":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                else:
                    if last_pressed == "ww":
                        print "I should be x"
                        last_pressed = "www"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "X":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "www":
                        print "I should be y"
                        last_pressed = "wwww"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "Y":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    elif last_pressed == "wwww":
                        print "I should be z"
                        last_pressed = "w"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "Z":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
                    else:
                        print "I should be the letter w"
                        print adder
                        print cursor_position
                        last_pressed = "ww"
                        first_index_of_letter = []
                        for x in range(0, len(song_list)):
                            if song_list[x][1][0] == "W":
                                first_index_of_letter.append(x)
                        adder = first_index_of_letter[0]
        except IndexError:
            return
        if str(key_event[1]) == '120':
            print 'x'
            credit_calculator()
            last_pressed = "x"
            print credit_amount
            self.my_credit_amount.text = "CREDITS " + str(credit_amount)
        if str(key_event[1]) == '273':
            print 'up'
            adder -= 1
            if adder < 0:
                adder = 0
            last_pressed = "up"
        if str(key_event[1]) == '274':
            print 'down'
            adder += 1
            if adder >= len(song_list) - 16:
                adder = len(song_list)
            last_pressed = "down"
        if str(key_event[1]) == '275':
            print 'right'
            adder += 8
            if adder > len(song_list) - 16:
                adder = len(song_list)
            last_pressed = "right"
        if str(key_event[1]) == '276':
            print 'left'
            adder -= 8
            if adder < 0:
                adder = 0
            last_pressed = "left"
        screen_cursor_positioner(adder)  # Determines Screen Number and Cursor Position
        selection_screen(self)  # Updates selection screen.
        highlighted_selection_generator(self)  # Updates cursor location on selection screen.
        clear_last_selections(self)
        if str(key_event[1]) == '13':
            print 'return'
            print "song selection number = " + str(song_selection_number)
            song_entry(song_selection_number)
            selections_screen_updater(self)
            self.my_credit_amount.text = "CREDITS " + str(credit_amount)
            '''random_generated_song_number = randint(0,len(song_list)-1)
            song_entry(random_generated_song_number)
            selections_screen_updater(self)'''
            last_pressed = "return"

    def file_reader(self, *args):
            global file_time_old
            global upcoming_list
            global start_up
            file_time_check = str(time.ctime(os.path.getmtime("output_list.txt")))  # http://bit.ly/22zKqLS

            if file_time_old != file_time_check:
                global start_up
                # screen_display()  # Updates screen based on file change.
                keyboard.press_and_release('b')  # Updates Selection Screen

                if start_up == 0:
                    keyboard.press_and_release('o')  # Updates Selection Screen
                    # time.sleep(3)
                    start_up += 1

                rss_writer()

                file_time_old = file_time_check
            else:
                print "Same"
                upcoming_list_recover = open('upcoming_list.pkl', 'rb')
                upcoming_list = pickle.load(upcoming_list_recover)
                upcoming_list_recover.close()
                # selections_screen_updater(self)

class MyFinalApp(App):

    def build(self):

        return JukeboxScreen()

def basic_random_list_generator():
    global random_list_with_year
    if not song_list:
        print "Error - No song_list in basic_random_list_generator() to develop basic random_list"
    random_list_with_year = []
    year_builder = []
    print "Building Random List"
    y = 0
    zz = len(song_list)
    z = zz - 1
    while y <= z:  # ##########code to build random_list_with_year starts here.##########
        test_string = str(song_list[y][7])
        norandom_check = "norandom"

        if re.search(r'\b' + norandom_check + r'\b', test_string):  # regex word boundaries http://bit.ly/1lSLXeP

            log_file_update = open("log.txt", "a+")  # new song_list added to log file.
            log_file_update.write(str("Song " + str(song_list[y][1]) + " " + str(song_list[y][2])
                                      + " has not been added to random_list because it's marked norandom." + '\n'))
            log_file_update.close()

            # Code below writes log entry to computers dropbox public directory for remote log access
            if os.path.exists(str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"))):
                log_file_update = open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                                      + computer_account_user_name.lower() + "log.txt", "a+")
                log_file_update.write(str("Song " + str(song_list[y][1]) + " " + str(song_list[y][2])
                                      + " has not been added to random_list because it's marked norandom." + '\n'))
                log_file_update.close()
            y += 1
        else:
            random_list.append(y)  # adds song number to random_list
            song_number = song_list[y][9]  # assigns song number from song_list to song_number variable
            song_year = song_list[y][3]  # assigns song year from song_list to song_year variable
            year_builder.append(song_number)  # appends song_number to year_builder list
            year_builder.append(song_year)  # appends song_year to year_builder list
            random_list_with_year.append(year_builder)  # appends year_builder List to random_list_with_year
            year_builder = []  # clears year_builder list
            y += 1
            #  ##########code to build random_list_with_year ends here##########
    return random_list

def brad_love():
    print "Hello, world!"
    sys.exit()

def clear_alpha_keys(event=None):
    global a_key_press
    global d_key_press
    global g_key_press
    global j_key_press
    global m_key_press
    global p_key_press
    global t_key_press
    global w_key_press
    a_key_press = 0  # Resets other multikeys to base letter..
    d_key_press = 0
    g_key_press = 0
    j_key_press = 0
    m_key_press = 0
    p_key_press = 0
    w_key_press = 0
    t_key_press = 0

def clear_button_color(self):
    self.my_first_title.background_color = (0, 0, 0, 0)
    self.my_first_artist.background_color = (0, 0, 0, 0)
    self.my_second_title.background_color = (0, 0, 0, 0)
    self.my_second_artist.background_color = (0, 0, 0, 0)
    self.my_third_title.background_color = (0, 0, 0, 0)
    self.my_third_artist.background_color = (0, 0, 0, 0)
    self.my_fourth_title.background_color = (0, 0, 0, 0)
    self.my_fourth_artist.background_color = (0, 0, 0, 0)
    self.my_fifth_title.background_color = (0, 0, 0, 0)
    self.my_fifth_artist.background_color = (0, 0, 0, 0)
    self.my_sixth_title.background_color = (0, 0, 0, 0)
    self.my_sixth_artist.background_color = (0, 0, 0, 0)
    self.my_seventh_title.background_color = (0, 0, 0, 0)
    self.my_seventh_artist.background_color = (0, 0, 0, 0)
    self.my_eigth_title.background_color = (0, 0, 0, 0)
    self.my_eigth_artist.background_color = (0, 0, 0, 0)
    self.my_ninth_title.background_color = (0, 0, 0, 0)
    self.my_ninth_artist.background_color = (0, 0, 0, 0)
    self.my_tenth_title.background_color = (0, 0, 0, 0)
    self.my_tenth_artist.background_color = (0, 0, 0, 0)
    self.my_eleventh_title.background_color = (0, 0, 0, 0)
    self.my_eleventh_artist.background_color = (0, 0, 0, 0)
    self.my_twelfth_title.background_color = (0, 0, 0, 0)
    self.my_twelfth_artist.background_color = (0, 0, 0, 0)
    self.my_thirteenth_title.background_color = (0, 0, 0, 0)
    self.my_thirteenth_artist.background_color = (0, 0, 0, 0)
    self.my_fourteenth_title.background_color = (0, 0, 0, 0)
    self.my_fourteenth_artist.background_color = (0, 0, 0, 0)
    self.my_fifteenth_title.background_color = (0, 0, 0, 0)
    self.my_fifteenth_artist.background_color = (0, 0, 0, 0)
    self.my_sixteenth_title.background_color = (0, 0, 0, 0)
    self.my_sixteenth_artist.background_color = (0, 0, 0, 0)

def clear_last_selections(self):
    if self.my_first_title.text == "zzzzz":
        self.my_first_title.font_size = 0
        self.my_first_artist.font_size = 0
    if self.my_second_title.text == "zzzzz":
        self.my_second_title.font_size = 0
        self.my_second_artist.font_size = 0
    if self.my_third_title.text == "zzzzz":
        self.my_third_title.font_size = 0
        self.my_third_artist.font_size = 0
    if self.my_fourth_title.text == "zzzzz":
        self.my_fourth_title.font_size = 0
        self.my_fourth_artist.font_size = 0
    if self.my_fifth_title.text == "zzzzz":
        self.my_fifth_title.font_size = 0
        self.my_fifth_artist.font_size = 0
    if self.my_sixth_title.text == "zzzzz":
        self.my_sixth_title.font_size = 0
        self.my_sixth_artist.font_size = 0
    if self.my_seventh_title.text == "zzzzz":
        self.my_seventh_title.font_size = 0
        self.my_seventh_artist.font_size = 0
    if self.my_eigth_title.text == "zzzzz":
        self.my_eigth_title.font_size = 0
        self.my_eigth_artist.font_size = 0
    if self.my_ninth_title.text == "zzzzz":
        self.my_ninth_title.font_size = 0
        self.my_ninth_artist.font_size = 0
    if self.my_tenth_title.text == "zzzzz":
        self.my_tenth_title.font_size = 0
        self.my_tenth_artist.font_size = 0
    if self.my_eleventh_title.text == "zzzzz":
        self.my_eleventh_title.font_size = 0
        self.my_eleventh_artist.font_size = 0
    if self.my_twelfth_title.text == "zzzzz":
        self.my_twelfth_title.font_size = 0
        self.my_twelfth_artist.font_size = 0
    if self.my_thirteenth_title.text == "zzzzz":
        self.my_thirteenth_title.font_size = 0
        self.my_thirteenth_artist.font_size = 0
    if self.my_fourteenth_title.text == "zzzzz":
        self.my_fourteenth_title.font_size = 0
        self.my_fourteenth_artist.font_size = 0
    if self.my_fifteenth_title.text == "zzzzz":
        self.my_fifteenth_title.font_size = 0
        self.my_fifteenth_artist.font_size = 0
    if self.my_sixteenth_title.text == "zzzzz":
        self.my_sixteenth_title.font_size = 0
        self.my_sixteenth_artist.font_size = 0

def count_number_mp3_songs():
    print "Entering count_number_mp3_songs()"
    global last_file_count_a
    global current_file_count
    global last_file_count
    mp3_counter = 0
    print full_path

    if sys.platform == 'win32':
        mp3_counter = len(glob.glob1(str(os.path.dirname(full_path)) + "\music", "*.mp3"))  # Number of MP3 files in library
        current_file_count = int(mp3_counter)  # provides int output for later comparison

    if sys.platform.startswith('linux'):
        #mp3_counter = len(glob.glob1(str(os.path.dirname(full_path)) + "/music", "*.mp3"))  # Number of MP3 files in library

        print "Linux MP3 Counter"
        if os.path.exists(str(os.path.dirname(full_path)) + "/music"):
            mp3_counter = len(glob.glob1(str(os.path.dirname(full_path)) + "/music", "*.mp3"))  # Number of MP3 files in library
        else:
            mp3_counter = len(glob.glob1(str(os.path.dirname(full_path)) + "/python/jukebox/music", "*.mp3"))  # Number of MP3 files in library
        current_file_count = int(mp3_counter)  # provides int output for later comparison
        print "Current Linux MP3 Count: " + str(current_file_count)
        if int(mp3_counter) == 0:
            master = Tk()
            screen_message = "Program Stopped. Please place fifty mp3's in the Convergence Jukebox music directory at " \
                         + str(os.path.dirname(full_path)) + "/music and then re-run the Convergence Jukebox software"
            msg = Message(master, text=screen_message)
            msg.config(bg='white', font=('times', 24, 'italic'))
            msg.pack()
            mainloop()
            sys.exit()

    past_mp3_file_count = open("file_count.txt", "r")  # Compares mp3 files from last run and looks for a difference
    for last_file_count_a in past_mp3_file_count:
        print "The last time the Jukebox was run there were " + str(last_file_count_a) + " files on it."
    past_mp3_file_count.close()
    last_file_count = int(last_file_count_a)  # Variable holding count of mp3 songs from last time Jukebox was run.
    print "Exiting count_number_mp3_songs()"

def credit_calculator(event=None):
    global credit_amount
    credit_amount += 1
    print credit_amount

def database_indicator():
    def song_counter_label(label):
        def count():
            global counter
            counter += 1
            label.config(text="You've added new songs. Updating your song database. Please be patient.")
            label.after(1, count)
            if counter > 7:
                song_counter.quit()

        count()
    global song_counter
    global delete_indicator
    '''song_counter = tk.Tk()
    song_counter.title("Updating Song Database")
    #label = tk.Label(song_counter, fg="black", width=130, height=200, font = "Helvetica 16 bold italic")
    label = tk.Label(song_counter, fg="black", width=130, height=200)
    label.pack()
    song_counter_label(label)
    song_counter.mainloop()'''
    print "All Done"

def flag_printer():
    print "flag_one = " + str(flag_one)
    print "flag_two = " + str(flag_two)
    print "flag_three = " + str(flag_three)
    print "flag_four = " + str(flag_four)
    print "flag_five = " + str(flag_five)
    print "flag_six = " + str(flag_six)
    print "flag_seven = " + str(flag_seven)
    print "flag_eight = " + str(flag_eight)
    print "flag_nine = " + str(flag_nine)
    print "flag_ten = " + str(flag_ten)
    print "flag_eleven = " + str(flag_eleven)
    print "flag_twelve = " + str(flag_twelve)
    print "flag_thirteen = " + str(flag_thirteen)
    print "flag_fourteen = " + str(flag_fourteen)
    print "flag_fourteen_change = " + str(flag_fourteen_change)

def genre_only_random_sorter():
    genre_search_flag = []
    flag_one_remove_list = []
    flag_two_remove_list = []
    flag_three_remove_list = []
    flag_four_remove_list = []
    flag_five_remove_list = []
    remove_list = []  # clears remove_list in advance of use
    if flag_one != "":  # Creates genre_search_flag list from various flags
        genre_search_flag.append(flag_one)
    if flag_two != "":
        genre_search_flag.append(flag_two)
    if flag_three != "":
        genre_search_flag.append(flag_three)
    if flag_four != "":
        genre_search_flag.append(flag_four)
    if flag_five != "":
        genre_search_flag.append(flag_five)
    print "Genres to be searched are: " + str(genre_search_flag)  # Print to console.
    flag_number = 1  # Used to determine name of flag_xxx_remove_list
    for j in genre_search_flag:
        counter = 0
        for i in song_list:  # List created (remove_list) to be deleted from random_list based on Genre in flag_one.
            if j in song_list[counter][7]:  # Looks for same genre selection(flag_one) in song_list
                remove_list.append(counter)  # when matched adds song number to remove_list
            counter += 1
        for i in remove_list:  # This loop uses remove_list generated above to remove ongs from random_list
            counter = 0
            if i in random_list:
                random_list.remove(i)  # Removes song numbers from random_list
            counter += 1
            if flag_number == 1:  # assigns removed song numbers to appropriate remove list
                flag_one_remove_list = remove_list
            if flag_number == 2:  # assigns removed song numbers to appropriate remove list
                flag_two_remove_list = remove_list
            if flag_number == 3:  # assigns removed song numbers to appropriate remove list
                flag_three_remove_list = remove_list
            if flag_number == 4:  # assigns removed song numbers to appropriate remove list
                flag_four_remove_list = remove_list
            if flag_number == 5:  # assigns removed song numbers to appropriate remove list
                flag_five_remove_list = remove_list
        flag_number += 1
        remove_list = []  # clears remove_list so next Genre can use it during processing
    if flag_one != "":  # Combines and creates genre_remove_list
        genre_remove_list = flag_one_remove_list + flag_two_remove_list + flag_three_remove_list \
                            + flag_four_remove_list + flag_five_remove_list
    random.shuffle(random_list)
    random.shuffle(genre_remove_list)
    counter = -1
    for i in genre_remove_list:  # this loop places the removed songs at start of random_list in random order
        counter += 1
        song_insert = genre_remove_list[counter]
        random_list.insert(0, song_insert)

def genre_year_artist_random_sort_engine():
    if flag_one == "none" and flag_six == "null" and flag_seven == "null" and flag_eight == "null" \
            and flag_nine == "null" and flag_ten == "null" and flag_eleven == "null" and flag_twelve == "null" \
            and flag_thirteen == "null":
        no_flag_random_sort()
    if flag_one != "none" and flag_six == "null" and flag_seven == "null" and flag_eight == "null" \
            and flag_nine == "null" and flag_ten == "null" and flag_eleven == "null" and flag_twelve == "null" \
            and flag_thirteen == "null":
        genre_only_random_sorter()
    if flag_one == "none" and flag_six != "null" and flag_seven != "null" and flag_eight == "null" \
            and flag_nine == "null" and flag_ten == "null" and flag_eleven == "null" and flag_twelve == "null" \
            and flag_thirteen == "null":
        multiple_year_random_sorter_no_genre()
    if flag_one == "none" and flag_six != "null" and flag_seven == "null" and flag_eight == "null" \
            and flag_nine == "null" and flag_ten == "null" and flag_eleven == "null" and flag_twelve == "null" \
            and flag_thirteen == "null":
        single_year_random_sorter_no_genre()
    if flag_one != "none" and flag_six != "null" and flag_eight == "null" and flag_nine == "null" \
            and flag_ten == "null" and flag_eleven == "null" and flag_twelve == "null" and flag_thirteen == "null":
        genre_by_year_random_sorter()
    if flag_one == "none":
        if flag_eight != "null" or flag_nine != "null" or flag_ten != "null" or flag_eleven != "null" \
                or flag_twelve != "null" or flag_thirteen != "null":
            artist_by_year_random_sorter()

def genre_read_and_select_engine():  # Opens and reads genreFlags.csv file. Assigns genres to random play functionality.

    print "Entering genre_read_and_select_engine()."

    # Convergence Jukebox Function
    # Purpose is to look up genre_flags.txt file and assigns genres to random play functionality.
    # Videos to understand functions, variables, global variables, scopes and lists at http://bit.ly/1Qx32aW

    global flag_one  # Global variables created.
    global flag_two
    global flag_three
    global flag_four
    global flag_five
    global flag_six
    global flag_seven
    global flag_eight
    global flag_nine
    global flag_ten
    global flag_eleven
    global flag_twelve
    global flag_thirteen
    global flag_fourteen
    global flag_fourteen_change

    # Code below reads genre_flags.txt from computers dropbox public directory. Allows for remote genre changes.
    if os.path.exists(str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\genre_flags.txt"))):
        genre_file_open = open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\" + "genre_flags.txt", 'r+')
        to_be_split = genre_file_open.read()
        genre_file_open.close()
    else:
        genre_file_open = open("genre_flags.txt", 'r+')
        to_be_split = genre_file_open.read()
        genre_file_open.close()
    print "genre_flags.txt file contains: ", to_be_split

    flag_file_input = to_be_split.split(",")  # Split function explained at http://www.dotnetperls.com/split-python.

    if flag_file_input[0] == "null":  # flag_one assigned.
        flag_one = "none"
    else:
        flag_one = flag_file_input[0]
    if flag_file_input[1] == "null":  # flag_two assigned.
        flag_two = ""
    else:
        flag_two = flag_file_input[1]
    if flag_file_input[2] == "null":  # flag_three assigned.
        flag_three = ""
    else:
        flag_three = flag_file_input[2]
    if flag_file_input[3] == "null":  # flag_four assigned.
        flag_four = ""
    else:
        flag_four = flag_file_input[3]
    if flag_file_input[4] == "null":  # flag_five assigned.
        flag_five = ""
    else:
        flag_five = flag_file_input[4]
    if flag_file_input[5] == "Starting Year":  # flag_six assigned.
        flag_six = "null"
    else:
        flag_six = flag_file_input[5]
    if flag_file_input[6] == "Ending Year":  # flag_seven assigned.
        flag_seven = "null"
    else:
        flag_seven = flag_file_input[6]
    if flag_file_input[7] == "Select Artists A thru C":  # flag_eight assigned.
        flag_eight = "null"
    else:
        flag_eight = flag_file_input[7]
    if flag_file_input[8] == "Select Artists D thru H":  # flag_nine assigned.
        flag_nine = "null"
    else:
        flag_nine = flag_file_input[8]
    if flag_file_input[9] == "Select Artists I Thru M":  # flag_ten assigned.
        flag_ten = "null"
    else:
        flag_ten = flag_file_input[9]
    if flag_file_input[10] == "Select Artists N Thru R":  # flag_eleven assigned.
        flag_eleven = "null"
    else:
        flag_eleven = flag_file_input[10]
    if flag_file_input[11] == "Select Artists S Thru V":  # flag_twelve assigned.
        flag_twelve = "null"
    else:
        flag_twelve = flag_file_input[11]
    if flag_file_input[12] == "Select Artists W Thru Z":  # flag_thirteen assigned.
        flag_thirteen = "null"
    else:
        flag_thirteen = flag_file_input[12]
    flag_fourteen = flag_file_input[13]  # flag_fourteen assigned.
    flag_fourteen_change = flag_fourteen  # flag_fourteen_change assigned.

def get_available_resolutions_win():  # Checks to see if device is 720p compatable for default display.

    class ScreenRes(object):  # http://bit.ly/1R6CXjF
        @classmethod
        def set(cls, width=None, height=None, depth=32):  #  Set the primary display to the specified mode
            if width and height:
                print('Setting resolution to {}x{}'.format(width, height, depth))
            else:
                print('Setting resolution to defaults')

            if sys.platform == 'win32':
                cls._win32_set(width, height, depth)
            elif sys.platform.startswith('linux'):
                cls._linux_set(width, height, depth)
            elif sys.platform.startswith('darwin'):
                cls._osx_set(width, height, depth)

        @classmethod
        def get(cls):
            if sys.platform == 'win32':
                return cls._win32_get()
            elif sys.platform.startswith('linux'):
                return cls._linux_get()
            elif sys.platform.startswith('darwin'):
                return cls._osx_get()

        @classmethod
        def get_modes(cls):
            if sys.platform == 'win32':
                return cls._win32_get_modes()
            elif sys.platform.startswith('linux'):
                return cls._linux_get_modes()
            elif sys.platform.startswith('darwin'):
                return cls._osx_get_modes()

        @staticmethod
        def _win32_get_modes():
            import win32api
            from pywintypes import DEVMODEType, error
            modes = []
            i = 0
            try:
                while True:
                    mode = win32api.EnumDisplaySettings(None, i)
                    modes.append((
                        int(mode.PelsWidth),
                        int(mode.PelsHeight),
                        int(mode.BitsPerPel),
                        ))
                    i += 1
            except error:
                pass

            return modes

        @staticmethod
        def _win32_get():
            import ctypes
            user32 = ctypes.windll.user32
            screensize = (
                user32.GetSystemMetrics(0),
                user32.GetSystemMetrics(1),
                )
            return screensize

        @staticmethod
        def _win32_set(width=None, height=None, depth=32):
            '''
            Set the primary windows display to the specified mode
            '''
            # Gave up on ctypes, the struct is really complicated

            import win32api
            from pywintypes import DEVMODEType
            if width and height:

                if not depth:
                    depth = 32

                mode = win32api.EnumDisplaySettings()
                mode.PelsWidth = width
                mode.PelsHeight = height
                mode.BitsPerPel = depth

                win32api.ChangeDisplaySettings(mode, 0)
            else:
                win32api.ChangeDisplaySettings(None, 0)

        @staticmethod
        def _win32_set_default():
            '''
            Reset the primary windows display to the default mode
            '''
            # Interesting since it doesn't depend on pywin32
            import ctypes
            user32 = ctypes.windll.user32
            # set screen size
            user32.ChangeDisplaySettingsW(None, 0)

        @staticmethod
        def _linux_set(width=None, height=None, depth=32):
            raise NotImplementedError()

        @staticmethod
        def _linux_get():
            raise NotImplementedError()

        @staticmethod
        def _linux_get_modes():
            raise NotImplementedError()

        @staticmethod
        def _osx_set(width=None, height=None, depth=32):
            raise NotImplementedError()

        @staticmethod
        def _osx_get():
            raise NotImplementedError()

        @staticmethod
        def _osx_get_modes():
            raise NotImplementedError()

    if __name__ == '__main__':
        print('Primary screen resolution: {}x{}'.format(
            *ScreenRes.get()
            ))

        if (1280, 720, 32) in (ScreenRes.get_modes()):
            print "I'm 720p compatable continuing Convergence Jukebox"
            sys.exit()
        else:
            print "I'm not 720p compatable"
            master = Tk()
            screen_message = "Program Stopped. This computer is not 1280 by 720 (720p) compatable." \
                             " 720p is the default resolution for Convergence Jukebox. This means Convergence Jukebox" \
                             " will not run on this computer. Consult www.convergencejukebox.com if you want more" \
                             " details and a potential fix to the problem."
            msg = Message(master, text=screen_message)
            msg.config(bg='white', font=('times', 24, 'italic'), justify='center')
            msg.pack()
            mainloop()
            sys.exit()

def highlighted_selection_generator(self):  # Updates cursor location on selection screen.
    global cursor_position
    global song_selection_number
    if cursor_position == 0:
        clear_button_color(self)
        if start_up != 0:
            self.my_first_title.background_color = (160, 160, 160, .2)
            self.my_first_artist.background_color = (160, 160, 160, .2)
        if self.my_first_artist.text[0:4] == "The ":
            self.my_first_artist.text = self.my_first_artist.text[4:]
        for i in range(0, len(song_list) - 1):  # Identifies song number from song_list
            if song_list[i][0] == self.my_first_title.text and song_list[i][1] == self.my_first_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 1:
        clear_button_color(self)
        self.my_second_title.background_color = (160, 160, 160, .2)
        self.my_second_artist.background_color = (160, 160, 160, .2)
        if self.my_second_artist.text[0:4] == "The ":
            self.my_second_artist.text = self.my_second_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_second_title.text and song_list[i][1] == self.my_second_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 2:
        clear_button_color(self)
        self.my_third_title.background_color = (160, 160, 160, .2)
        self.my_third_artist.background_color = (160, 160, 160, .2)
        if self.my_third_artist.text[0:4] == "The ":
            self.my_third_artist.text = self.my_third_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_third_title.text and song_list[i][1] == self.my_third_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 3:
        clear_button_color(self)
        self.my_fourth_title.background_color = (160, 160, 160, .2)
        self.my_fourth_artist.background_color = (160, 160, 160, .2)
        if self.my_fourth_artist.text[0:4] == "The ":
            self.my_fourth_artist.text = self.my_fourth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_fourth_title.text and song_list[i][1] == self.my_fourth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 4:
        clear_button_color(self)
        self.my_fifth_title.background_color = (160, 160, 160, .2)
        self.my_fifth_artist.background_color = (160, 160, 160, .2)
        if self.my_fifth_artist.text[0:4] == "The ":
            self.my_fifth_artist.text = self.my_fifth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_fifth_title.text and song_list[i][1] == self.my_fifth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 5:
        clear_button_color(self)
        self.my_sixth_title.background_color = (160, 160, 160, .2)
        self.my_sixth_artist.background_color = (160, 160, 160, .2)
        if self.my_sixth_artist.text[0:4] == "The ":
            self.my_sixth_artist.text = self.my_sixth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_sixth_title.text and song_list[i][1] == self.my_sixth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 6:
        clear_button_color(self)
        self.my_seventh_title.background_color = (160, 160, 160, .2)
        self.my_seventh_artist.background_color = (160, 160, 160, .2)
        if self.my_seventh_artist.text[0:4] == "The ":
            self.my_seventh_artist.text = self.my_seventh_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_seventh_title.text and song_list[i][1] == self.my_seventh_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 7:
        clear_button_color(self)
        self.my_eigth_title.background_color = (160, 160, 160, .2)
        self.my_eigth_artist.background_color = (160, 160, 160, .2)
        if self.my_eigth_artist.text[0:4] == "The ":
            self.my_eigth_artist.text = self.my_eigth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_eigth_title.text and song_list[i][1] == self.my_eigth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 8:
        clear_button_color(self)
        self.my_ninth_title.background_color = (160, 160, 160, .2)
        self.my_ninth_artist.background_color = (160, 160, 160, .2)
        if self.my_ninth_artist.text[0:4] == "The ":
            self.my_ninth_artist.text = self.my_ninth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_ninth_title.text and song_list[i][1] == self.my_ninth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 9:
        clear_button_color(self)
        self.my_tenth_title.background_color = (160, 160, 160, .2)
        self.my_tenth_artist.background_color = (160, 160, 160, .2)
        if self.my_tenth_artist.text[0:4] == "The ":
            self.my_tenth_artist.text = self.my_tenth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_tenth_title.text and song_list[i][1] == self.my_tenth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 10:
        clear_button_color(self)
        self.my_eleventh_title.background_color = (160, 160, 160, .2)
        self.my_eleventh_artist.background_color = (160, 160, 160, .2)
        if self.my_eleventh_artist.text[0:4] == "The ":
            self.my_eleventh_artist.text = self.my_eleventh_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_eleventh_title.text and song_list[i][1] == self.my_eleventh_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 11:
        clear_button_color(self)
        self.my_twelfth_title.background_color = (160, 160, 160, .2)
        self.my_twelfth_artist.background_color = (160, 160, 160, .2)
        if self.my_twelfth_artist.text[0:4] == "The ":
            self.my_twelfth_artist.text = self.my_twelfth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_twelfth_title.text and song_list[i][1] == self.my_twelfth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 12:
        clear_button_color(self)
        self.my_thirteenth_title.background_color = (160, 160, 160, .2)
        self.my_thirteenth_artist.background_color = (160, 160, 160, .2)
        if self.my_thirteenth_artist.text[0:4] == "The ":
            self.my_thirteenth_artist.text = self.my_thirteenth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_thirteenth_title.text and song_list[i][1] == self.my_thirteenth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 13:
        clear_button_color(self)
        self.my_fourteenth_title.background_color = (160, 160, 160, .2)
        self.my_fourteenth_artist.background_color = (160, 160, 160, .2)
        if self.my_fourteenth_artist.text[0:4] == "The ":
            self.my_fourteenth_artist.text = self.my_fourteenth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_fourteenth_title.text and song_list[i][1] == self.my_fourteenth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 14:
        clear_button_color(self)
        self.my_fifteenth_title.background_color = (160, 160, 160, .2)
        self.my_fifteenth_artist.background_color = (160, 160, 160, .2)
        if self.my_fifteenth_artist.text[0:4] == "The ":
            self.my_fifteenth_artist.text = self.my_fifteenth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_fifteenth_title.text and song_list[i][1] == self.my_fifteenth_artist.text:
                song_selection_number = song_list[i][9]
    if cursor_position == 15:
        clear_button_color(self)
        self.my_sixteenth_title.background_color = (160, 160, 160, .2)
        self.my_sixteenth_artist.background_color = (160, 160, 160, .2)
        if self.my_sixteenth_artist.text[0:4] == "The ":
            self.my_sixteenth_artist.text = self.my_sixteenth_artist.text[4:]
        for i in range(0, len(song_list) - 1):
            if song_list[i][0] == self.my_sixteenth_title.text and song_list[i][1] == self.my_sixteenth_artist.text:
                song_selection_number = song_list[i][9]

def player_launch():
    def player_launch():
        print "Hello, world!"
        if os.path.exists(str(os.path.dirname(full_path)) + "\convergenceplayer2.py"):
            print ".py directory exists at " + str(os.path.dirname(full_path)) + "\convergenceplayer2.py"
            os.system("RunConvergencePlayer2.exe")  # Launches Convergence Jukebox GUI
        else:
            os.system("RunConvergencePlayer2.exe")  # Launches Convergence Jukebox GUI

def mciSend(s):  # Function of playmp3.py
    if sys.platform == 'win32':
        winmm = windll.winmm  # Variable used in playmp3.py.
        i = winmm.mciSendStringA(s, 0, 0, 0)
        if i != 0:
            print "Error %d in mciSendString %s" % (i, s)

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def play_list_loader():
    global play_list
    play_list_recover = open('play_list.pkl', 'rb')  # Loads play_list.
    play_list = pickle.load(play_list_recover)
    play_list_recover.close()
    return play_list

def play_list_player():
    global play_list

    # This statement runs songs in play_list, deletes first song in play_list after it completes
    #  playing song and finally opens play_list to see if any new songs have appeared.
    print "Song in play_list: " + str(play_list[0])
    x = play_list[0]
    print x
    print  # x variable used below to print song data to screen
    title = str(song_list[x][0])
    artist = str(song_list[x][1])
    album = str(song_list[x][2])
    year = (song_list[x][3])
    ptime = (song_list[x][6])
    song_number = song_list[x][9]
    mode = "Mode: Playing Selected Song"
    print "Title: " + title
    print "Artist: " + artist
    print "Album: " + album
    print "Year Released: " + year + " Time: " + ptime
    output_prep = title + "," + artist + "," + album + "," + year + "," + ptime + "," + mode
    output_list_save = open("output_list.txt", "w")
    output_list_save.write(str(output_prep))
    output_list_save.close()
    time_date_stamp = datetime.datetime.now().strftime("%A. %d. %B %Y %I:%M%p")
    log_file_entry = open("log.txt", "a+")
    comma_removal = str(song_list[x][8])
    comma_free_title = comma_removal.replace(',', '')  # http://bit.ly/1SuAnRh
    log_file_entry.write(str(time_date_stamp + ',' + str(comma_free_title) + ',' + str(mode) + ',' + '1' + '\n'))
    log_file_entry.close()
    # Code below writes log entry to computers dropbox public directory for remote log access
    if os.path.exists(str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"))):
        log_file_update = open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                              + computer_account_user_name.lower() + "log.txt", "a+")
        log_file_update.write(str(time_date_stamp + ',' + str(comma_free_title) + ',' + str(mode) + ',' + '1' + '\n'))
        log_file_update.close()
    del comma_free_title
    del comma_removal
    upcoming_list_recover = open('upcoming_list.pkl', 'rb')
    upcoming_list = pickle.load(upcoming_list_recover)
    upcoming_list_recover.close()
    if len(upcoming_list) > 0:
        del upcoming_list[0]
    upcoming_list_save = open('upcoming_list.pkl', 'wb')
    pickle.dump(upcoming_list, upcoming_list_save)
    upcoming_list_save.close()

    if song_number in random_list:  # Removes paid songs from random_list. Checks for song number is in random_list.
        song_index = random_list.index(song_number)  # Index number assigned to variable. bit.ly/20FsVsl
        delete_song_index = random_list[song_index]  # Variable assigned to song number song number to be deleted.
        if song_number == delete_song_index:  # Checks if song to be deleted is still in random_list
            del random_list[song_index]  # Deletes song number from random list if found. http://bit.ly/1MRbT6I
    full_path = os.path.realpath('__file__')
    if os.path.exists(str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"))):
        log_file_update = open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                              + computer_account_user_name.lower() + "log.txt", "a+")
        log_file_update.write(str(time_date_stamp + ',' + str(song_list[x][8]) + ',' + str(mode) + ',' + '0' + '\n'))
        log_file_update.close()
    full_path = os.path.realpath('__file__')
    print "Now playing: " + str(x)
    if sys.platform == 'win32':
        playMP3(str(os.path.dirname(full_path)) + '\music' + '\\\\' + song_list[x][8])  # Plays song using mp3Play.
        # info on mp3Play at http://www.mailsend-online.com/blog/play-mp3-files-with-python-on-windows.html
    if sys.platform.startswith('linux'):
        current_path = os.getcwd()
        print current_path
        path = str(current_path) + "/music"
        os.chdir( path )# sets path for mpg321
        music = os.popen('mpg321 '+ song_list[x][8], 'w')
        music.close()
        path = current_path
        os.chdir( path )# resets path
    play_list_recover = open('play_list.pkl', 'rb')
    play_list = pickle.load(play_list_recover)
    play_list_recover.close()
    del play_list[0]
    play_list_save = open('play_list.pkl', 'wb')
    pickle.dump(play_list, play_list_save)
    play_list_save.close()
    if len(play_list) > 0:  # Checks for any paid songs to play
        play_list_player()  # Plays paid songs

def playMP3(mp3Name):  # Function of playmp3.py
    mciSend("Close All")
    mciSend("Open \"%s\" Type MPEGVideo Alias theMP3" % mp3Name)
    mciSend("Play theMP3 Wait")
    mciSend("Close theMP3")

def random_mode_playback():
    global title
    global artist
    global album
    global year
    global ptime
    global randomplay
    print "The play_list is empty. Operating in random mode."
    x = random_list[0]  # First element in random_list assigned to x variable
    print len(random_list)
    title = str(song_list[x][0])
    artist = str(song_list[x][1])
    album = str(song_list[x][2])
    year = (song_list[x][3])
    ptime = (song_list[x][6])
    randomplay = str(song_list[x][7])
    play_random_song()
    del random_list[0]
    return random_list

def play_random_song():
    global title
    global artist
    global album
    global year
    global ptime
    global randomplay
    mode = "Mode: Playing Song"
    print "Title: " + title
    print "Artist: " + artist
    print "Album: " + album
    print "Year Released: " + year + " Time: " + ptime
    output_prep = title + "," + artist + "," + album + "," + year + "," + ptime + "," + mode
    output_list_save = open("output_list.txt", "w")
    output_list_save.write(str(output_prep))
    output_list_save.close()
    time_date_stamp = datetime.datetime.now().strftime("%A. %d. %B %Y %I:%M%p")
    log_file_entry = open("log.txt", "a+")
    log_file_entry.write(str(time_date_stamp + ',' + str(song_list[x][8]) + ',' + str(mode) + ',' + '0' + '\n'))
    log_file_entry.close()
    # Code below writes log entry to computers dropbox public directory for remote log access
    if os.path.exists(str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"))):
        log_file_update = open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                              + computer_account_user_name.lower() + "log.txt", "a+")
        log_file_update.write(str(time_date_stamp + ',' + str(song_list[x][8]) + ',' + str(mode) + ',' + '0' + '\n'))
        log_file_update.close()
    full_path = os.path.realpath('__file__')
    print "Now playing: " + str(x)
    if sys.platform == 'win32':
        playMP3(str(os.path.dirname(full_path)) + '\music' + '\\\\' + song_list[x][8])  # Plays song using mp3Play.
        # info on mp3Play at http://www.mailsend-online.com/blog/play-mp3-files-with-python-on-windows.html
    if sys.platform.startswith('linux'):
        current_path = os.getcwd()
        reset_path = current_path
        path = str(current_path) + "/music"
        print path
        os.chdir( path )# sets path for mpg321
        current_path = os.getcwd()
        print current_path
        print song_list[x][8]
        print song_list[x][8]
        music = os.popen('mpg321 '+ song_list[x][8], 'w')
        music.close()
        path = reset_path
        os.chdir( path )# resets path
        print path

def resize_button_text(self):
    self.my_first_title.font_size = 16
    self.my_first_artist.font_size = 16
    self.my_second_title.font_size = 16
    self.my_second_artist.font_size = 16
    self.my_third_title.font_size = 16
    self.my_third_artist.font_size = 16
    self.my_fourth_title.font_size = 16
    self.my_fourth_artist.font_size = 16
    self.my_fifth_title.font_size = 16
    self.my_fifth_artist.font_size = 16
    self.my_sixth_title.font_size = 16
    self.my_sixth_artist.font_size = 16
    self.my_seventh_title.font_size = 16
    self.my_seventh_artist.font_size = 16
    self.my_eigth_title.font_size = 16
    self.my_eigth_artist.font_size = 16
    self.my_ninth_title.font_size = 16
    self.my_ninth_artist.font_size = 16
    self.my_tenth_title.font_size = 16
    self.my_tenth_artist.font_size = 16
    self.my_eleventh_title.font_size = 16
    self.my_eleventh_artist.font_size = 16
    self.my_twelfth_title.font_size = 16
    self.my_twelfth_artist.font_size = 16
    self.my_thirteenth_title.font_size = 16
    self.my_thirteenth_artist.font_size = 16
    self.my_fourteenth_title.font_size = 16
    self.my_fourteenth_artist.font_size = 16
    self.my_fifteenth_title.font_size = 16
    self.my_fifteenth_artist.font_size = 16
    self.my_sixteenth_title.font_size = 16
    self.my_sixteenth_artist.font_size = 16

def rss_writer():  # This function writes rss feeds to Dropbox public directory.

    global text_display_1
    global display_info
    display_info_recover = open("output_list.txt", 'r+')
    output_list_read = display_info_recover.read()
    display_info_recover.close()
    display_info = output_list_read.split(",")
    rss_song_name = display_info[0]
    rss_artist_name = display_info[1]
    rss_album_name = display_info[2]
    rss_year_info = display_info[3]
    rss_time_info = display_info[4]
    rss_mode_info = display_info[5]
    print rss_song_name
    print rss_artist_name
    rss_current_song = " . . . . . " + str(rss_song_name) + " - " + str(rss_artist_name)
    full_path = os.path.realpath('__file__')  # http://bit.ly/1RQBZYF
    if os.path.exists(str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"))):
        time_now = datetime.datetime.now()
        rss = PyRSS2Gen.RSS2(
            title="Convergence Music System RSS Feed Current Song",
            link="http://www.convergencejukebox.com",
            description="",
            lastBuildDate=datetime.datetime.now(),
            items=[
                PyRSS2Gen.RSSItem(
                    title=str(rss_current_song),
                    link="http://www.convergencejukebox.com",
                    description="Currently Playing",
                    pubDate=datetime.datetime(int(time_now.year), int(time_now.month), int(time_now.day),
                                              int(time_now.hour), int(time_now.minute))),
            ])

        rss.write_xml(open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                           + computer_account_user_name.lower() + "_current_song.xml", "w"))

        rss = PyRSS2Gen.RSS2(
            title="Convergence Music System RSS Feed Current Song",
            link="http://www.convergencejukebox.com",
            description="",
            lastBuildDate=datetime.datetime.now(),

            items=[
                PyRSS2Gen.RSSItem(
                    title=str(rss_song_name),
                    link="http://www.convergencejukebox.com",
                    description="Title Currently Playing",
                    pubDate=datetime.datetime(int(time_now.year), int(time_now.month), int(time_now.day),
                                              int(time_now.hour), int(time_now.minute))),
            ])

        rss.write_xml(open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                           + computer_account_user_name.lower() + "_title_current_song.xml", "w"))

        rss = PyRSS2Gen.RSS2(
            title="Convergence Music System RSS Feed Current Song",
            link="http://www.convergencejukebox.com",
            description="",
            lastBuildDate=datetime.datetime.now(),

            items=[
                PyRSS2Gen.RSSItem(
                    title=str(rss_artist_name),
                    link="http://www.convergencejukebox.com",
                    description="ArtistCurrently Playing",
                    pubDate=datetime.datetime(int(time_now.year), int(time_now.month), int(time_now.day),
                                              int(time_now.hour), int(time_now.minute))),
            ])

        rss.write_xml(open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                           + computer_account_user_name.lower() + "_artist_current_song.xml", "w"))

def screen_cursor_positioner(adder):  # Determines Screen Number And Cursor Position
    global cursor_position
    global screen_number
    screen_number = adder / 16
    if screen_number > 0:
        cursor_position = (adder % (screen_number * 16))
    else:
        cursor_position = adder
    return adder

def selection_font_size(self):
    self.my_selection_one.font_size = 16
    self.my_selection_two.font_size = 16
    self.my_selection_three.font_size = 16
    self.my_selection_four.font_size = 16
    self.my_selection_five.font_size = 16
    self.my_selection_six.font_size = 16
    self.my_selection_seven.font_size = 16
    self.my_selection_eight.font_size = 16
    self.my_selection_nine.font_size = 16
    self.my_selection_ten.font_size = 16
    self.my_selection_eleven.font_size = 16
    self.my_selection_twelve.font_size = 16
    self.my_selection_thirteen.font_size = 16
    self.my_selection_fourteen.font_size = 16
    self.my_selection_fifteen.font_size = 16
    self.my_selection_sixteen.font_size = 16
    self.my_selection_seventeen.font_size = 16

def selection_screen(self):  # Updates selection screen.
    global cursor_position
    global screen_number
    resize_button_text(self)
    selection_start = screen_number * 16
    if selection_start + 16 > len(song_list):
        selection_start = (screen_number * 16) - 16

    if len(str(song_list[selection_start][0])) > 36:
        if len(str(song_list[selection_start][0])) >= 48:
            self.my_first_title.font_size = 12
        elif len(str(song_list[selection_start][0])) > 44:
            self.my_first_title.font_size = 13
        else:
            self.my_first_title.font_size = 14
    if len(str(song_list[selection_start][1])) > 36:
        if len(str(song_list[selection_start][0])) >= 48:
            self.my_first_artist.font_size = 12
        elif len(str(song_list[selection_start][0])) > 44:
            self.my_first_artist.font_size = 13
        else:
            self.my_first_artist.font_size = 14
    self.my_first_title.text = str(song_list[selection_start][0])
    self.my_first_artist.text = str(song_list[selection_start][1])
    if len(str(song_list[selection_start + 1][0])) > 36:
        if len(str(song_list[selection_start + 1][0])) >= 48:
            self.my_second_title.font_size = 12
        elif len(str(song_list[selection_start + 1][0])) > 44:
            self.my_second_title.font_size = 13
        else:
            self.my_second_title.font_size = 14
    if len(str(song_list[selection_start + 1][1])) > 36:
        if len(str(song_list[selection_start + 1][0])) >= 48:
            self.my_second_artist.font_size = 12
        elif len(str(song_list[selection_start + 1][0])) > 44:
            self.my_second_artist.font_size = 13
        else:
            self.my_second_artist.font_size = 14
    self.my_second_title.text = str(song_list[selection_start + 1][0])
    self.my_second_artist.text = str(song_list[selection_start + 1][1])
    if len(str(song_list[selection_start + 2][0])) > 36:
        if len(str(song_list[selection_start + 2][0])) >= 48:
            self.my_third_title.font_size = 12
        elif len(str(song_list[selection_start + 2][0])) > 44:
            self.my_third_title.font_size = 13
        else:
            self.my_third_title.font_size = 14
    if len(str(song_list[selection_start + 2][1])) > 36:
        if len(str(song_list[selection_start + 2][0])) >= 48:
            self.my_third_artist.font_size = 12
        elif len(str(song_list[selection_start + 2][0])) > 44:
            self.my_third_artist.font_size = 13
        else:
            self.my_third_artist.font_size = 14
    self.my_third_title.text = str(song_list[selection_start + 2][0])
    self.my_third_artist.text = str(song_list[selection_start + 2][1])
    if len(str(song_list[selection_start + 3][0])) > 36:
        if len(str(song_list[selection_start + 3][0])) >= 48:
            self.my_fourth_title.font_size = 12
        elif len(str(song_list[selection_start + 3][0])) > 44:
            self.my_fourth_title.font_size = 13
        else:
            self.my_fourth_title.font_size = 14
    if len(str(song_list[selection_start + 3][1])) > 36:
        if len(str(song_list[selection_start + 3][0])) >= 48:
            self.my_fourth_artist.font_size = 12
        elif len(str(song_list[selection_start + 3][0])) > 44:
            self.my_fourth_artist.font_size = 13
        else:
            self.my_fourth_artist.font_size = 14
    self.my_fourth_title.text = str(song_list[selection_start + 3][0])
    self.my_fourth_artist.text = str(song_list[selection_start + 3][1])
    if len(str(song_list[selection_start + 4][0])) > 36:
        if len(str(song_list[selection_start + 4][0])) >= 48:
            self.my_fifth_title.font_size = 12
        elif len(str(song_list[selection_start + 4][0])) > 44:
            self.my_fifth_title.font_size = 13
        else:
            self.my_fifth_title.font_size = 14
    if len(str(song_list[selection_start + 4][1])) > 36:
        if len(str(song_list[selection_start + 4][0])) >= 48:
            self.my_fifth_artist.font_size = 12
        elif len(str(song_list[selection_start + 4][0])) > 44:
            self.my_fifth_artist.font_size = 13
        else:
            self.my_fifth_artist.font_size = 14
    self.my_fifth_title.text = str(song_list[selection_start + 4][0])
    self.my_fifth_artist.text = str(song_list[selection_start + 4][1])
    if len(str(song_list[selection_start + 5][0])) > 36:
        if len(str(song_list[selection_start + 5][0])) >= 48:
            self.my_sixth_title.font_size = 12
        elif len(str(song_list[selection_start + 5][0])) > 44:
            self.my_sixth_title.font_size = 13
        else:
            self.my_sixth_title.font_size = 14
    if len(str(song_list[selection_start + 5][1])) > 36:
        if len(str(song_list[selection_start + 5][0])) >= 48:
            self.my_sixth_artist.font_size = 12
        elif len(str(song_list[selection_start + 5][0])) > 44:
            self.my_sixth_artist.font_size = 13
        else:
            self.my_sixth_artist.font_size = 14
    self.my_sixth_title.text = str(song_list[selection_start + 5][0])
    self.my_sixth_artist.text = str(song_list[selection_start + 5][1])
    if len(str(song_list[selection_start + 6][0])) > 36:
        if len(str(song_list[selection_start + 6][0])) >= 48:
            self.my_seventh_title.font_size = 12
        elif len(str(song_list[selection_start + 6][0])) > 44:
            self.my_seventh_title.font_size = 13
        else:
            self.my_seventh_title.font_size = 14
    if len(str(song_list[selection_start + 6][1])) > 36:
        if len(str(song_list[selection_start + 6][0])) >= 48:
            self.my_seventh_artist.font_size = 12
        elif len(str(song_list[selection_start + 6][0])) > 44:
            self.my_seventh_artist.font_size = 13
        else:
            self.my_seventh_artist.font_size = 14
    self.my_seventh_title.text = str(song_list[selection_start + 6][0])
    self.my_seventh_artist.text = str(song_list[selection_start + 6][1])
    if len(str(song_list[selection_start + 7][0])) > 36:
        if len(str(song_list[selection_start + 7][0])) >= 48:
            self.my_eigth_title.font_size = 12
        elif len(str(song_list[selection_start + 7][0])) > 44:
            self.my_eigth_title.font_size = 13
        else:
            self.my_eigth_title.font_size = 14
    if len(str(song_list[selection_start + 7][1])) > 36:
        if len(str(song_list[selection_start + 7][0])) >= 48:
            self.my_eigth_artist.font_size = 12
        elif len(str(song_list[selection_start + 7][0])) > 44:
            self.my_eigth_artist.font_size = 13
        else:
            self.my_eigth_artist.font_size = 14
    self.my_eigth_title.text = str(song_list[selection_start + 7][0])
    self.my_eigth_artist.text = str(song_list[selection_start + 7][1])
    if len(str(song_list[selection_start + 8][0])) > 36:
        if len(str(song_list[selection_start + 8][0])) >= 48:
            self.my_ninth_title.font_size = 12
        elif len(str(song_list[selection_start + 8][0])) > 44:
            self.my_ninth_title.font_size = 13
        else:
            self.my_ninth_title.font_size = 14
    if len(str(song_list[selection_start + 8][1])) > 36:
        if len(str(song_list[selection_start + 8][0])) >= 48:
            self.my_ninth_artist.font_size = 12
        elif len(str(song_list[selection_start + 8][0])) > 44:
            self.my_ninth_artist.font_size = 13
        else:
            self.my_ninth_artist.font_size = 14
    self.my_ninth_title.text = str(song_list[selection_start + 8][0])
    self.my_ninth_artist.text = str(song_list[selection_start + 8][1])
    if len(str(song_list[selection_start + 9][0])) > 36:
        if len(str(song_list[selection_start + 9][0])) >= 48:
            self.my_tenth_title.font_size = 12
        elif len(str(song_list[selection_start + 9][0])) > 44:
            self.my_tenth_title.font_size = 13
        else:
            self.my_tenth_title.font_size = 14
    if len(str(song_list[selection_start + 9][1])) > 36:
        if len(str(song_list[selection_start + 9][0])) >= 48:
            self.my_tenth_artist.font_size = 12
        elif len(str(song_list[selection_start + 9][0])) > 44:
            self.my_tenth_artist.font_size = 13
        else:
            self.my_tenth_artist.font_size = 14
    self.my_tenth_title.text = str(song_list[selection_start + 9][0])
    self.my_tenth_artist.text = str(song_list[selection_start + 9][1])
    if len(str(song_list[selection_start + 10][0])) > 36:
        if len(str(song_list[selection_start + 10][0])) >= 48:
            self.my_eleventh_title.font_size = 12
        elif len(str(song_list[selection_start + 10][0])) > 44:
            self.my_eleventh_title.font_size = 13
        else:
            self.my_eleventh_title.font_size = 14
    if len(str(song_list[selection_start + 10][1])) > 36:
        if len(str(song_list[selection_start + 10][0])) >= 48:
            self.my_eleventh_artist.font_size = 12
        elif len(str(song_list[selection_start + 10][0])) > 44:
            self.my_eleventh_artist.font_size = 13
        else:
            self.my_eleventh_artist.font_size = 14
    self.my_eleventh_title.text = str(song_list[selection_start + 10][0])
    self.my_eleventh_artist.text = str(song_list[selection_start + 10][1])
    if len(str(song_list[selection_start + 11][0])) > 36:
        if len(str(song_list[selection_start + 11][0])) >= 48:
            self.my_twelfth_title.font_size = 12
        elif len(str(song_list[selection_start + 11][0])) > 44:
            self.my_twelfth_title.font_size = 13
        else:
            self.my_twelfth_title.font_size = 14
    if len(str(song_list[selection_start + 11][1])) > 36:
        if len(str(song_list[selection_start + 11][0])) >= 48:
            self.my_twelfth_artist.font_size = 12
        elif len(str(song_list[selection_start + 11][0])) > 44:
            self.my_twelfth_artist.font_size = 13
        else:
            self.my_twelfth_artist.font_size = 14
    self.my_twelfth_title.text = str(song_list[selection_start + 11][0])
    self.my_twelfth_artist.text = str(song_list[selection_start + 11][1])
    if len(str(song_list[selection_start + 12][0])) > 36:
        if len(str(song_list[selection_start + 12][0])) >= 48:
            self.my_thirteenth_title.font_size = 12
        elif len(str(song_list[selection_start + 12][0])) > 44:
            self.my_thirteenth_title.font_size = 13
        else:
            self.my_thirteenth_title.font_size = 14
    if len(str(song_list[selection_start + 12][1])) > 36:
        if len(str(song_list[selection_start + 12][0])) >= 48:
            self.my_thirteenth_artist.font_size = 12
        elif len(str(song_list[selection_start + 12][0])) > 44:
            self.my_thirteenth_artist.font_size = 13
        else:
            self.my_thirteenth_artist.font_size = 14
    self.my_thirteenth_title.text = str(song_list[selection_start + 12][0])
    self.my_thirteenth_artist.text = str(song_list[selection_start + 12][1])
    if len(str(song_list[selection_start + 13][0])) > 36:
        if len(str(song_list[selection_start + 13][0])) >= 48:
            self.my_fourteenth_title.font_size = 12
        elif len(str(song_list[selection_start + 13][0])) > 44:
            self.my_fourteenth_title.font_size = 13
        else:
            self.my_fourteenth_title.font_size = 14
    if len(str(song_list[selection_start + 13][1])) > 36:
        if len(str(song_list[selection_start + 13][0])) >= 48:
            self.my_fourteenth_artist.font_size = 12
        elif len(str(song_list[selection_start + 13][0])) > 44:
            self.my_fourteenth_artist.font_size = 13
        else:
            self.my_fourteenth_artist.font_size = 14
    self.my_fourteenth_title.text = str(song_list[selection_start + 13][0])
    self.my_fourteenth_artist.text = str(song_list[selection_start + 13][1])
    if len(str(song_list[selection_start + 14][0])) > 36:
        if len(str(song_list[selection_start + 14][0])) >= 48:
            self.my_fifteenth_title.font_size = 12
        elif len(str(song_list[selection_start + 14][0])) > 44:
            self.my_fifteenth_title.font_size = 13
        else:
            self.my_fifteenth_title.font_size = 14
    if len(str(song_list[selection_start + 14][1])) > 36:
        if len(str(song_list[selection_start + 14][0])) >= 48:
            self.my_fifteenth_artist.font_size = 12
        elif len(str(song_list[selection_start + 14][0])) > 44:
            self.my_fifteenth_artist.font_size = 13
        else:
            self.my_fifteenth_artist.font_size = 14
    self.my_fifteenth_title.text = str(song_list[selection_start + 14][0])
    self.my_fifteenth_artist.text = str(song_list[selection_start + 14][1])
    if len(str(song_list[selection_start + 15][0])) > 36:
        if len(str(song_list[selection_start + 15][0])) >= 48:
            self.my_sixteenth_title.font_size = 12
        elif len(str(song_list[selection_start + 15][0])) > 44:
            self.my_sixteenth_title.font_size = 13
        else:
            self.my_sixteenth_title.font_size = 14
    if len(str(song_list[selection_start + 15][1])) > 36:
        if len(str(song_list[selection_start + 15][0])) >= 48:
            self.my_sixteenth_artist.font_size = 12
        elif len(str(song_list[selection_start + 15][0])) > 44:
            self.my_sixteenth_artist.font_size = 13
        else:
            self.my_sixteenth_artist.font_size = 14
    self.my_sixteenth_title.text = str(song_list[selection_start + 15][0])
    self.my_sixteenth_artist.text = str(song_list[selection_start + 15][1])

    x = self.my_first_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_first_artist.text = str(x)

    x = self.my_second_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_second_artist.text = str(x)

    x = self.my_third_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_third_artist.text = str(x)

    x = self.my_fourth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_fourth_artist.text = str(x)

    x = self.my_fifth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_fifth_artist.text = str(x)

    x = self.my_sixth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_sixth_artist.text = str(x)

    x = self.my_seventh_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_seventh_artist.text = str(x)

    x = self.my_eigth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_eigth_artist.text = str(x)

    x = self.my_ninth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_ninth_artist.text = str(x)

    x = self.my_tenth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_tenth_artist.text = str(x)

    x = self.my_eleventh_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_eleventh_artist.text = str(x)

    x = self.my_twelfth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_twelfth_artist.text = str(x)

    x = self.my_thirteenth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_thirteenth_artist.text = str(x)

    x = self.my_fourteenth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_fourteenth_artist.text = str(x)

    x = self.my_fifteenth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_fifteenth_artist.text = str(x)

    x = self.my_sixteenth_artist.text
    if x.lower() in the_bands_list_lower_case:
        x = "The " + str(x)
        self.my_sixteenth_artist.text = str(x)

    clear_button_color(self)

def selections_screen_starter(self):
    global upcoming_list
    if len(upcoming_list) >= 1:
        self.my_selection_one = Label(text=str(upcoming_list[0]), pos=(40, 107))
    else:
        self.my_selection_one = Label(text=' ', pos=(40, 107))
    if len(upcoming_list) >= 2:
        self.my_selection_two = Label(text=str(upcoming_list[1]), pos=(40, 88))
    else:
        self.my_selection_two = Label(text=' ', pos=(40, 88))
    if len(upcoming_list) >= 3:
        self.my_selection_three = Label(text=str(upcoming_list[2]), pos=(40, 69))
    else:
        self.my_selection_three = Label(text=' ', pos=(40, 69))
    if len(upcoming_list) >= 4:
        self.my_selection_four = Label(text=str(upcoming_list[3]), pos=(40, 50))
    else:
        self.my_selection_four = Label(text=' ', pos=(40, 50))
    if len(upcoming_list) >= 5:
        self.my_selection_five = Label(text=str(upcoming_list[4]), pos=(40, 31))
    else:
        self.my_selection_five = Label(text=' ', pos=(40, 31))
    if len(upcoming_list) >= 6:
        self.my_selection_six = Label(text=str(upcoming_list[5]), pos=(40, 12))
    else:
        self.my_selection_six = Label(text=' ', pos=(40, 12))
    if len(upcoming_list) >= 7:
        self.my_selection_seven = Label(text=str(upcoming_list[6]), pos=(40, -7))
    else:
        self.my_selection_seven = Label(text=' ', pos=(40, -7))
    if len(upcoming_list) >= 8:
        self.my_selection_eight = Label(text=str(upcoming_list[7]), pos=(40, -26))
    else:
        self.my_selection_eight = Label(text=' ', pos=(40, -26))
    if len(upcoming_list) >= 9:
        self.my_selection_nine = Label(text=str(upcoming_list[8]), pos=(40, -47))
    else:
        self.my_selection_nine = Label(text=' ', pos=(40, -47))
    if len(upcoming_list) >= 10:
        self.my_selection_ten = Label(text=str(upcoming_list[9]), pos=(40, -66))
    else:
        self.my_selection_ten = Label(text=' ', pos=(40, -66))
    if len(upcoming_list) >= 11:
        self.my_selection_eleven = Label(text=str(upcoming_list[10]), pos=(40, -85))
    else:
        self.my_selection_eleven = Label(text=' ', pos=(40, -85))
    if len(upcoming_list) >= 12:
        self.my_selection_twelve = Label(text=str(upcoming_list[11]), pos=(40, -104))
    else:
        self.my_selection_twelve = Label(text=' ', pos=(40, -104))
    if len(upcoming_list) >= 13:
        self.my_selection_thirteen = Label(text=str(upcoming_list[12]), pos=(40, -123))
    else:
        self.my_selection_thirteen = Label(text=' ', pos=(40, -123))
    if len(upcoming_list) >= 14:
        self.my_selection_fourteen = Label(text=str(upcoming_list[13]), pos=(40, -142))
    else:
        self.my_selection_fourteen = Label(text=' ', pos=(40, -142))
    if len(upcoming_list) >= 15:
        self.my_selection_fifteen = Label(text=str(upcoming_list[14]), pos=(40, -161))
    else:
        self.my_selection_fifteen = Label(text=' ', pos=(40, -161))
    if len(upcoming_list) >= 16:
        self.my_selection_sixteen = Label(text=str(upcoming_list[15]), pos=(40, -180))
    else:
        self.my_selection_sixteen = Label(text=" ", pos=(40, -180))
    if len(upcoming_list) == 17:
        self.my_selection_seventeen = Label(text=str(upcoming_list[16]), pos=(40, -199))
    else:
        self.my_selection_seventeen = Label(text=' ', pos=(40, -199))

def selections_screen_updater(self):
    if len(upcoming_list) >= 1:
        self.my_selection_one.text = str(upcoming_list[0])
    if len(upcoming_list) >= 2:
        self.my_selection_two.text = str(upcoming_list[1])
    if len(upcoming_list) >= 3:
        self.my_selection_three.text = str(upcoming_list[2])
    if len(upcoming_list) >= 4:
        self.my_selection_four.text = str(upcoming_list[3])
    if len(upcoming_list) >= 5:
        self.my_selection_five.text = str(upcoming_list[4])
    if len(upcoming_list) >= 6:
        self.my_selection_six.text = str(upcoming_list[5])
    if len(upcoming_list) >= 7:
        self.my_selection_seven.text = str(upcoming_list[6])
    if len(upcoming_list) >= 8:
        self.my_selection_eight.text = str(upcoming_list[7])
    if len(upcoming_list) >= 9:
        self.my_selection_nine.text = str(upcoming_list[8])
    if len(upcoming_list) >= 10:
        self.my_selection_ten.text = str(upcoming_list[9])
    if len(upcoming_list) >= 11:
        self.my_selection_eleven.text = str(upcoming_list[10])
    if len(upcoming_list) >= 12:
        self.my_selection_twelve.text = str(upcoming_list[11])
    if len(upcoming_list) >= 13:
        self.my_selection_thirteen.text = str(upcoming_list[12])
    if len(upcoming_list) >= 14:
        self.my_selection_fourteen.text = str(upcoming_list[13])
    if len(upcoming_list) >= 15:
        self.my_selection_fifteen.text = str(upcoming_list[14])
    if len(upcoming_list) >= 16:
        self.my_selection_sixteen.text = str(upcoming_list[15])
    if len(upcoming_list) == 17:
        self.my_selection_seventeen.text = str(upcoming_list[16])

def set_720_resolution():

    class ScreenRes(object):  # http://bit.ly/1R6CXjF
        @classmethod
        def set(cls, width=None, height=None, depth=32):
            '''
            Set the primary display to the specified mode
            '''
            if width and height:
                print('Setting resolution to {}x{}'.format(width, height, depth))
            else:
                print('Setting resolution to defaults')

            if sys.platform == 'win32':
                cls._win32_set(width, height, depth)
            elif sys.platform.startswith('linux'):
                cls._linux_set(width, height, depth)
            elif sys.platform.startswith('darwin'):
                cls._osx_set(width, height, depth)

        @classmethod
        def get(cls):
            if sys.platform == 'win32':
                return cls._win32_get()
            elif sys.platform.startswith('linux'):
                return cls._linux_get()
            elif sys.platform.startswith('darwin'):
                return cls._osx_get()

        @classmethod
        def get_modes(cls):
            if sys.platform == 'win32':
                return cls._win32_get_modes()
            elif sys.platform.startswith('linux'):
                return cls._linux_get_modes()
            elif sys.platform.startswith('darwin'):
                return cls._osx_get_modes()

        @staticmethod
        def _win32_get_modes():  #  Get the primary windows display width and height
            import win32api
            from pywintypes import DEVMODEType, error
            modes = []
            i = 0
            try:
                while True:
                    mode = win32api.EnumDisplaySettings(None, i)
                    modes.append((
                        int(mode.PelsWidth),
                        int(mode.PelsHeight),
                        int(mode.BitsPerPel),
                        ))
                    i += 1
            except error:
                pass

            return modes

        @staticmethod
        def _win32_get():  #  Get the primary windows display width and height
            import ctypes
            user32 = ctypes.windll.user32
            screensize = (
                user32.GetSystemMetrics(0),
                user32.GetSystemMetrics(1),
                )
            return screensize

        @staticmethod
        def _win32_set(width=None, height=None, depth=32):  # Set the primary windows display to the specified mode
            # Gave up on ctypes, the struct is really complicated
            import win32api
            from pywintypes import DEVMODEType
            if width and height:

                if not depth:
                    depth = 32

                mode = win32api.EnumDisplaySettings()
                mode.PelsWidth = width
                mode.PelsHeight = height
                mode.BitsPerPel = depth

                win32api.ChangeDisplaySettings(mode, 0)
            else:
                win32api.ChangeDisplaySettings(None, 0)

        @staticmethod
        def _win32_set_default():  #  Reset the primary windows display to the default mode
            # Interesting since it doesn't depend on pywin32
            import ctypes
            user32 = ctypes.windll.user32
            # set screen size
            user32.ChangeDisplaySettingsW(None, 0)

        @staticmethod
        def _linux_set(width=None, height=None, depth=32):
            raise NotImplementedError()

        @staticmethod
        def _linux_get():
            raise NotImplementedError()

        @staticmethod
        def _linux_get_modes():
            raise NotImplementedError()

        @staticmethod
        def _osx_set(width=None, height=None, depth=32):
            raise NotImplementedError()

        @staticmethod
        def _osx_get():
            raise NotImplementedError()

        @staticmethod
        def _osx_get_modes():
            raise NotImplementedError()

    if __name__ == '__main__':
        print('Primary screen resolution: {}x{}'.format(
            *ScreenRes.get()
            ))
        # print(ScreenRes.get_modes())
        ScreenRes.set(1280, 720)
        # ScreenRes.set(1920, 1080)
        # ScreenRes.set() # Set defaults

def set_default_screen_resolution():  # Used by so_long()

    class ScreenRes(object):  # http://bit.ly/1R6CXjF
        @classmethod
        def set(cls, width=None, height=None, depth=32):
            '''
            Set the primary display to the specified mode
            '''
            if width and height:
                print('Setting resolution to {}x{}'.format(width, height, depth))
            else:
                print('Setting resolution to defaults')

            if sys.platform == 'win32':
                cls._win32_set(width, height, depth)
            elif sys.platform.startswith('linux'):
                cls._linux_set(width, height, depth)
            elif sys.platform.startswith('darwin'):
                cls._osx_set(width, height, depth)

        @classmethod
        def get(cls):
            if sys.platform == 'win32':
                return cls._win32_get()
            elif sys.platform.startswith('linux'):
                return cls._linux_get()
            elif sys.platform.startswith('darwin'):
                return cls._osx_get()

        @classmethod
        def get_modes(cls):
            if sys.platform == 'win32':
                return cls._win32_get_modes()
            elif sys.platform.startswith('linux'):
                return cls._linux_get_modes()
            elif sys.platform.startswith('darwin'):
                return cls._osx_get_modes()

        @staticmethod
        def _win32_get_modes():
            '''
            Get the primary windows display width and height
            '''
            import win32api
            from pywintypes import DEVMODEType, error
            modes = []
            i = 0
            try:
                while True:
                    mode = win32api.EnumDisplaySettings(None, i)
                    modes.append((
                        int(mode.PelsWidth),
                        int(mode.PelsHeight),
                        int(mode.BitsPerPel),
                    ))
                    i += 1
            except error:
                pass

            return modes

        @staticmethod
        def _win32_get():
            '''
            Get the primary windows display width and height
            '''
            import ctypes
            user32 = ctypes.windll.user32
            screensize = (
                user32.GetSystemMetrics(0),
                user32.GetSystemMetrics(1),
            )
            return screensize

        @staticmethod
        def _win32_set(width=None, height=None, depth=32):
            '''
            Set the primary windows display to the specified mode
            '''
            # Gave up on ctypes, the struct is really complicated
            # user32.ChangeDisplaySettingsW(None, 0)
            import win32api
            from pywintypes import DEVMODEType
            if width and height:

                if not depth:
                    depth = 32

                mode = win32api.EnumDisplaySettings()
                mode.PelsWidth = width
                mode.PelsHeight = height
                mode.BitsPerPel = depth

                win32api.ChangeDisplaySettings(mode, 0)
            else:
                win32api.ChangeDisplaySettings(None, 0)

        @staticmethod
        def _win32_set_default():
            '''
            Reset the primary windows display to the default mode
            '''
            # Interesting since it doesn't depend on pywin32
            import ctypes
            user32 = ctypes.windll.user32
            # set screen size
            user32.ChangeDisplaySettingsW(None, 0)

        @staticmethod
        def _linux_set(width=None, height=None, depth=32):
            raise NotImplementedError()

        @staticmethod
        def _linux_get():
            raise NotImplementedError()

        @staticmethod
        def _linux_get_modes():
            raise NotImplementedError()

        @staticmethod
        def _osx_set(width=None, height=None, depth=32):
            raise NotImplementedError()

        @staticmethod
        def _osx_get():
            raise NotImplementedError()

        @staticmethod
        def _osx_get_modes():
            raise NotImplementedError()

    if __name__ == '__main__':
        print('Primary screen resolution: {}x{}'.format(
            *ScreenRes.get()
        ))
        print(ScreenRes.get_modes())
        # ScreenRes.set(1280, 720)
        # ScreenRes.set(1920, 1080)
        if sys.platform.startswith('linux'):
            print "music directory exists at " + str(os.path.dirname(full_path)) + "Removing underscores to MP3 Files."
            current_path = os.getcwd()
            print current_path
            path = str(current_path) + "/music"
            os.chdir(path)  # sets path for mpg321
            [os.rename(f, f.replace('_', ' ')) for f in os.listdir('.') if not f.startswith('.')]
        ScreenRes.set()  # Set defaults

def set_up_user_files_first_time():
    global full_path
    current_directory = os.getcwd()

    if current_directory == "/home/pi":
        os.chdir("/home/pi/python/jukebox")
        #current_directory = os.getcwd()
        full_path = os.getcwd()
    else:
        full_path = os.path.realpath('__file__')  # http://bit.ly/1RQBZYF
    artist_list = []
    upcoming_list = []

    '''if sys.platform == 'win32':
        if os.path.exists(str(os.path.dirname(full_path)) + "\music"):
            print "music directory exists. Nothing to do here."
        else:
            print "music directory does not exist."
            os.makedirs(str(os.path.dirname(full_path)) + "\music")
            master = Tk()
            screen_message = "Program Stopped. Please place fifty mp3's in the Convergence Jukebox music directory at " \
                         + str(os.path.dirname(full_path)) + "\music and then re-run the Convergence Jukebox software"
            msg = Message(master, text=screen_message)
            msg.config(bg='white', font=('times', 24, 'italic'), justify='center')
            msg.pack()
            mainloop()

    if sys.platform.startswith('linux'):
        if os.path.exists(str(os.path.dirname(full_path)) + "/music"):
            print "music directory exists. Nothing to do here."
        else:
            print "music directory does not exist."
            os.makedirs(str(os.path.dirname(full_path)) + "/music")
            master = Tk()
            screen_message = "Program Stopped. Please place fifty mp3's in the Convergence Jukebox music directory at " \
                         + str(os.path.dirname(full_path)) + "/music and then re-run the Convergence Jukebox software"
            msg = Message(master, text=screen_message)
            msg.config(bg='white', font=('times', 24, 'italic'), justify='center')
            msg.pack()
            mainloop()'''

    if os.path.exists("log.txt"):
        print "log.txt exists. Nothing to do here."
    else:
        log_file = file("log.txt", "w")
        log_file.close()
        print "log.txt created."

    if os.path.exists("genre_flags.txt"):
        print "genre_flags.txt exists. Nothing to do here."
    else:
        genre_file = file("genre_flags.txt", "w")
        genre_file.write("null,null,null,null,null,Starting Year,Ending Year,Select Artists A thru C,"
                         + "Select Artists D thru H,Select Artists I Thru M,Select Artists N Thru R,"
                         + "Select Artists S Thru V,Select Artists W Thru Z,"
                         + "Wednesday December 16 2015 12:44:11 PM")
        genre_file.close()
        print "genre_flags.txt created."

    if os.path.exists("file_count.txt"):
        print "file_count.txt exists. Nothing to do here."
    else:
        old_file_count = file("file_count.txt", "w")
        old_file_count.write("0")
        old_file_count.close()
        print "file_count.txt created."

    if os.path.exists("song_list.pkl"):
        print "song_list.pkl exists. Nothing to do here."
    else:
        song_list_file_create = file("song_list.pkl", "wb")
        song_list_file_create.close()
        print "song_list.pkl created."

    if os.path.exists("output_list.txt"):
        print "output_list.txt exists. Nothing to do here."
    else:
        output_list_file_create = file("output_list.txt", "w")
        output_list_file_create.write("Convergence Jukebox,Brad Fortner,www.convergencejukebox.com,2012,2016,GNU General Public License V3")
        output_list_file_create.close()
        print "output_list.txt created."

    if os.path.exists("play_list.pkl"):
        print "play_list.pkl exists. Nothing to do here."
    else:
        play_list_file_create = open('play_list.pkl', 'wb')
        pickle.dump(play_list, play_list_file_create)
        play_list_file_create.close()
        print "play_list.pkl created."

    if os.path.exists("upcoming_list.pkl"):
        print "upcoming_list.pkl exists. Nothing to do here."
    else:
        upcoming_list_file_create = open('upcoming_list.pkl', 'wb')
        pickle.dump(upcoming_list, upcoming_list_file_create)
        upcoming_list_file_create.close()
        print "upcoming_list.pkl created."

    if os.path.exists("artist_list.pkl"):
        print "artist_list.pkl exists. Nothing to do here."
    else:
        artist_list_file_create = open('artist_list.pkl', 'wb')
        pickle.dump(artist_list, artist_list_file_create)
        artist_list_file_create.close()
        print "artist_list.pkl created."

def song_entry(song_number):  # Writes selected song to playlist.
    global credit_amount
    global upcoming_list
    if credit_amount == 0:
        playMP3('buzz.mp3')
        return
    play_list_recover = open('play_list.pkl', 'rb')
    play_list = pickle.load(play_list_recover)
    play_list_recover.close()
    new_entry = song_number
    print new_entry
    if new_entry in play_list:  # Checks if song number is in play_list to avoid duplicates. http://bit.ly/2pTlkLS
        a = play_list.index(song_number)  # Locates song number in play_list. Index number assigned to variable.
        b = play_list[a]  # b variable assigned song number at play_list index provided in above line.
        if song_number == b:
            return
    x = 0
    while x < len(song_list):  # Saves all upcoming song titles and artist to upcoming_list for side display.
        if song_list[x][9] == new_entry:
            print song_list[x][0]
            upcoming_song = str(song_list[x][0]) + " - " + str(song_list[x][1])
            upcoming_list_recover = open('upcoming_list.pkl', 'rb')
            upcoming_list = pickle.load(upcoming_list_recover)
            upcoming_list_recover.close()
            upcoming_list.append(upcoming_song)
            upcoming_list_save = open('upcoming_list.pkl', 'wb')
            pickle.dump(upcoming_list, upcoming_list_save)
            upcoming_list_save.close()
        x += 1
    play_list.append(new_entry)
    play_list_save = open('play_list.pkl', 'wb')
    pickle.dump(play_list, play_list_save)
    play_list_save.close()
    credit_amount -= 1
    playMP3('success.mp3')

def so_long(event=None):  # Used to terminate program.

    if sys.platform == 'win32':
        set_default_screen_resolution()
        if os.path.exists(str(os.path.dirname(full_path)) + "\convergenceplayer.py"):
            os.system("player_quit_py.exe")  # Launches Convergence Jukebox Player
            jukebox_display.destroy()
        else:
            os.system("taskkill /im convergenceplayer.exe")
            jukebox_display.destroy()

    if sys.platform.startswith('linux'):
        sys.exit()

def song_list_generator():
    global song_list
    global file_name_with_error
    delete_indicator = ""
    #bad_file_name = ""
    print "Entering song_list_generator()"

    if last_file_count == current_file_count:  # If matched the song_list is loaded from file
        print "Jukebox music files same as last startup. Using existing song database."  # Message to console.
        song_list_recover = open('song_list.pkl', 'rb')  # Loads song_list
        song_list_open = pickle.load(song_list_recover)
        song_list_recover.close()
        song_list = song_list_open
    else:  # New song_list, filecount and location_list generated and saved.
        song_list_generate = []
        build_list = []
        location_list = []
        time_date_stamp = datetime.datetime.now().strftime("%A. %d. %B %Y %I:%M%p")  # Timestamp generate bit.ly/1MKPl5x
        log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
        log_file_entry.write(str(time_date_stamp + ',' + 'New song_list generated' + ',' + '\n'))
        log_file_entry.close()
        # Code below writes log entry to computers dropbox public directory for remote log access
        if os.path.exists(str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"))):
            log_file_update = open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                                  + computer_account_user_name.lower() + "log.txt", "a+")
            log_file_update.write(str(time_date_stamp + ',' + 'New song_list generated' + ',' + '\n'))
            log_file_update.close()
        file_count_update = open("file_count.txt", "w+")  # Writes new filecount to filecount.txt file for next start.
        s = str(current_file_count)
        file_count_update.write(s)
        file_count_update.close()
        location_list = []  # Creates temporary location_list used for initial song file names for mp3 player.
        # File names later inserted in song_list to be used to play mp3's
        full_path = os.path.realpath('__file__')
        if sys.platform == 'win32':
            for name in os.listdir(str(os.path.dirname(full_path)) + "\music" + "\\"):  # Reads files in the music dir.
                if name.endswith(".mp3"):  # If statement searching for files with mp3 designation
                    title = name  # Name of mp3 transferred to title variable
                    location_list.append(title)  # Name of song appended to location_list
        if sys.platform.startswith('linux'):
            for name in os.listdir(str(os.path.dirname(full_path)) + "/music"):  # Reads files in the music dir.
                if name.endswith(".mp3"):  # If statement searching for files with mp3 designation
                    title = name  # Name of mp3 transferred to title variable
                    location_list.append(title)  # Name of song appended to location_list
        x = 0  # hsaudiotag 1.1.1 code begins here to pull out ID3 information
        while x < len(location_list):  # Python List len function http://docs.python.org/2/library/functions.html#len
            if sys.platform == 'win32':
                myfile = auto.File(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x] + "")
            if sys.platform.startswith('linux'):
                myfile = auto.File(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x] + "")
            # Note "" Quotes Required in above string.
            # hsaudiotag function that assigns mp3 song to myfile object
            print "Building Song Database. Stand By. This can take some time"
            albumorg = myfile.album  # Assigns above mp3 ID3 Album name to albumorg variable
            yearorg = myfile.year  # Assigns above mp3 ID3 Year info to yearorg variable
            durationorgseconds = myfile.duration  # Assigns mp3 Duration (in seconds) info to durationorgseconds var.
            genreorg = myfile.genre  # Assigns above mp3 Genre info to genreorg variable
            commentorg = myfile.comment  # Assigns above mp3 Comment info to commentorg variable
            build_list.append(myfile.title)  # Title of song appended to build_list
            try:  # http://www.pythonlovers.net/python-exceptions-handling
                unicode_crash_test = str(myfile.title)  # Causes crash if Unicode found in Artist Name
            except UnicodeEncodeError:
                print str(location_list[x])
                #bad_file_name = str(location_list[x])
                file_name_with_error = str(location_list[x])
                log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                log_file_entry.write(str(file_name_with_error + ' was deleted because of a Unicode character in its ID3 Title data.' + '\n'))
                log_file_entry.close()
                print "Title Unicode Error"
                if sys.platform == 'win32':
                    print "Removing " + str(location_list[x])
                    os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                if sys.platform.startswith('linux'):
                    os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                delete_indicator = "yes"
                if location_list[x] in build_list:
                    print "We need to delete " + str(location_list[x]) + " here Unicode title."
            try:  # http://www.pythonlovers.net/python-exceptions-handling
                unicode_crash_test = str(myfile.artist)  # Causes crash if Unicode found in Artist Name
            except UnicodeEncodeError:
                print str(location_list[x])
                #bad_file_name = str(location_list[x])
                file_name_with_error = str(location_list[x])
                log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                log_file_entry.write(str(file_name_with_error + ' was deleted because of a Unicode character in its ID3 Artist data.' + '\n'))
                log_file_entry.close()
                print "Artist Unicode Error"
                if sys.platform == 'win32':
                    print "Removing " + str(location_list[x])
                    os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                if sys.platform.startswith('linux'):
                    os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                delete_indicator = "yes"
                if location_list[x] in build_list:
                    print "We need to delete " + str(location_list[x]) + " here Unicode title."
            try:  # http://www.pythonlovers.net/python-exceptions-handling
                unicode_crash_test = str(myfile.comment)  # Causes crash if Unicode found in Artist Name
            except UnicodeEncodeError:
                print str(location_list[x])
                #bad_file_name = str(location_list[x])
                file_name_with_error = str(location_list[x])
                log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                log_file_entry.write(str(file_name_with_error + ' was deleted because of a Unicode character in its ID3 Comment data.' + '\n'))
                log_file_entry.close()
                print "Comment Unicode Error"
                if sys.platform == 'win32':
                    print "Removing " + str(location_list[x])
                    os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                if sys.platform.startswith('linux'):
                    os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                delete_indicator = "yes"
                if location_list[x] in build_list:
                    print "We need to delete " + str(location_list[x]) + " here Unicode title."
            if myfile.artist == "":  # Check for invalid Artist mp3 ID tag
                print str(location_list[x])
                #bad_file_name = str(location_list[x])
                file_name_with_error = str(location_list[x])
                print str(location_list[x]) + "'s Artist ID3 tag is not valid for Convergence Jukebox. Please correct or remove from media folder."
                log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                log_file_entry.write(str(file_name_with_error + ' was deleted because its ID3 Artist data is not valid.' + '\n'))
                log_file_entry.close()
                if sys.platform == 'win32':
                    print "Removing " + str(location_list[x])
                    os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                if sys.platform.startswith('linux'):
                    os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                delete_indicator = "yes"
                if location_list[x] in build_list:
                    print "We need to delete " + str(location_list[x]) + " here Unicode title."
            if myfile.title == "":  # Check for invalid mp3 Title ID tag
                print str(location_list[x])
                #bad_file_name = str(location_list[x])
                file_name_with_error = str(location_list[x])
                print str(location_list[x]) + "'s Title ID3 tag is not valid for Convergence Jukebox. Please correct or remove from media folder."
                log_file_entry = open("log.txt", "a+")  # new song_list added to log file.
                log_file_entry.write(str(file_name_with_error + ' was deleted because its ID3 Title data is not valid.' + '\n'))
                log_file_entry.close()
                if sys.platform == 'win32':
                    print "Removing " + str(location_list[x])
                    os.remove(str(os.path.dirname(full_path)) + "\music" + "\\" + location_list[x])
                if sys.platform.startswith('linux'):
                    os.remove(str(os.path.dirname(full_path)) + "/music" + "/" + location_list[x])
                delete_indicator = "yes"
                if location_list[x] in build_list:
                    print "We need to delete " + str(location_list[x]) + " here Unicode title."
            if x == 0:
                database_indicator()
            if delete_indicator == "yes":
                file_count_update = open("file_count.txt", "w+")  # Writes new filecount to filecount.txt file for next start.
                s = str(0)
                file_count_update.write(s)
                file_count_update.close()
            if delete_indicator != "yes":
                build_list.append(myfile.artist)  # Artist of song appended to build_list
                build_list.append(myfile.album)  # Album title of song appended to build_list
                build_list.append(myfile.year)  # Year of song appended to build_list
                build_list.append(myfile.duration)  # Duration of song in seconds appended to build_list
                build_list.append(myfile.genre)  # Genre of song appended to build_list
                durationtimefull = str(datetime.timedelta(seconds=durationorgseconds))  # Info at http://bit.ly/1L5pU9t
                durationtime = durationtimefull[3:7]  # Slices string to minute:second notation. http://bit.ly/1QphhOW
                build_list.append(durationtime)  # Time of song in minutes/seconds of song appended to build_list
                build_list.append(myfile.comment)  # Comment in ID3 data appended to build_list
                full_file_name = str(location_list[x])
                if sys.platform.startswith('linux'):
                    title_with_whitespace = full_file_name
                    title_without_whitespace = title_with_whitespace.replace(" ", "_")
                    full_file_name = title_without_whitespace
                    current_path = os.getcwd()
                    temp_path = str(current_path)+'/music'
                    os.chdir(temp_path)  # resets path
                    os.rename(str(title_with_whitespace), str(title_without_whitespace))
                    os.chdir(current_path)# resets path
                build_list.append(full_file_name)
                song_list_generate.append(build_list)
                build_list.append(x)
                print location_list[x]
                print build_list[8]
                print build_list
                build_list = []
                y = len(location_list) - x
                # print "www.convergencejukebox.com Building your database " + str(full_file_name) + ". " + str(y) + \
                # " files remaining to process."
            delete_indicator = ""
            print x
            x += 1
        song_list_save = open('song_list.pkl', 'wb')  # song_list saved as binary pickle file
        pickle.dump(song_list_generate, song_list_save)
        song_list_save.close()
        song_list = song_list_generate
    print "Exiting song_list_generator()"
    return song_list

def write_jukebox_startup_to_log():
    time_date_stamp = datetime.datetime.now().strftime("%A. %d. %B %Y %I:%M%p")  # time_date_stamp. bit.ly/1MKPl5x
    log_file_entry = open("log.txt", "a+")
    log_file_entry.write(str(time_date_stamp + ',' + 'Jukebox Started For Day' + ',' + '\n'))
    log_file_entry.close()

    # Code below writes log entry to computers dropbox public directory for remote log access
    if os.path.exists(str(os.path.dirname("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"))):
        log_file_entry = open("c:\\users\\" + computer_account_user_name + "\\Dropbox\\public\\"
                              + computer_account_user_name.lower() + "log.txt", "a+")
        log_file_entry.write(str(time_date_stamp + ',' + 'Jukebox Started For Day' + ',' + '\n'))
        log_file_entry.close()

if __name__ == "__main__":
    MyFinalApp().run()
