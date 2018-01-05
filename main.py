# -*- coding: utf-8 -*-

# Standard libraries stuff
import os
import re
import smtplib
import time
from datetime import datetime
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Third party stuff
import cv2
import numpy as np
from PyQt4 import QtCore, QtGui

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# Application stuff
from main_ui import Ui_Dialog


DEFAULT_THRESHOLD = 32


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


def get_frames_difference(frame, prev_frame):
    frame_diff = cv2.absdiff(frame, prev_frame)
    gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
    thrs = DEFAULT_THRESHOLD
    ret, motion_mask = cv2.threshold(gray_diff, thrs, 1, cv2.THRESH_BINARY)
    difference = np.sum(motion_mask)
    return difference


# class to capture the video
class VideoCapture(QtGui.QWidget):
    def __init__(self, parent):
        super(QtGui.QWidget, self).__init__()
        self.parent = parent
        self.cap = cv2.VideoCapture(0)
        self.resolution = '640x512'
        if self.resolution == '1280x1024':
            self.cap.set(3, 1280)
            self.cap.set(4, 1024)
        else:
            self.cap.set(3, 640)
            self.cap.set(4, 512)
        self.video_frame = QtGui.QLabel()
        self.prev_frame = None
        self.triggered_frame = 0
        parent.layout.addWidget(self.video_frame)

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0],
                           QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

        if self.parent.parent.status == 'watching':
            # check difference between current and previous frame
            difference = get_frames_difference(frame, self.prev_frame)
            if difference > 1000:  # Adjust value accoring to camera resolution
                self.triggered_frame += 1
                """
                Check if the difference is longer than 15 frames to preven
                incorrect detections
                """
                if self.triggered_frame > 15:
                    self.triggered_frame = 0
                    print('Motion detected!')
            else:
                self.triggered_frame = 0

        self.prev_frame = frame

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000.0/30)

    def pause(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(QtGui.QWidget, self).deleteLater()


class VideoDisplayWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(VideoDisplayWidget, self).__init__()
        self.parent = parent
        self.layout = QtGui.QFormLayout(self)
        self.setLayout(self.layout)


class App(Ui_Dialog):
    def __init__(self):
        super(App, self).__init__()
        self.capture = None

    def camera(self):
        if self.status == 'ready' or self.status == 'watching':
            self.status = 'identified'
            self.buttonCamera.setText(_translate("Dialog", "Activate Camera",
                                                 None))
            self.buttonSurveillance.setText('Start surveillance')
            self.labelStatus.setText('Status: identified')
            self.buttonSurveillance.setEnabled(False)
            self.capture.pause()
        else:
            if self.status == 'identified':
                self.status = 'ready'
                self.buttonCamera.setText(_translate(
                    "Dialog", "Deactivate Camera", None))
                self.buttonSurveillance.setEnabled(True)
                if not self.capture:
                    self.capture = VideoCapture(self.videoDisplayWidget)
                self.capture.start()
            else:
                self.status = 'unidentified'
                self.labelStatus.setText('Status: credentials error')
                self.buttonCamera.setEnabled(False)

    def save_photo(self, frame):
        # save image
        current_datetime = datetime.now()
        filename = str(current_datetime).replace(' ', '_').replace(
            ':', '.') + '.jpg'
        filepath = 'images/'+filename
        cv2.imwrite(filepath, frame)

        # append to query
        self.images.append(filepath)

    def send_email(self):
        try:
            sender = self.user_email
            gmail_password = self.user_password
            recipients = [sender]

            outer = MIMEMultipart()
            outer['Subject'] = Header('New motion detected.', 'utf-8')
            outer['From'] = sender
            outer['To'] = sender

            for file in self.images[:5]:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment',
                               filename=os.path.basename(file))
                outer.attach(msg)

            html = '<p>Dummy test message</p>'
            part2 = MIMEText(html, 'html', 'utf-8')

            outer.attach(part2)

            composed = outer.as_string()

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
            return 'email sent'
        except:
            return None

    def surveillance(self):
        if self.status == 'watching':
            self.status = 'ready'
            self.labelStatus.setText('Status: ready')
            self.buttonSurveillance.setText('Start Surveillance')
        else:
            self.status = 'watching'
            self.labelStatus.setText('Status: watching')
            self.buttonSurveillance.setText('Stop Surveillance')

    def applyChanges(self):
        user_email = str(self.lineEmail.text())
        user_password = str(self.linePassword.text())
        resolution = str(self.comboResolution.currentText())
        email_minutes = str(self.lineMinutesEmails.text())
        photos_days = str(self.lineDaysPhotos.text())

        from configobj import ConfigObj
        config = ConfigObj()
        config.filename = 'config.ini'

        config['DEFAULT'] = {}
        config['DEFAULT']['email'] = user_email
        # config['DEFAULT']['password'] = EncodeAES(cipher, user_password)
        # config['DEFAULT']['password'] = user_password
        config['DEFAULT']['resolution'] = resolution
        config['DEFAULT']['email-minutes'] = email_minutes
        config['DEFAULT']['photos-days'] = photos_days

        config.write()

        # check data
        if user_email != '' and user_password != '' and \
           is_valid_email(user_email) and email_minutes.isdigit() and \
           photos_days.isdigit():
            # send email
            self.user_email = user_email
            self.user_password = user_password
            self.email_minutes = int(email_minutes)
            self.resolution = resolution

            # delete older photos
            days = int(photos_days)
            if days > 0:
                delete_photos(days)

        else:
            # invalid data
            self.status = 'unidentified'
            self.labelStatus.setText(_translate("Dialog",
                                                "Status: invalid data", None))
            self.buttonCamera.setEnabled(False)
            self.buttonSurveillance.setEnabled(False)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)

    widget = QtGui.QWidget()
    ex = App()
    ex.setupUi(widget)

    # add subwindows
    ex.mdiArea.addSubWindow(ex.subwindowCamera)
    ex.mdiArea.addSubWindow(ex.subwindowOptions)

    ex.buttonCamera.clicked.connect(ex.camera)
    ex.buttonSurveillance.clicked.connect(ex.surveillance)
    ex.buttonApply.clicked.connect(ex.applyChanges)

    ex.videoDisplayWidget = VideoDisplayWidget(ex)
    ex.horizontalLayoutCamera.addWidget(ex.videoDisplayWidget)

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
