# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fecha.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(593, 322)
        Dialog.setStyleSheet("")
        self.Date = QtWidgets.QCalendarWidget(Dialog)
        self.Date.setGeometry(QtCore.QRect(40, 20, 321, 231))
        self.Date.setStyleSheet("")
        self.Date.setObjectName("Date")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(380, 20, 171, 231))
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.boxLunes = QtWidgets.QCheckBox(self.groupBox)
        self.boxLunes.setGeometry(QtCore.QRect(60, 20, 70, 17))
        self.boxLunes.setObjectName("boxLunes")
        self.boxMartes = QtWidgets.QCheckBox(self.groupBox)
        self.boxMartes.setGeometry(QtCore.QRect(60, 50, 70, 17))
        self.boxMartes.setObjectName("boxMartes")
        self.boxMiercoles = QtWidgets.QCheckBox(self.groupBox)
        self.boxMiercoles.setGeometry(QtCore.QRect(60, 80, 70, 17))
        self.boxMiercoles.setObjectName("boxMiercoles")
        self.boxJueves = QtWidgets.QCheckBox(self.groupBox)
        self.boxJueves.setGeometry(QtCore.QRect(60, 110, 70, 17))
        self.boxJueves.setObjectName("boxJueves")
        self.boxViernes = QtWidgets.QCheckBox(self.groupBox)
        self.boxViernes.setGeometry(QtCore.QRect(60, 140, 70, 17))
        self.boxViernes.setObjectName("boxViernes")
        self.boxSabado = QtWidgets.QCheckBox(self.groupBox)
        self.boxSabado.setGeometry(QtCore.QRect(60, 170, 70, 17))
        self.boxSabado.setObjectName("boxSabado")
        self.BoxDomingo = QtWidgets.QCheckBox(self.groupBox)
        self.BoxDomingo.setGeometry(QtCore.QRect(60, 200, 70, 17))
        self.BoxDomingo.setObjectName("BoxDomingo")
        self.btnFecha = QtWidgets.QPushButton(Dialog)
        self.btnFecha.setGeometry(QtCore.QRect(250, 270, 111, 31))
        self.btnFecha.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnFecha.setStyleSheet("")
        self.btnFecha.setObjectName("btnFecha")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Dias no laborables"))
        self.boxLunes.setText(_translate("Dialog", "Lunes"))
        self.boxMartes.setText(_translate("Dialog", "Martes"))
        self.boxMiercoles.setText(_translate("Dialog", "Míercoles"))
        self.boxJueves.setText(_translate("Dialog", "Jueves"))
        self.boxViernes.setText(_translate("Dialog", "Viernes"))
        self.boxSabado.setText(_translate("Dialog", "Sábado"))
        self.BoxDomingo.setText(_translate("Dialog", "Domingo"))
        self.btnFecha.setText(_translate("Dialog", "Aceptar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
