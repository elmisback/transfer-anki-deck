# -*- coding: utf-8 -*-
#############################################################################
# 
# -Made by Zack Boyd for:
#       Goal Oriented Academics LLC <goalorientedacademics@gmail.com>
# -GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# 
#############################################################################

import os
from aqt        import mw, profiles, exporting, importing
from aqt.qt     import *
from aqt.utils  import showInfo, showWarning
from anki.exporting import *

#main function
def transferTo():
    #starting
    mw.progress.start(immediate=True)

    #Set up the Anki Package Exporter Object
    exp = AnkiPackageExporter(mw.col)
    exp.includeSched = False
    exp.includeMedia = True
    exp.includeTags  = True
    exp.did          = mw.col.decks.selected()

    #Where the temporary file is going
    path = os.path.join(mw.pm.profileFolder())
    filename = os.path.join(path, 'temp.apkg')

    #Do the exporting and be careful(catch file errors)
    try:
        f = open(filename, "wb")
        f.close()
    except (OSError, IOError), e:
        showWarning(_("Couldn't make temp file: %s") % unicode(e))
        mw.progress.finish()
        return
    else:
        os.unlink(filename)
        exp.exportInto(filename)
    
    #done with exporting
    mw.progress.finish()
    #get the deck name before we sign out
    name = mw.col.decks.name(mw.col.decks.selected())

    #get user to login to the user receiving the deck
    mw.unloadProfile(browser=False)
    showInfo("Login as the User you wish to Transfer Deck <i>{0}</i> to.".format(name))
    mw.showProfileManager() 
    mw.loadProfile()

    #starting
    mw.progress.start(immediate=True) 

    #import and delete the temp.apkg
    importing.importFile(mw, filename)
    os.unlink(filename)

    #done
    mw.progress.finish()
    return

transferDeck = QAction("Transfer Deck", mw)
mw.connect(transferDeck, SIGNAL("triggered()"), transferTo)
mw.form.menuTools.addAction(transferDeck)
