#!/usr/bin/env python

import appindicator, gtk, os, requests, subprocess

key = None
indicator = None
menu = None

def init_indicator():
        global indicator, menu
        indicator = appindicator.Indicator('Puush', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
        indicator.set_status(appindicator.STATUS_ACTIVE)
        indicator.set_attention_icon('indicator-messages-new')
        indicator.set_icon_theme_path(os.path.dirname(os.path.realpath(__file__)))
        indicator.set_icon('icon')

        menu = gtk.Menu()

        item_account = gtk.MenuItem('My account')
        item_account.connect('activate', show_account)
        item_account.show()
        menu.append(item_account)

        separator = gtk.SeparatorMenuItem()
        separator.show()
        menu.append(separator)

        item_capture_area = gtk.MenuItem('Capture Area')
        item_capture_area.connect('activate', capture_area)
        item_capture_area.show()
        menu.append(item_capture_area)

        item_upload = gtk.MenuItem('Upload')
        item_upload.connect('activate', upload)
        item_upload.show()
        menu.append(item_upload)

        item_desktop_screenshot = gtk.MenuItem('Desktop Screenshot')
        item_desktop_screenshot.connect('activate', desktop_screenshot)
        item_desktop_screenshot.show()
        menu.append(item_desktop_screenshot)

        item_upload_clipboard = gtk.MenuItem('Upload Clipboard')
        item_upload_clipboard.connect('activate', upload_clipboard)
        item_upload_clipboard.show()
        menu.append(item_upload_clipboard)


        separator = gtk.SeparatorMenuItem()
        separator.show()
        menu.append(separator)

        item_quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        item_quit.connect('activate', quit)
        item_quit.show()
        menu.append(item_quit)

        menu.show()
        indicator.set_menu(menu)

def desktop_screenshot(indicator):
        window = gtk.gdk.get_default_root_window()
        size = window.get_size()
        pixelBuffer = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, size[0], size[1])
        pixelBuffer = pixelBuffer.get_from_drawable(window, window.get_colormap(), 0, 0, 0, 0, size[0], size[1])
        if pixelBuffer is not None:
            pixelBuffer.save("/tmp/puush_screenshot.png", "png")
        else:
            notify('Could not take screenshot!')
            return

        puush('/tmp/puush_screenshot.png')
        os.remove('/tmp/puush_screenshot.png')

def upload_clipboard(indicator):
        clip = subprocess.Popen(["xclip", "-selection", "clipboard", "-o"], stdout=subprocess.PIPE).communicate()[0]
        # If the contained clip data is a link to a file, puush that
        if os.path.isfile(clip):
            puush(clip)
        # Else write the clip data to a file and then puush it
        else:
            with open("/tmp/puush_clip", "w") as file:
                file.write(clip)
            puush("/tmp/puush_clip")
            os.remove('/tmp/puush_clip')


def capture_area(indicator):
        subprocess.call(['scrot', '-s', '/tmp/puush_screenshot.png']) 
        puush('/tmp/puush_screenshot.png')
        os.remove('/tmp/puush_screenshot.png')

def upload(self):
        dialog = gtk.FileChooserDialog(title='Select a file to puush', action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        response = dialog.run()

        if response == gtk.RESPONSE_OK:
                filename = dialog.get_filename()
        else:
                return

        dialog.destroy()
        puush(filename)

def notify(message):
        subprocess.Popen(['notify-send', 'Puush', message])

def show_account(indicator):
        global key
        subprocess.call(["xdg-open", "http://puush.me/login/go/?k=%s" % str(key) ])

def quit(indicator):
        gtk.main_quit()

def puush(filepath):
        global key
        data = {'z': 'poop', 'k': key}
        files = {'f': open(filepath, 'rb')}
        r = requests.post('http://puush.me/api/up', data=data, files=files)
        response = r.text.split(',')
        statusCode = int(response[0])

        if statusCode != 0:
                notify('The upload failed!')
                return
        
        notify('Puushed! %s' % response[1])
        subprocess.Popen(['xdg-open', response[1]])

def main():
        global key
        key = os.getenv('PUUSH_API_KEY')

        if key is None:
                print('Missing the API key!')
                return

        init_indicator()
        gtk.main() 

if __name__ == "__main__":
        main()
