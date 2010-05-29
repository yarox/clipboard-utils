# playword.py

import gtk
import urllib
import json



LANG_FROM = "en" 
LANG_TO   = "es"


def translate(text_from, lang_from, lang_to):
    user_ip   = "http://www.my-ajax-site.com"
    version   = "1.0"

    text_to   = "ERROR"
    lang_pair = "|".join([lang_from, lang_to])
    base_url  = "http://ajax.googleapis.com/ajax/services/language/translate?"

    params   = urllib.urlencode({'v':version, 'q': text_from,
                             'langpair': lang_pair, 'userip':
                             user_ip})  
    response = urllib.urlopen(base_url + "%s" % params)
    response = response.read()
    data     = json.loads(response)

    if data["responseStatus"] == 200:
        text_to = data["responseData"]["translatedText"]

    return text_to

      
def clipboard_changed(clipboard, event):
    text_from = clipboard.wait_for_text()
    text_to   = translate(text_from, LANG_FROM, LANG_TO)

    print text_to


clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
clip.connect("owner-change", clipboard_changed)

gtk.main()
