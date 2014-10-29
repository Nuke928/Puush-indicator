# Puush indicator

Simple appindicator for GTK that uses puush.

## Requirements

* Python 2.7
* Appindicator module
* PyGTK

## Usage

Run puush_indicator.py


You need to set your puush API key in PUUSH_API_KEY.
Preferably add this to your .bashrc:
> export PUUSH_API_KEY=maikey

## Todo

The upload functions need to run in a seperate thread.
Somehow though subprocess.call blocks the thread until the other thread is finished?
