# Puush indicator

Simple appindicator for GTK that uses puush.

## Requirements

* Python 2.7
* Appindicator module
* PyGTK

## Usage

Add your puush API key in ~/.puush.rc in one line.


Run puush_indicator.py

## Todo

The upload functions need to run in a seperate thread.
Somehow though subprocess.call blocks the thread until the other thread is finished?
