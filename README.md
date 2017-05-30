# Convergence-Jukebox-Experimental

This project contains developing code to be integrated into the Convergence Jukebox project.

* For the most part this code should be working.
* I'm currently merging convergencejukebox.py (from the original Convergence Jukebox) with convergencegui.py and convergenceplayer.py (from Convergence Jukebox 2) into one file.
* The merged file is named convergencejukebox2.py
UPDATE
* Turns out that two files may be needed after all.
* Kivy does not like python loops executing. The GUI freezes.
* Windows mp3 player player employed in this software will not release Kivy GUI while playing mp3.
* Currently paring down player code to try running as a Python subprocess to get around problem.

Some notes:

* See Convergence Jukebox 2 in this repository for more information on this program.