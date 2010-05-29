# playword.py

import gtk


def _clipboard_changed(clipboard, event):
    text = clipboard.wait_for_text()
    print text

clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
clip.connect("owner-change", _clipboard_changed)

gtk.main()
