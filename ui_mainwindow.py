# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 634)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_7 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.manual_tab = QWidget()
        self.manual_tab.setObjectName(u"manual_tab")
        self.horizontalLayout_10 = QHBoxLayout(self.manual_tab)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.image_robotic_arm = QLabel(self.manual_tab)
        self.image_robotic_arm.setObjectName(u"image_robotic_arm")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_robotic_arm.sizePolicy().hasHeightForWidth())
        self.image_robotic_arm.setSizePolicy(sizePolicy)
        self.image_robotic_arm.setPixmap(QPixmap(u":/images/robot_arm.jpg"))
        self.image_robotic_arm.setScaledContents(True)

        self.horizontalLayout_10.addWidget(self.image_robotic_arm)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.checkbox_joystick = QCheckBox(self.manual_tab)
        self.checkbox_joystick.setObjectName(u"checkbox_joystick")
        self.checkbox_joystick.setTristate(False)

        self.horizontalLayout_9.addWidget(self.checkbox_joystick)

        self.label_joystick_status = QLabel(self.manual_tab)
        self.label_joystick_status.setObjectName(u"label_joystick_status")

        self.horizontalLayout_9.addWidget(self.label_joystick_status)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.checkbox_gripper = QCheckBox(self.manual_tab)
        self.checkbox_gripper.setObjectName(u"checkbox_gripper")

        self.horizontalLayout_6.addWidget(self.checkbox_gripper)

        self.button_home = QPushButton(self.manual_tab)
        self.button_home.setObjectName(u"button_home")

        self.horizontalLayout_6.addWidget(self.button_home)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_base = QLabel(self.manual_tab)
        self.label_base.setObjectName(u"label_base")

        self.verticalLayout.addWidget(self.label_base)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_base_minus = QPushButton(self.manual_tab)
        self.button_base_minus.setObjectName(u"button_base_minus")
        icon = QIcon()
        icon.addFile(u":/images/minus_.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_base_minus.setIcon(icon)

        self.horizontalLayout.addWidget(self.button_base_minus)

        self.spinBox_base = QSpinBox(self.manual_tab)
        self.spinBox_base.setObjectName(u"spinBox_base")
        self.spinBox_base.setKeyboardTracking(False)
        self.spinBox_base.setMaximum(180)
        self.spinBox_base.setValue(90)

        self.horizontalLayout.addWidget(self.spinBox_base)

        self.button_base_plus = QPushButton(self.manual_tab)
        self.button_base_plus.setObjectName(u"button_base_plus")
        icon1 = QIcon()
        icon1.addFile(u":/images/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_base_plus.setIcon(icon1)

        self.horizontalLayout.addWidget(self.button_base_plus)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_6.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_shoulder = QLabel(self.manual_tab)
        self.label_shoulder.setObjectName(u"label_shoulder")

        self.verticalLayout_2.addWidget(self.label_shoulder)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_shoulder_minus = QPushButton(self.manual_tab)
        self.button_shoulder_minus.setObjectName(u"button_shoulder_minus")
        self.button_shoulder_minus.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.button_shoulder_minus)

        self.spinBox_shoulder = QSpinBox(self.manual_tab)
        self.spinBox_shoulder.setObjectName(u"spinBox_shoulder")
        self.spinBox_shoulder.setKeyboardTracking(False)
        self.spinBox_shoulder.setMaximum(180)
        self.spinBox_shoulder.setValue(180)

        self.horizontalLayout_2.addWidget(self.spinBox_shoulder)

        self.button_shoulder_plus = QPushButton(self.manual_tab)
        self.button_shoulder_plus.setObjectName(u"button_shoulder_plus")
        self.button_shoulder_plus.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.button_shoulder_plus)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_6.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_elbow = QLabel(self.manual_tab)
        self.label_elbow.setObjectName(u"label_elbow")

        self.verticalLayout_3.addWidget(self.label_elbow)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.button_elbow_minus = QPushButton(self.manual_tab)
        self.button_elbow_minus.setObjectName(u"button_elbow_minus")
        self.button_elbow_minus.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.button_elbow_minus)

        self.spinBox_elbow = QSpinBox(self.manual_tab)
        self.spinBox_elbow.setObjectName(u"spinBox_elbow")
        self.spinBox_elbow.setKeyboardTracking(False)
        self.spinBox_elbow.setMaximum(180)
        self.spinBox_elbow.setValue(5)

        self.horizontalLayout_3.addWidget(self.spinBox_elbow)

        self.button_elbow_plus = QPushButton(self.manual_tab)
        self.button_elbow_plus.setObjectName(u"button_elbow_plus")
        self.button_elbow_plus.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.button_elbow_plus)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_wrist = QLabel(self.manual_tab)
        self.label_wrist.setObjectName(u"label_wrist")

        self.verticalLayout_4.addWidget(self.label_wrist)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.button_wrist_minus = QPushButton(self.manual_tab)
        self.button_wrist_minus.setObjectName(u"button_wrist_minus")
        self.button_wrist_minus.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.button_wrist_minus)

        self.spinBox_wrist = QSpinBox(self.manual_tab)
        self.spinBox_wrist.setObjectName(u"spinBox_wrist")
        self.spinBox_wrist.setKeyboardTracking(False)
        self.spinBox_wrist.setMaximum(180)
        self.spinBox_wrist.setValue(90)

        self.horizontalLayout_4.addWidget(self.spinBox_wrist)

        self.button_wrist_plus = QPushButton(self.manual_tab)
        self.button_wrist_plus.setObjectName(u"button_wrist_plus")
        self.button_wrist_plus.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.button_wrist_plus)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_gripper = QLabel(self.manual_tab)
        self.label_gripper.setObjectName(u"label_gripper")

        self.verticalLayout_5.addWidget(self.label_gripper)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.button_gripper_minus = QPushButton(self.manual_tab)
        self.button_gripper_minus.setObjectName(u"button_gripper_minus")
        self.button_gripper_minus.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.button_gripper_minus)

        self.spinBox_gripper = QSpinBox(self.manual_tab)
        self.spinBox_gripper.setObjectName(u"spinBox_gripper")
        self.spinBox_gripper.setKeyboardTracking(False)
        self.spinBox_gripper.setMaximum(180)

        self.horizontalLayout_5.addWidget(self.spinBox_gripper)

        self.button_gripper_plus = QPushButton(self.manual_tab)
        self.button_gripper_plus.setObjectName(u"button_gripper_plus")
        self.button_gripper_plus.setIcon(icon1)

        self.horizontalLayout_5.addWidget(self.button_gripper_plus)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)


        self.horizontalLayout_10.addLayout(self.verticalLayout_6)

        self.tabWidget.addTab(self.manual_tab, "")
        self.head_tab = QWidget()
        self.head_tab.setObjectName(u"head_tab")
        self.verticalLayout_14 = QVBoxLayout(self.head_tab)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_camera = QLabel(self.head_tab)
        self.label_camera.setObjectName(u"label_camera")
        sizePolicy.setHeightForWidth(self.label_camera.sizePolicy().hasHeightForWidth())
        self.label_camera.setSizePolicy(sizePolicy)
        self.label_camera.setMinimumSize(QSize(640, 480))
        self.label_camera.setStyleSheet(u"background-color: black; color: white; border: 2px solid red;")
        self.label_camera.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.label_camera)

        self.tabWidget.addTab(self.head_tab, "")
        self.voice_tab = QWidget()
        self.voice_tab.setObjectName(u"voice_tab")
        self.verticalLayout_9 = QVBoxLayout(self.voice_tab)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_voice_status = QLabel(self.voice_tab)
        self.label_voice_status.setObjectName(u"label_voice_status")

        self.verticalLayout_9.addWidget(self.label_voice_status)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.text_voice_log = QPlainTextEdit(self.voice_tab)
        self.text_voice_log.setObjectName(u"text_voice_log")

        self.horizontalLayout_8.addWidget(self.text_voice_log)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.text_voice_input = QPlainTextEdit(self.voice_tab)
        self.text_voice_input.setObjectName(u"text_voice_input")

        self.verticalLayout_8.addWidget(self.text_voice_input)

        self.text_command_sheet = QPlainTextEdit(self.voice_tab)
        self.text_command_sheet.setObjectName(u"text_command_sheet")

        self.verticalLayout_8.addWidget(self.text_command_sheet)


        self.horizontalLayout_8.addLayout(self.verticalLayout_8)


        self.verticalLayout_9.addLayout(self.horizontalLayout_8)

        self.tabWidget.addTab(self.voice_tab, "")

        self.horizontalLayout_7.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 940, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.image_robotic_arm.setText("")
        self.checkbox_joystick.setText(QCoreApplication.translate("MainWindow", u"Joystick", None))
        self.label_joystick_status.setText(QCoreApplication.translate("MainWindow", u"Joystick: Not Activate", None))
        self.checkbox_gripper.setText(QCoreApplication.translate("MainWindow", u"Gripper", None))
        self.button_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.label_base.setText(QCoreApplication.translate("MainWindow", u"Base", None))
        self.button_base_minus.setText("")
        self.button_base_plus.setText("")
        self.label_shoulder.setText(QCoreApplication.translate("MainWindow", u"Shoulder", None))
        self.button_shoulder_minus.setText("")
        self.button_shoulder_plus.setText("")
        self.label_elbow.setText(QCoreApplication.translate("MainWindow", u"Elbow", None))
        self.button_elbow_minus.setText("")
        self.button_elbow_plus.setText("")
        self.label_wrist.setText(QCoreApplication.translate("MainWindow", u"Wrist", None))
        self.button_wrist_minus.setText("")
        self.button_wrist_plus.setText("")
        self.label_gripper.setText(QCoreApplication.translate("MainWindow", u"Gripper", None))
        self.button_gripper_minus.setText("")
        self.button_gripper_plus.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.manual_tab), QCoreApplication.translate("MainWindow", u"Manual Control", None))
        self.label_camera.setText(QCoreApplication.translate("MainWindow", u"Camera OFF", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.head_tab), QCoreApplication.translate("MainWindow", u"Head Control", None))
        self.label_voice_status.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.text_voice_log.setPlainText("")
        self.text_voice_input.setPlainText("")
        self.text_command_sheet.setPlainText(QCoreApplication.translate("MainWindow", u"Selection Option:\n"
"> A, B, C, D, E, F, G, H, J\n"
"> HOME\n"
"> NEXT\n"
"> FINISH\n"
"\n"
"Confirmation:\n"
"> YES, YUP, YEAH\n"
"> NO, NOPE, NAH\n"
"\n"
"\n"
"", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.voice_tab), QCoreApplication.translate("MainWindow", u"Voice Control", None))
    # retranslateUi

