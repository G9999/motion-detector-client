# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Wed Feb 18 01:07:02 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

# options
# import configparser
import re
import os
import time
from Crypto.Cipher import AES
import base64
BLOCK_SIZE = 32
PADDING = '{'
DEFAULT_SECRET = 'qwertyuiopasdfgh'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
cipher = AES.new(DEFAULT_SECRET)

# email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
# from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

# camera
import cv2
import numpy as np
from datetime import datetime
DEFAULT_THRESHOLD = 32

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Dialog(QtGui.QWidget):
    status = 'unidentified'
    driver = None
    user_email = None
    user_password = None
    resolution = None
    email_minutes = None
    images = []
    close_camera_window = False

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(349, 632)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelStatus = QtGui.QLabel(Dialog)
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        self.verticalLayout.addWidget(self.labelStatus)
        self.label = QtGui.QLabel(Dialog)
        self.label.setText(_fromUtf8(""))
        # self.label.setPixmap(QtGui.QPixmap(_fromUtf8("logo.bmp")))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.mdiArea = QtGui.QMdiArea(Dialog)
        self.mdiArea.setActivationOrder(QtGui.QMdiArea.CreationOrder)
        self.mdiArea.setViewMode(QtGui.QMdiArea.TabbedView)
        self.mdiArea.setTabShape(QtGui.QTabWidget.Rounded)
        self.mdiArea.setObjectName(_fromUtf8("mdiArea"))
        self.subwindowCamera = QtGui.QWidget()
        self.subwindowCamera.setObjectName(_fromUtf8("subwindowCamera"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.subwindowCamera)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.buttonCamera = QtGui.QPushButton(self.subwindowCamera)
        self.buttonCamera.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonCamera.sizePolicy().hasHeightForWidth())
        self.buttonCamera.setSizePolicy(sizePolicy)
        self.buttonCamera.setObjectName(_fromUtf8("buttonCamera"))
        self.verticalLayout_2.addWidget(self.buttonCamera)
        self.buttonSurveillance = QtGui.QPushButton(self.subwindowCamera)
        self.buttonSurveillance.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSurveillance.sizePolicy().hasHeightForWidth())
        self.buttonSurveillance.setSizePolicy(sizePolicy)
        self.buttonSurveillance.setObjectName(_fromUtf8("buttonSurveillance"))
        self.verticalLayout_2.addWidget(self.buttonSurveillance)
        self.subwindowOptions = QtGui.QWidget()
        self.subwindowOptions.setObjectName(_fromUtf8("subwindowOptions"))
        self.layoutWidget = QtGui.QWidget(self.subwindowOptions)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 312, 206))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEmail = QtGui.QLineEdit(self.layoutWidget)
        self.lineEmail.setObjectName(_fromUtf8("lineEmail"))
        self.horizontalLayout.addWidget(self.lineEmail)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelPassword = QtGui.QLabel(self.layoutWidget)
        self.labelPassword.setObjectName(_fromUtf8("labelPassword"))
        self.horizontalLayout_2.addWidget(self.labelPassword)
        self.linePassword = QtGui.QLineEdit(self.layoutWidget)
        self.linePassword.setEchoMode(QtGui.QLineEdit.Password)
        self.linePassword.setObjectName(_fromUtf8("linePassword"))
        self.horizontalLayout_2.addWidget(self.linePassword)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelResolution = QtGui.QLabel(self.layoutWidget)
        self.labelResolution.setObjectName(_fromUtf8("labelResolution"))
        self.horizontalLayout_3.addWidget(self.labelResolution)
        self.comboResolution = QtGui.QComboBox(self.layoutWidget)
        self.comboResolution.setObjectName(_fromUtf8("comboResolution"))
        self.horizontalLayout_3.addWidget(self.comboResolution)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelMinutesEmails = QtGui.QLabel(self.layoutWidget)
        self.labelMinutesEmails.setObjectName(_fromUtf8("labelMinutesEmails"))
        self.horizontalLayout_4.addWidget(self.labelMinutesEmails)
        self.lineMinutesEmails = QtGui.QLineEdit(self.layoutWidget)
        self.lineMinutesEmails.setObjectName(_fromUtf8("lineMinutesEmails"))
        self.horizontalLayout_4.addWidget(self.lineMinutesEmails)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelDaysPhotos = QtGui.QLabel(self.layoutWidget)
        self.labelDaysPhotos.setObjectName(_fromUtf8("labelDaysPhotos"))
        self.horizontalLayout_5.addWidget(self.labelDaysPhotos)
        self.lineDaysPhotos = QtGui.QLineEdit(self.layoutWidget)
        self.lineDaysPhotos.setObjectName(_fromUtf8("lineDaysPhotos"))
        self.horizontalLayout_5.addWidget(self.lineDaysPhotos)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem = QtGui.QSpacerItem(168, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.buttonApply = QtGui.QPushButton(self.layoutWidget)
        self.buttonApply.setObjectName(_fromUtf8("buttonApply"))
        self.horizontalLayout_6.addWidget(self.buttonApply)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addWidget(self.mdiArea)

        self.mdiArea.addSubWindow(self.subwindowCamera)
        self.mdiArea.addSubWindow(self.subwindowOptions)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Detector - Sistema de Vigilancia", None))
        self.labelStatus.setText(_translate("Dialog", "Estado: no identificado", None))
        self.subwindowCamera.setWindowTitle(_translate("Dialog", "Cámara", None))
        self.buttonCamera.setText(_translate("Dialog", "Activar Cámara", None))
        self.buttonSurveillance.setText(_translate("Dialog", "Comenzar Vigilancia", None))
        self.subwindowOptions.setWindowTitle(_translate("Dialog", "Opciones", None))
        self.label_2.setText(_translate("Dialog", "Correo Gmail:", None))
        self.labelPassword.setText(_translate("Dialog", "Contraseña:", None))
        self.labelResolution.setText(_translate("Dialog", "Resolución de fotos:", None))
        self.labelMinutesEmails.setText(_translate("Dialog", "Rango de minutos entre emails:", None))
        self.labelDaysPhotos.setText(_translate("Dialog", "Conservar fotos de los últimos días:", None))
        self.buttonApply.setText(_translate("Dialog", "Aplicar cambios", None))

        self.buttonCamera.clicked.connect(self.camera)
        self.buttonSurveillance.clicked.connect(self.surveillance)
        self.buttonApply.clicked.connect(self.applyChanges)

    def camera(self):
        if self.status == 'ready' or self.status == 'watching':
            self.status = 'identified'
            self.buttonCamera.setText(_translate("Dialog", "Activar Cámara", None))
            self.buttonSurveillance.setText('Iniciar Vigilancia')
            self.labelStatus.setText('Estado: Identificado!')
            self.buttonSurveillance.setEnabled(False)
            self.close_camera_window = True
        else:
            if self.status == 'identified':
                self.status = 'ready'
                self.buttonCamera.setText(_translate("Dialog", "Desactivar Cámara", None))
                self.buttonSurveillance.setEnabled(True)
                self.open_camera()
            else:
                self.status = 'unidentified'
                self.labelStatus.setText('Estado: Error al identificarse')
                self.buttonCamera.setEnabled(False)

    def open_camera(self):
        # initialize camera
        email_sent = False
        click = False

        def mouse(event, x, y, flag, param):
            global click
            if event == cv2.cv.CV_EVENT_LBUTTONUP:
                click = True

        capture = cv2.VideoCapture(0)
        print self.resolution
        if self.resolution == '1280x1024':
            capture.set(3, 1280)
            capture.set(4, 1024)
        else:
            capture.set(3, 640)
            capture.set(4, 512)

        cv2.namedWindow('Camera')
        cv2.setMouseCallback('Camera', mouse)

        success, frame = capture.read()
        prev_frame = frame.copy()

        last_email_time = None
        triggered_frame = 0
        self.close_camera_window = False
        while success and cv2.waitKey(1) == -1 and not click and not self.close_camera_window:
            ret, frame = capture.read()
            frame_diff = cv2.absdiff(frame, prev_frame)
            gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
            thrs = DEFAULT_THRESHOLD
            ret, motion_mask = cv2.threshold(gray_diff, thrs, 1, cv2.THRESH_BINARY)
            difference = np.sum(motion_mask)

            if difference > 1000:
                triggered_frame += 1
                if triggered_frame > 15:
                    triggered_frame = 0
                    if self.status == 'watching':
                        self.save_photo(frame)
                        if not email_sent:
                            resp = self.send_email()
                            if resp == 'email sent':
                                email_sent = True
                                self.images = []
                                last_email_time = datetime.now()
                        else:
                            current_datetime = datetime.now()
                            delta = current_datetime - last_email_time
                            if delta.total_seconds() >= (self.email_minutes * 60):
                                resp = self.send_email()
                                self.images = []
                                last_email_time = datetime.now()

            cv2.imshow('Camera', frame)
            prev_frame = frame.copy()

        cv2.destroyWindow('Camera')

        self.status = 'identified'
        self.buttonCamera.setText(_translate("Dialog", "Activar Cámara", None))
        self.buttonSurveillance.setText('Iniciar Vigilancia')
        self.labelStatus.setText('Estado: Identificado!')
        self.buttonSurveillance.setEnabled(False)

    def save_photo(self, frame):
        # save image
        current_datetime = datetime.now()
        filename = str(current_datetime).replace(' ', '_').replace(':', '.') + '.jpg'
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
            outer['Subject'] = Header('Detector – Información de Incidente detectado.', 'utf-8')
            outer['From'] = sender
            outer['To'] = sender

            for file in self.images[:5]:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)

            # text = "Nuevos eventos de movimiento txt"
            # part1 = MIMEText(text, 'plain')

            html = '''<p>Sr(a) ciudadano(a),</p>
                    <p>Se le informa que la aplicación “VIGILANTE CIUDADANO” detectó movimientos irregulares en su domicilio, se le recomienda tomar las precauciones necesarias llamando a vecinos cercanos o comunicándose con las estaciones policiales integrales que cuenta el Municipio de La Paz detallado a continuación:</p>
                    <p>
                        <table>
                            <thead>
                                <tr><th>EPI / Módulo Policial / Unidad Polcial  / Municipio</th><th>UBICACIÓN</th><th>TELÉFONO</th></tr>
                            </thead>
                            <tbody>
                                <tr><td>EPI Bosquecillo</td><td>Av. Naciones Unidas s/n (curva de Pura Pura), zona Pura Pura.</td><td>800140039</td></tr>
                                <tr><td>E.P.I. Chasquipampa</td><td>Calle 51, lado Centro de Salud, zona Chasquipampa</td><td>800140070</td></tr>
                                <tr><td>E.P.I. Cotahuma</td><td>Calle Zudañez  y Caupolicán s/n,  Tembladerani</td><td>800142222</td></tr>
                                <tr><td>E.P.I. Ferroviario</td><td>Av. Periférica  s/n (calle Cupilupaca) zona Barrio Ferroviario</td><td>800140097</td></tr>
                                <tr><td>E.P.I. La Merced</td><td>Av. Palos Blancos s/n ,zona La Merced.</td><td>800140050</td></tr>
                                <tr><td>E.P.I. La Portada</td><td>Plaza Sergio Almaráz (ex Centro de Salud, al lado de la Iglesia), zona La Portada</td><td>800140083</td></tr>
                                <tr><td>E.P.I. San Antonio</td><td></td><td>800140290</td></tr>
                                <tr><td>E.P.I. Maximiliano Paredes (Munaypata)</td><td>Av. Naciones Unidas s/n,(curva de Munaypata), zona Munaypata</td><td>800140035</td></tr>
                                <tr><td>E.P.I. San Pedro – Radio Patrulla 110</td><td>Calle Colombia s/n zona San Pedro</td><td>800140095</td></tr>
                                <tr><td>M.P. 18 de mayo</td><td>Av. 18 de Mayo s/n, (altura parada 149 y micro T), zona Viviendas 18 de Mayo (Vino Tinto)</td><td>800140045</td></tr>
                                <tr><td>M.P. 27 de Mayo, Bajo Tejar (Modulo Policial Nº 11)</td><td>Plaza 27 de Mayo entre Santos Prada y Bustillos, zona Bajo Tejar.</td><td>800140034</td></tr>
                                <tr><td>M.P. 8 de Diciembre</td><td>Calle Río Jinchupalla s/n, zona Jinchupalla</td><td>800140019</td></tr>
                                <tr><td>M.P. Achachicala (Piedra Vieja)</td><td>Av. Ramos Gavilán s/n, zona Achachicala</td><td>800140041</td></tr>
                                <tr><td>M.P. Alonso de Mendoza</td><td>Plaza Alonso de Mendoza s/n, entre calle Bozo y Condeuyo, zona San Sebastián.</td><td>800140089</td></tr>
                                <tr><td>M.P. Alto Las Delicias</td><td>Av. Periférica s/n (Av. Juan José  Torrez), cerca Cancha las Delicias, zona Alto las Delicias</td><td>800140052</td></tr>
                                <tr><td>M.P. Alto Mcal. Sta Cruz</td><td>Av. Segundo Bascones esq. Apumallita, zona Alto Mariscal Santa Cruz</td><td>800140038</td></tr>
                                <tr><td>M.P. Alto Olimpic.</td><td></td><td>800140022</td></tr>
                                <tr><td>M.P. Alto Seguencoma 1ra Meseta</td><td>Calle 3 s/n esq. Av del  Policia zona Alto Seguencoma 1ra Meseta</td><td>800140077</td></tr>
                                <tr><td>M.P. Alto Villa Copacabana, (Ex Río Viscachani)</td><td>Av. Imperial s/n (final), zona Viscachani</td><td>800140062</td></tr>
                                <tr><td>M.P. Apumalla (Modulo Policial Nº 9)</td><td>Av. Apumalla s/n (cerca gradas de pasarela), zona  Callampalla</td><td>800140031</td></tr>
                                <tr><td>M.P. Arandia.</td><td>Plaza Arandia s/n, Villa Fatima.</td><td>800140054</td></tr>
                                <tr><td>M.P. Armando Escobar Uría</td><td>Calle 9 esq. Calle F s/n, zona Armando Escobar Uría</td><td>800140065</td></tr>
                                <tr><td>M.P. Av. del Poeta</td><td>Av. del Poeta s/n (a 100 metros de la Gruta de la Virgen), zona Soqueri.</td><td>800702020</td></tr>
                                <tr><td>M.P. Bajo Achumani.</td><td>Av. García Lanza s/n, esq. Calle 8, Plaza Escalante, zona Achumani</td><td>800140082</td></tr>
                                <tr><td>M.P. Bajo Las Delicias</td><td>Av. Las Delicias esq. Av. San Buenaventura s/n zona Las Delicias (Chapuma).</td><td>800140053</td></tr>
                                <tr><td>M.P. Bajo Seguencoma</td><td>Av. Victor  Zapana y Hugo Ernst s/n, zona Bajo Seguencoma</td><td>800140078</td></tr>
                                <tr><td>M.P. Barrio lindo</td><td>Av. 5 de Agosto  s/n (final), cancha polifuncional, zona Barrio Lindo.</td><td>800140026</td></tr>
                                <tr><td>M.P. Barrio Minero</td><td>Parque Domitila Chungara s/n, zona Barrio Minero</td><td>800140064</td></tr>
                                <tr><td>M.P. Barrio Municipal Bella Vista</td><td>Calle 4 s/n, zona Barrio Municipal</td><td>800140079</td></tr>
                                <tr><td>M.P. Bello Horizonte</td><td>Calle Canonigo Ayllón s/n, zona Bello Horizonte Bajo</td><td>800140037</td></tr>
                                <tr><td>M.P. Ben Hur (Policía Comunitaria)</td><td>Calle Antonio Quijarro y Nardín Rivas s/n, zona 14  de Septiembre</td><td>800140040</td></tr>
                                <tr><td>M.P. Bolognia, P.A.C.</td><td>Calle 5 s/n, zona Irpavi (pasando Puente de la Calle 5)</td><td>800140075</td></tr>
                                <tr><td>M.P. Cabo Juán</td><td>Gradas entre Calle Juan Bárbaro y Rene Barrientos s/n, zona Vino Tinto</td><td>800140043</td></tr>
                                <tr><td>M.P. Caja de Agua</td><td>Calle Humahuaca s/n esq. Calle Iriarte (parque Iruya), zona Norte Caja de Agua</td><td>800140036</td></tr>
                                <tr><td>M.P. Capitan Ustariz</td><td>Calle Capitán Victor Ustariz s/n esq. Calle Estensoro, zona Villa Pabón</td><td>800140048</td></tr>
                                <tr><td>M.P. Chacaltaya (ex Viscachani)</td><td>Av. Periférica s/n Cancha Maracaná, zona Challapampa.</td><td>800140047</td></tr>
                                <tr><td>M.P. Entre Rios (Modulo Policial Nº 12)</td><td>Av. Entre Ríos s/n, Zona Mariscal Santa Cruz</td><td>800140024</td></tr>
                                <tr><td>M.P. German Bush</td><td>Av. Baltazar de Salas s/n (frente al Hospital Germán Busch), zona Vino Tinto</td><td>800140046</td></tr>
                                <tr><td>M.P. Guindales</td><td>Calle José Gutierrez s/n (Final), zona Miraflores Centro</td><td>800140094</td></tr>
                                <tr><td>M.P. Guitarrani</td><td>Av. Periférica s/n  (al lado de Pro Salud), zona Alto 27 de Mayo.</td><td>800140051</td></tr>
                                <tr><td>M.P. Hinojosa.</td><td>Mercado Hinojosa, Av, Buenos Aires esq. Alcoreza.</td><td>800140069</td></tr>
                                <tr><td>M.P. Illimani</td><td>Calle 5 s/n, esq. Av. Los Sargentos (Centro de Salud), zona Illimani (Bajo Llojeta )</td><td>800140229</td></tr>
                                <tr><td>M.P. Inka Llojeta</td><td>Av. Los Sargentos s/n, zona Alto Inka Llojeta</td><td>800140015</td></tr>
                                <tr><td>M.P. Juan XXIII</td><td>Calle Linares,  Pasaje Artesanal Juan XXIII, zona San Pedro</td><td>800140021</td></tr>
                                <tr><td>M.P. Juancito Pinto</td><td>Calle Jimenez s/n (entre Calle Cardozo y Graneros), zona El Rosario</td><td>800140096</td></tr>
                                <tr><td>M.P. Kantutani</td><td>Calle Romecín Campos s/n, zona Kantutani</td><td>800140073</td></tr>
                                <tr><td>M.P. Killi Killi (Mirador de Killi Killi)</td><td>Mirador de Killi Killi s/n, Av. La Bandera, zona San Juan.</td><td>800140049</td></tr>
                                <tr><td>M.P. Kilometro 7  Pasankeri</td><td>Calle Kilometro 7  s/n (al lado de la cancha de futsal), zona Pasankeri</td><td>800140016</td></tr>
                                <tr><td>M.P. Koani</td><td>Av. Muñoz Reyes s/n, zona Koani</td><td>800140067</td></tr>
                                <tr><td>M.P. Las Nieves (Alto Cotahuma)</td><td>Calle Moxos s/n (detrás de la cancha de Futbol Las Nieves), San Juan Cotahuma</td><td>800140012</td></tr>
                                <tr><td>M.P. Litoral</td><td>Av. la Florida esq. Calle 0 s/n, zona Mallasa (al lado de la cancha Litoral)</td><td>800140084</td></tr>
                                <tr><td>M.P. Los Andes  (Módulo Policial Nº  8)</td><td>Calle Diez de Medina s/n, casi esq. Manuel Cossio, zona Los Andes</td><td>800140030</td></tr>
                                <tr><td>M.P. Luis Uría de la Oliva</td><td>Av. Vicente Burgaleta esq. Costanera s/n (al frente del Hospital Luis Uría)</td><td>800140059</td></tr>
                                <tr><td>M.P. Mallasilla</td><td>Av. Valle de la Luna s/n (frente a la cancha Mallasilla), zona Mallasilla</td><td>800140074</td></tr>
                                <tr><td>M.P. Mariano Colodro</td><td>Av. Mariano Colodro y Río Abuná, zona Koa Koa</td><td>800140027</td></tr>
                                <tr><td>M.P. Max Paredes (Sub Alcaldía)</td><td>Calle Max Paredes s/n (Sub Alcaldía Max Paredes)</td><td>800140023</td></tr>
                                <tr><td>M.P. Montículo.</td><td>Calle A. Muñoz s/n, Sopocachi.</td><td>800142226</td></tr>
                                <tr><td>M.P. Niño Kollo</td><td>Av. Pablo zárate s/n, zona Niño Kollo</td><td>800140013</td></tr>
                                <tr><td>M.P. Obispo Indaburo (Parque Niño Jesus)</td><td>Calle Obispo Balderrama s/n, zona Obispo Indaburo</td><td>800140033</td></tr>
                                <tr><td>M.P. Padre Eterno, z Villa San Antonio (Cementerio Judio)</td><td>Calle Bailón Mercado esq Calle Rengel s/n (a una cuadra del cementerio Judio) zona Padre Eterno.</td><td>800140063</td></tr>
                                <tr><td>M.P. Pampahasi Alto,  Sector Guardia (sede vecinal)</td><td>Calle K s/n al lado de la Capilla Santiago, zona Pampahasi Alto</td><td>800140058</td></tr>
                                <tr><td>M.P. Pampahasi Bajo (Cancha Venus)</td><td>Calle 7 s/n esq. Calle 10 (Cancha Venus, Casa Comunal Pampahasi Bajo)</td><td>800140056</td></tr>
                                <tr><td>M.P. Pampahasi Central (SAMAPA)</td><td>Av. Circunvalación esq. Av. Ciudad del Niño s/n (SAMAPA), Zona Pampahasi Central  sector Cervecería</td><td>800140057</td></tr>
                                <tr><td>M.P. Peña Azul, zona Alto Irpavi</td><td>Av. Muñoz Reyes s/n (final), zona Alto Irpavi (parada Minibus 200)</td><td>800140068</td></tr>
                                <tr><td>M.P. Pichincha</td><td>Calle Pichincha s/n entre calle Ingavi y Comercio, zona Casco Viejo</td><td>800140087</td></tr>
                                <tr><td>M.P. Plaza Abel Alarcón</td><td>Plaza Abél Alarcón s/n, entre Luis Lara y Rigoberto Paredes, zona Alto San Pedro</td><td>800140017</td></tr>
                                <tr><td>M.P. Plaza Avaroa</td><td>Plaza Avaroa (casi esq. Belisario Salinas y 20 de Octubre) Sopocachi</td><td>800142223</td></tr>
                                <tr><td>M.P. Puente Colonial</td><td>Av. Periférica s/n (sobre Puente Colonial), zona 3 de Mayo</td><td>800140055</td></tr>
                                <tr><td>M.P. Pura Pura (Av Vasquez)</td><td>Av. Vasquez s/n, zona Pura Pura Said (sector pescaderas)</td><td>800140028</td></tr>
                                <tr><td>M.P. Pura Pura (Final Vasquez)</td><td>Av. Vasquez s/n (final) , Pura Pura Sector Samapa (al lado de la Cancha Polifuncional)</td><td>800140042</td></tr>
                                <tr><td>M.P. Rio Abuná (Modulo Policial Nº 10)</td><td>Calle Río Abuná, entre Río Piraí y Cuzco s/n, zona Bajo Tejar</td><td>800140032</td></tr>
                                <tr><td>M.P. San  Miguel</td><td>Pasaje Naira s/n (cerca Avenida Mariscal Montenegro), zona San Miguel</td><td>800140072</td></tr>
                                <tr><td>M.P. San Francisco</td><td>Planta baja  Mercado  Lanza s/n (Salida Calle Figueroa)</td><td>800140091</td></tr>
                                <tr><td>M.P. San Jorge</td><td>Calle Clavijo s/n (final, bajando gradas), zona San Jorge</td><td>800140092</td></tr>
                                <tr><td>M.P. San Luís</td><td>Calle Justo Ávila s/n (Complejo Deportico San Luis), zona San Luis</td><td>800140020</td></tr>
                                <tr><td>M.P. San Martin</td><td>Av. Saavedra s/n esq. Calle Litoral (al lado del Estadium Obrero), zona Miraflores Estadium</td><td>800140093</td></tr>
                                <tr><td>M.P. Santa Barbara</td><td>Calle Castro s/n ente Illimani y Obispo Indaburo, zona Santa Bárbara</td><td>800140088</td></tr>
                                <tr><td>M.P. Seguencoma 2da Meseta</td><td>Calle 4 s/n esq. Av. Circunvalación (parada Minibus 237)</td><td>800140076</td></tr>
                                <tr><td>M.P. Segundo Bascones (Alto Tejar)</td><td>Av. Segundo Bascones esq. Hermanos Lanza s/n, zona Alto Tejar</td><td>800140025</td></tr>
                                <tr><td>M.P. Trebol</td><td>Av. Manco Kapac esq. Vásquez s/n, zona San Sebastian</td><td>800140086</td></tr>
                                <tr><td>M.P. Venado</td><td>Calle  Omasuyos s/n, zona Challapampa.</td><td>800140044</td></tr>
                                <tr><td>M.P. Villa Armonía</td><td>Av. Nieves Linares s/n, zona Villa Armonía (al lado del Mercado Villa Armonía)</td><td>800140060</td></tr>
                                <tr><td>M.P. Villa Montes</td><td>Calle Villa Montes s/n (graderías a la Av. Buenos Aires), zona Alto San Pedro</td><td>800140018</td></tr>
                                <tr><td>M.P. Villa Nuevo Potosí</td><td>Calle 4  deMayo s/n (final), zona Villa Nuevo Potosí</td><td>800140014</td></tr>
                                <tr><td>M.P. Villa Victoria (Modulo Policial Nº 7)</td><td>Av. República esq. Naciones Unidas s/n, zona Villa Victoria</td><td>800140029</td></tr>
                                <tr><td>M.P. Zoológico</td><td>Av. la Florida s/n (frente al Zoológico), zona Mallasa</td><td>800140228</td></tr>
                            </tbody>
                        </table>
                    </p>
                    <p>ATENTAMENTE,</p>
                    <p>GOBIERNO AUTÓNOMO MUNICIPAL DE LA PAZ.</p>'''
            part2 = MIMEText(html, 'html', 'utf-8')

            # outer.attach(part1)
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
            self.labelStatus.setText('Estado: Listo')
            self.buttonSurveillance.setText('Iniciar Vigilancia')
        else:
            self.status = 'watching'
            self.labelStatus.setText('Estado: Vigilando')
            self.buttonSurveillance.setText('Detener Vigilancia')

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
        config['DEFAULT']['password'] = EncodeAES(cipher, user_password)
        # config['DEFAULT']['password'] = user_password
        config['DEFAULT']['resolution'] = resolution
        config['DEFAULT']['email-minutes'] = email_minutes
        config['DEFAULT']['photos-days'] = photos_days

        config.write()

        # check data
        if user_email != '' and user_password != '' and is_valid_email(user_email) and email_minutes.isdigit() and photos_days.isdigit():
            # send email
            self.user_email = user_email
            self.user_password = user_password
            self.email_minutes = int(email_minutes)
            self.resolution = resolution
            resp = self.send_confirm_email()
            if resp is None:
                self.status = 'unidentified'
                self.labelStatus.setText(_translate("Dialog",  "Estado: Error de identificación", None))
                self.buttonCamera.setEnabled(False)
                self.buttonSurveillance.setEnabled(False)
            else:
                self.status = 'identified'
                self.labelStatus.setText('Estado: Identificado')
                self.buttonCamera.setEnabled(True)
                self.buttonSurveillance.setEnabled(False)
                self.mdiArea.setActiveSubWindow(
                    self.mdiArea.subWindowList()[0])

            # delete older photos
            days = int(photos_days)
            if days > 0:
                delete_photos(days)

        else:
            # invalid data
            self.status = 'unidentified'
            self.labelStatus.setText(_translate("Dialog",  "Estado: Datos inválidos", None))
            self.buttonCamera.setEnabled(False)
            self.buttonSurveillance.setEnabled(False)

    def send_confirm_email(self):
        try:
            sender = self.user_email
            gmail_password = self.user_password
            recipients = [sender]

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Detector Vigilancia: Email confirmado"
            msg['From'] = sender
            msg['To'] = sender

            text = "Felicidades, su email fue confirmado."
            part1 = MIMEText(text, 'plain')

            html = "<p>Felicidades, su email fue confirmado.</p>"
            part2 = MIMEText(html, 'html')

            msg.attach(part1)
            msg.attach(part2)

            composed = msg.as_string()

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
    ex = Ui_Dialog()
    ex.show()
    valid_settings = False

    #config = configparser.ConfigParser()
    #config.read('C:/config.ini')
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
        user_password = DecodeAES(cipher, user_password)
        # user_password = user_password
        ex.lineEmail.setText(user_email)
        ex.linePassword.setText(user_password)
        valid_settings = True
        ex.user_email = user_email
        ex.user_password = user_password
        ex.resolution = resolution
        ex.email_minutes = minutes

    if valid_settings:
        ex.status = 'identified'
        ex.labelStatus.setText('Estado: Identificado')
        ex.buttonCamera.setEnabled(True)
        ex.buttonSurveillance.setEnabled(False)
        ex.mdiArea.setActiveSubWindow(
            ex.mdiArea.subWindowList()[0])

    sys.exit(app.exec_())
