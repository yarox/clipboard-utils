# playword.py

import gtk
import glib
import urllib
import json



LANG_FROM = "en" 
LANG_TO   = "es"


def translate(text_from, lang_from, lang_to):
    """Returns the text translation, using the translation API from
    Google."""
    base_url = "http://ajax.googleapis.com/ajax/services/"
    service = "language/translate?"
    user_ip = "http://www.my-ajax-site.com"
    version = "1.0"

    text_to = "ERROR"
    lang_pair = "|".join([lang_from, lang_to])

    params = urllib.urlencode({'v':version,
                               'q': text_from,
                               'langpair': lang_pair,
                               'userip': user_ip})
    
    response = urllib.urlopen(base_url + service + "%s" % params) 
    response = response.read()
    data = json.loads(response)

    if data["responseStatus"] == 200:
        text_to = data["responseData"]["translatedText"]

    return text_to


def display(text):
    """Creates a window for displaying some text."""

    # Init the window and link it with a signal handler
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("show", pop_window)

    # Get the cursor position
    root = window.get_screen().get_root_window()
    x, y, mods = root.get_pointer()

    # Create the label and set some parameters
    label = gtk.Label(text)
    label.set_line_wrap(True)
    label.set_max_width_chars(50)
    label.connect("size-allocate", size_label)
    window.add(label)

    # Create the window and set some parameters
    window.set_decorated(False)
    window.set_border_width(5)
    window.set_opacity(0.85)
    window.move(x, y)

    window.show_all()


# Callback functions used by gtk and friends
def clipboard_changed(clipboard, event):
    """Gets called when the clipboard is updated with new content."""
    text_from = clipboard.wait_for_text()
    text_to   = translate(text_from, LANG_FROM, LANG_TO)

    display(text_to)


def pop_window(widget, data=None):
    """Gets called when a new window is shown, in order to make it
    disappear within some seconds."""
    glib.timeout_add(3000, widget.hide)
    return True


def size_label(label, allocation):
    """Gets called when a label needs to know its size. It'll make the
    parent window the same size as the label."""
    label.set_size_request(allocation.width, -1)


# Initzialize the clipboard
clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
clip.connect("owner-change", clipboard_changed)

# GTK main loop
gtk.main()
