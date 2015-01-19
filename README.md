# Puush indicator

Simple appindicator for GTK that emulates the puush's client functionality.

## Requirements

* Python 2.7
* Appindicator module
* PyGTK

## Usage

Store your API key in the PUUSH_API_KEY environment variable.


Then run puush_indicator.py

## Options

You can let puush_indicator only upload a single file for you by giving the file name as the only argument.
Example: `./puush_indicator.py ~/myfile.png`
