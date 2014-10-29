#!/usr/bin/env python

from threading import Thread
from time import sleep
import subprocess
import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import os
import sys

class PuushIndicator:
    key=None
    def __init__(self):
        self.key = os.getenv("PUUSH_API_KEY")
        if self.key is None:
            print("Missing API key")
            exit(1)

        self.ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon ("indicator-messages-new")
        self.ind.set_icon_theme_path(os.path.dirname(os.path.realpath(__file__)))
        self.ind.set_icon("icon")

        self.menu = gtk.Menu()

        myAccount = gtk.MenuItem("My account")
        myAccount.connect("activate", self.showAccount)
        myAccount.show()
        self.menu.append(myAccount)

        separator = gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)

        itemDesktop = gtk.MenuItem("Capture desktop")
        itemDesktop.connect("activate", self.uploadDesktopScreenshot)
        itemDesktop.show()
        self.menu.append(itemDesktop)

        itemArea = gtk.MenuItem("Capture area")
        itemArea.connect("activate", self.captureArea)
        itemArea.show()
        self.menu.append(itemArea)

        item = gtk.MenuItem("Upload file")
        item.connect("activate", self.upload)
        item.show()
        self.menu.append(item)

        separator = gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)

        image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        image.connect("activate", self.quit)
        image.show()
        self.menu.append(image)
                    
        self.menu.show()
        self.ind.set_menu(self.menu)

    def notify(self, msg):
            subprocess.Popen(['notify-send', "Puush", msg]) 
        
    def puush(self,filepath,delete=False):
            subprocess.call(["bash", "puush.sh", filepath ], stdout=open("curlout", "w"))
            status = None

            with open("curlout", "r") as file:
                status = file.read().split(',')

            code = status[0]
        
            if int(code) != 0:
                notify("The upload failed!")
                return

            url = status[1]
            self.notify("File uploaded! %s" % url)
            subprocess.Popen(["xdg-open", url]) 
            if delete:
                os.system("rm %s" % filepath)
            os.system("rm %s" % "curlout")

    def captureArea(self, widget, data=None):
        subprocess.call(["scrot", "-s", "screenshot.png"]) 
        self.puush("screenshot.png", delete=True)

    def showAccount(self, widget, data=None):
        subprocess.call(["xdg-open", "http://puush.me/login/go/?k=%s" % str(self.key) ])

    def upload(self, widget, data=None):
        filename = ""

        dialog=gtk.FileChooserDialog(title="Select a File to puush", action=gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        response = dialog.run()
                
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            return

        dialog.destroy() 
        self.puush(filename)

    def quit(self, widget, data=None):
        gtk.main_quit()

    def uploadDesktopScreenshot(self, widget, data=None):
        w = gtk.gdk.get_default_root_window()
        sz = w.get_size()
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        if (pb != None):
            pb.save("screenshot.png","png")
        else:
            return
        self.puush("screenshot.png",delete=True)

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    indicator = PuushIndicator()
    main()
