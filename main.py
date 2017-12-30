# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

import os
import re
import time

from main_ui import Ui_Dialog


# email
def is_valid_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    else:
        return True


def delete_photos(days):
    now = time.time()
    cutoff = now - (days * 86400)

    files = os.listdir("images")
    for xfile in files:
        if os.path.isfile("images/" + xfile):
            t = os.stat("images/" + xfile)
            c = t.st_ctime

            # delete file if older than a the number of days
            if c < cutoff:
                os.remove("images/" + xfile)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)

    widget = QtGui.QWidget()
    ex = Ui_Dialog()
    ex.setupUi(widget)

    # add subwindows
    ex.mdiArea.addSubWindow(ex.subwindowCamera)
    ex.mdiArea.addSubWindow(ex.subwindowOptions)

    widget.show()

    valid_settings = False
    from configobj import ConfigObj
    config = ConfigObj('config.ini')
    user_email = config['DEFAULT']['email']
    user_password = config['DEFAULT']['password']
    resolution = config['DEFAULT']['resolution']
    email_minutes = config['DEFAULT']['email-minutes']
    photos_days = config['DEFAULT']['photos-days']

    # resolution dropdown
    resolution_options = [
        '640x512',
        '1280x1024'
    ]
    ex.comboResolution.clear()
    ex.comboResolution.addItems(resolution_options)
    index = ex.comboResolution.findText(resolution, QtCore.Qt.MatchFixedString)
    if index >= 0:
        ex.comboResolution.setCurrentIndex(index)
    else:
        resolution = resolution_options[0]

    # emails days range
    if email_minutes.isdigit():
        minutes = int(email_minutes)
        ex.lineMinutesEmails.setText(email_minutes)
    else:
        minutes = 5
        ex.lineMinutesEmails.setText('5')

    # delete older photos
    if photos_days.isdigit():
        days = int(photos_days)
        if days > 0:
            delete_photos(days)
        ex.lineDaysPhotos.setText(photos_days)
    else:
        days = 5
        ex.lineDaysPhotos.setText('5')

    if user_email != '' and user_password != '' and is_valid_email(user_email):
        ex.lineEmail.setText(user_email)
        ex.linePassword.setText(user_password)
        valid_settings = True
        ex.user_email = user_email
        ex.user_password = user_password
        ex.resolution = resolution
        ex.email_minutes = minutes

    if valid_settings:
        ex.status = 'identified'
        ex.labelStatus.setText('Status: identified')
        ex.buttonCamera.setEnabled(True)
        ex.buttonSurveillance.setEnabled(False)
        ex.mdiArea.setActiveSubWindow(
            ex.mdiArea.subWindowList()[0])

    sys.exit(app.exec_())
