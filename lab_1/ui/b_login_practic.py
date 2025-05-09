# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'b_login_practic.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(350, 240)
        Form.setMinimumSize(QSize(350, 240))
        Form.setMaximumSize(QSize(350, 240))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.lineEditLogin = QLineEdit(Form)
        self.lineEditLogin.setObjectName(u"lineEditLogin")
        self.lineEditLogin.setMinimumSize(QSize(100, 0))
        self.lineEditLogin.setFont(font)

        self.horizontalLayout.addWidget(self.lineEditLogin)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEditPassword = QLineEdit(Form)
        self.lineEditPassword.setObjectName(u"lineEditPassword")
        self.lineEditPassword.setMinimumSize(QSize(100, 0))
        self.lineEditPassword.setFont(font)
        self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout_2.addWidget(self.lineEditPassword)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonForgotPass = QPushButton(Form)
        self.pushButtonForgotPass.setObjectName(u"pushButtonForgotPass")
        self.pushButtonForgotPass.setMinimumSize(QSize(160, 24))
        self.pushButtonForgotPass.setFont(font)

        self.horizontalLayout_3.addWidget(self.pushButtonForgotPass)

        self.pushButtonRegistration = QPushButton(Form)
        self.pushButtonRegistration.setObjectName(u"pushButtonRegistration")
        self.pushButtonRegistration.setMinimumSize(QSize(160, 24))
        self.pushButtonRegistration.setFont(font)

        self.horizontalLayout_3.addWidget(self.pushButtonRegistration)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonOk = QPushButton(Form)
        self.pushButtonOk.setObjectName(u"pushButtonOk")
        self.pushButtonOk.setMinimumSize(QSize(160, 24))
        self.pushButtonOk.setFont(font)

        self.horizontalLayout_4.addWidget(self.pushButtonOk)

        self.pushButtonCancel = QPushButton(Form)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setMinimumSize(QSize(160, 24))
        self.pushButtonCancel.setFont(font)

        self.horizontalLayout_4.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Login       ", None))
        self.lineEditLogin.setPlaceholderText(QCoreApplication.translate("Form", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043b\u043e\u0433\u0438\u043d", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Password ", None))
        self.lineEditPassword.setPlaceholderText(QCoreApplication.translate("Form", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.pushButtonForgotPass.setText(QCoreApplication.translate("Form", u"\u0417\u0430\u0431\u044b\u043b\u0438 \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.pushButtonRegistration.setText(QCoreApplication.translate("Form", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f", None))
        self.pushButtonOk.setText(QCoreApplication.translate("Form", u"\u041e\u043a", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("Form", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

