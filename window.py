# window.py

# imports
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog,
                               QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QMenu, QMessageBox, QPushButton,
                               QSpinBox, QStyle, QSystemTrayIcon, QTextEdit,
                               QVBoxLayout)

import rc_systray


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.iconGroupBox = QGroupBox()
        self.iconLabel = QLabel()
        self.iconComboBox = QComboBox()
        self.showIconCheckBox = QCheckBox()

        self.messageGroupBox = QGroupBox()
        self.typeLabel = QLabel()
        self.durationLabel = QLabel()
        self.durationWarningLabel = QLabel()
        self.titleLabel = QLabel()
        self.bodyLabel = QLabel()

        self.typeComboBox = QComboBox()
        self.durationSpinBox = QSpinBox()
        self.titleEdit = QLineEdit()
        self.bodyEdit = QTextEdit()
        self.showMessageButton = QPushButton()

        self.minimizeAction = QAction()
        self.maximizeAction = QAction()
        self.restoreAction = QAction()
        self.quitAction = QAction()

        self.trayIcon = QSystemTrayIcon()
        self.trayIconMenu = QMenu()

        self.createIconGroupBox()
        self.createMessageGroupBox()

        self.iconLabel.setMinimumWidth(self.durationLabel.sizeHint().width())

        self.createActions()
        self.createTrayIcon()

        self.showMessageButton.clicked.connect(self.showMessage)
        self.showIconCheckBox.toggled.connect(self.trayIcon.setVisible)
        self.iconComboBox.currentIndexChanged.connect(self.setIcon)
        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.activated.connect(self.iconActivated)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.iconGroupBox)
        self.mainLayout.addWidget(self.messageGroupBox)
        self.setLayout(self.mainLayout)

        self.iconComboBox.setCurrentIndex(1)
        self.trayIcon.show()

        self.setWindowTitle("Systray")
        self.resize(400, 300)

    def setVisible(self, visible):
        self.minimizeAction.setEnabled(visible)
        self.maximizeAction.setEnabled(not self.isMaximized())
        self.restoreAction.setEnabled(self.isMaximized() or not visible)
        super().setVisible(visible)

    def closeEvent(self, event):
        if not event.spontaneous() or not self.isVisible():
            return
        if self.trayIcon.isVisible():
            QMessageBox.information(self, "Systray",
                                    "The program will keep running in the system tray. "
                                    "To terminate the program, choose <b>Quit</b> in the context "
                                    "menu of the system tray entry.")
            self.hide()
            event.ignore()

    @Slot(int)
    def setIcon(self, index):
        icon = self.iconComboBox.itemIcon(index)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self.trayIcon.setToolTip(self.iconComboBox.itemText(index))

    @Slot(str)
    def iconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            pass
        if reason == QSystemTrayIcon.DoubleClick:
            self.iconComboBox.setCurrentIndex(
                (self.iconComboBox.currentIndex() + 1) % self.iconComboBox.count()
            )
        if reason == QSystemTrayIcon.MiddleClick:
            self.showMessage()

    @Slot()
    def showMessage(self):
        self.showIconCheckBox.setChecked(True)
        selectedIcon = self.typeComboBox.itemData(self.typeComboBox.currentIndex())
        msgIcon = QSystemTrayIcon.MessageIcon(selectedIcon)

        if selectedIcon == -1:  # custom icon
            icon = QIcon(self.iconComboBox.itemIcon(self.iconComboBox.currentIndex()))
            self.trayIcon.showMessage(
                self.titleEdit.text(),
                self.bodyEdit.toPlainText(),
                icon,
                self.durationSpinBox.value() * 1000,
            )
        else:
            self.trayIcon.showMessage(
                self.titleEdit.text(),
                self.bodyEdit.toPlainText(),
                msgIcon,
                self.durationSpinBox.value() * 1000,
            )

    @Slot()
    def messageClicked(self):
        QMessageBox.information(None, "Systray",
                                "Sorry, I already gave what help I could.\n"
                                "Maybe you should try asking a human?")

    def createIconGroupBox(self):
        self.iconGroupBox = QGroupBox("Tray Icon")

        self.iconLabel = QLabel("Icon:")

        self.iconComboBox = QComboBox()
        self.iconComboBox.addItem(QIcon(":/images/bad.png"), "Bad")
        self.iconComboBox.addItem(QIcon(":/images/heart.png"), "Heart")
        self.iconComboBox.addItem(QIcon(":/images/trash.png"), "Trash")

        self.showIconCheckBox = QCheckBox("Show icon")
        self.showIconCheckBox.setChecked(True)

        iconLayout = QHBoxLayout()
        iconLayout.addWidget(self.iconLabel)
        iconLayout.addWidget(self.iconComboBox)
        iconLayout.addStretch()
        iconLayout.addWidget(self.showIconCheckBox)
        self.iconGroupBox.setLayout(iconLayout)

    def createMessageGroupBox(self):
        self.messageGroupBox = QGroupBox("Balloon Message")

        self.typeLabel = QLabel("Type:")

        self.typeComboBox = QComboBox()
        self.typeComboBox.addItem("None", QSystemTrayIcon.NoIcon)
        self.typeComboBox.addItem(
            self.style().standardIcon(QStyle.SP_MessageBoxInformation),
            "Information",
            QSystemTrayIcon.Information,
        )
        self.typeComboBox.addItem(
            self.style().standardIcon(QStyle.SP_MessageBoxWarning),
            "Warning",
            QSystemTrayIcon.Warning,
        )
        self.typeComboBox.addItem(
            self.style().standardIcon(QStyle.SP_MessageBoxCritical),
            "Critical",
            QSystemTrayIcon.Critical,
        )
        self.typeComboBox.addItem(QIcon(), "Custom icon", -1)
        self.typeComboBox.setCurrentIndex(1)

        self.durationLabel = QLabel("Duration:")

        self.durationSpinBox = QSpinBox()
        self.durationSpinBox.setRange(5, 60)
        self.durationSpinBox.setSuffix(" s")
        self.durationSpinBox.setValue(15)

        self.durationWarningLabel = QLabel("(some systems might ignore this hint)")
        self.durationWarningLabel.setIndent(10)

        self.titleLabel = QLabel("Title:")
        self.titleEdit = QLineEdit("Cannot connect to network")
        self.bodyLabel = QLabel("Body:")

        self.bodyEdit = QTextEdit()
        self.bodyEdit.setPlainText("Don't believe me. Honestly, I don't have a clue."
                                   "\nClick this balloon for details.")

        self.showMessageButton = QPushButton("Show Message")
        self.showMessageButton.setDefault(True)

        messageLayout = QGridLayout()
        messageLayout.addWidget(self.typeLabel, 0, 0)
        messageLayout.addWidget(self.typeComboBox, 0, 1, 1, 2)
        messageLayout.addWidget(self.durationLabel, 1, 0)
        messageLayout.addWidget(self.durationSpinBox, 1, 1)
        messageLayout.addWidget(self.durationWarningLabel, 1, 2, 1, 3)
        messageLayout.addWidget(self.titleLabel, 2, 0)
        messageLayout.addWidget(self.titleEdit, 2, 1, 1, 4)
        messageLayout.addWidget(self.bodyLabel, 3, 0)
        messageLayout.addWidget(self.bodyEdit, 3, 1, 2, 4)
        messageLayout.addWidget(self.showMessageButton, 5, 4)
        messageLayout.setColumnStretch(3, 1)
        messageLayout.setRowStretch(4, 1)
        self.messageGroupBox.setLayout(messageLayout)

    def createActions(self):
        self.minimizeAction = QAction("Minimize", self)
        self.minimizeAction.triggered.connect(self.hide)

        self.maximizeAction = QAction("Maximize", self)
        self.maximizeAction.triggered.connect(self.showMaximized)

        self.restoreAction = QAction("Restore", self)
        self.restoreAction.triggered.connect(self.showNormal)

        self.quitAction = QAction("Quit", self)
        self.quitAction.triggered.connect(qApp.quit)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
