import sys, re, os, string, re
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import numpy as np
from datetime import date, datetime, timedelta

#from src.Perl import Perl
from src.view.principal import Ui_Principal
from src.view.fecha import Ui_Dialog


class MainWindow(QMainWindow):
    # Constructor
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Principal()
        self.ui.setupUi(self)
        self.perl = Perl(self.ui)
  
        
######
######
##          PERL
       
class Perl(QMainWindow):

    #Método constructor de la clase
    def __init__(self, ui):
         super(Perl, self).__init__()
         self.ui = ui
 
         self.ui.btnGenera.clicked.connect(self.genera)
         self.ui.btnNuevo.clicked.connect(self.limpia)
         self.ui.btnCalcular.clicked.connect(self.calculo)
         self.ui.btnCalcular.setEnabled(False)

         # Atributos
         self.fechInicio = ""
         #+establecer el ancho de columnas
         for indice, ancho in enumerate((70, 109, 90, 30, 30, 30), start=0):
             self.ui.tabla.setColumnWidth(indice, ancho)
         
         for indice, ancho in enumerate((35, 35, 30, 30, 30, 30, 35,35, 140,120,136,110), start=0):
             self.ui.tablaView.setColumnWidth(indice, ancho)
         #self.ui.tablaView.horizontalHeader(columns)
         self.ui.tablaView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    #generamos la tabla 
    def genera(self):
        self.ui.btnCalcular.setEnabled(True)
        self.variables = self.ui.canVariable.value()
        #establecer el alto de filas
        #Bself.ui.tabla.verticalHeader().setDefaultSectionSize(20)
        self.ui.tabla.verticalHeader().setVisible(False)
        #self.ui.tablaView.verticalHeader().setDefaultSectionSize(20)
        self.ui.tablaView.verticalHeader().setVisible(False)
        
        self.Actividades = []
        
        #poner las letras del abecedario
        if(self.variables > 20):
            QMessageBox.information(None, ('Error'), ('Se permiten solo 20'))
        else:
            self.ui.tabla.setRowCount(self.variables)
            self.ui.tablaView.setRowCount(self.variables)
            self.abec = list(map(chr, range(65, 91)))
            for i in range(self.variables):
                self.Actividades.append(self.abec[i])
                celda = QTableWidgetItem(self.abec[i])
                celda.setTextAlignment(Qt.AlignHCenter)
                self.ui.tabla.setItem(i, 0, celda)
                self.ui.tabla.setItem(i,2, QTableWidgetItem(" "))
                self.ui.tabla.setItem(i,1, QTableWidgetItem(" "))
            
            
        ##
    def calculo(self):
        try:
            self.Predecesores = []
        
            """pOR EL MOMENTO"""
            # Bucle: Obtiene los valores de la columna Predecesora
            for f in range(self.variables):
                valor = self.ui.tabla.item(f,2).text()
                self.Predecesores.append(valor)
                regex = re.search(r" |^[A-Z]{1}$|^[A-Z]{1}(,[A-Z]{1}){1,10}$", valor)
                if(regex == None):
                    raise Exception('Error en el predecesor .')

                prede = regex.group()
                listPrede = prede.split(sep=",")
                for value in range(len(listPrede)):
                    if(listPrede[value] != " " and not(listPrede[value] in self.Actividades)):
                        raise Exception(f'El predecesor "{listPrede[value]}" no existe')

                for j in range(3):
                    if self.ui.tabla.item(f,j+3) == None:
                        raise Exception('Error algún campo vacío')
          
            #abrimos ventana para la fecha
            self.dialog = Dialog()
            self.dialog.show()
            self.DijOij = self.calculaDijOij(self.variables)
            self.calculaTiempos(self.variables)
            self.dialog.ui.btnFecha.clicked.connect(self.fechaobten)
            
            
        except Exception as err:
            
            QMessageBox.information(None, ('Error'), str(err))

   
    # Método: Calcula el valor de Dij y Oij
    def calculaDijOij(self, filas):
        try:
            dij = []
            oij = []
            for f in range(filas):
                valores = []
                for c in range(3):
                    valor = int(self.ui.tabla.item(f,c+3).text())
                    valores.append(valor)
                
                valorDij = (valores[0] + (4 * valores[1]) + valores[2]) / 6
                valorDij = round(valorDij)
                dij.append(valorDij)
                
                valorOij = pow(((valores[2] - valores[0]) / 6), 2)
                valorOij = round(valorOij, 2)
                oij.append(valorOij)
                
                # Inserta los valores Dij en la tabla
                celdaDij = QTableWidgetItem(str(valorDij))
                celdaDij.setTextAlignment(Qt.AlignCenter)
                self.ui.tablaView.setItem(f, 0, celdaDij)
                
                # Inserta los valores Oij en la tabla
                celdaOij = QTableWidgetItem(str(valorOij))
                celdaOij.setTextAlignment(Qt.AlignCenter)
                self.ui.tablaView.setItem(f, 1, celdaOij)
                
            return dij, oij
        except Exception as err:
            QMessageBox.information(None, ('Error'), str(err))
    
    # Méctodo: Calcula los tiempo
    def calculaTiempos(self, filas):
        # Calcula e inserta los valores de Ti0 y Tj0
        self.Ti0 = []
        self.Tj0 = []
        self.Ti1 = []
        self.Tj1 = []
        for f in range(filas):
            validarPrece = []
            valorPrece = self.ui.tabla.item(f,2).text()
            
            if(valorPrece == " "):
                celdaTi0 = QTableWidgetItem(str(0))
                celdaTi0.setTextAlignment(Qt.AlignCenter)
                self.ui.tablaView.setItem(f, 2, celdaTi0)
                self.Ti0.append(0)
                
                celdaTj0 = QTableWidgetItem(str(self.DijOij[0][f]))
                celdaTj0.setTextAlignment(Qt.AlignCenter)
                self.ui.tablaView.setItem(f, 4, celdaTj0)
                self.Tj0.append(self.DijOij[0][f])
                
            else:
                listPrede = valorPrece.split(sep=",")
                for value in range(len(listPrede)):
                    indexFilaTc = self.Actividades.index(listPrede[value])
                    valorPreceTc = int(self.ui.tablaView.item(indexFilaTc,4).text())
                    validarPrece.append(valorPreceTc)
                
                valorMax = max(validarPrece)
                celdaTi0 = QTableWidgetItem(str(valorMax))
                celdaTi0.setTextAlignment(Qt.AlignCenter)
                self.ui.tablaView.setItem(f, 2, celdaTi0)
                self.Ti0.append(valorMax)
                
                celdaTj0 = QTableWidgetItem(str(valorMax + self.DijOij[0][f]))
                celdaTj0.setTextAlignment(Qt.AlignCenter)
                self.ui.tablaView.setItem(f, 4, celdaTj0)
                self.Tj0.append(valorMax + self.DijOij[0][f])
                
         # Calcula e inserta los valores de Ti1 y Tj1
        lastFilaAct = len(self.Actividades)-1
        validarLastAct = []
        for i in range(lastFilaAct, -1, -1):
            validarPreceLast = []
            valorPreceLast = self.ui.tabla.item(i,2).text()
            if(len(self.Actividades) == i+1):
                vMax = max(self.Tj0)
                celdaTj1 = QTableWidgetItem(str(vMax))
                celdaTj1.setTextAlignment(Qt.AlignCenter)
                self.ui.tablaView.setItem(i, 5, celdaTj1)
                self.Tj1.append(vMax)
                
                celdaTi1 = QTableWidgetItem(str(vMax - self.DijOij[0][i]))
                celdaTi1.setTextAlignment(Qt.AlignCenter)
                self.ui.tablaView.setItem(i, 3, celdaTi1)
                self.Ti1.append(vMax - self.DijOij[0][i])
                
                listPredeLast = valorPreceLast.split(sep=",")
                validarLastAct.append(listPredeLast)
            else:
                listPredeLast = valorPreceLast.split(sep=",")
                validarLastAct.append(listPredeLast)
                indexFilaLast = []
                for value in range(len(validarLastAct)):
                    if(self.Actividades[i] in validarLastAct[value]):
                        predecesor = ",".join(validarLastAct[value])
                        index = [indice for indice in range(len(self.Predecesores)) if self.Predecesores[indice] == predecesor]
                        
                        for ind in index:
                            if(not(ind in indexFilaLast)):
                                indexFilaLast.append(ind)
                
                if(len(indexFilaLast) == 0):
                    valorTj0 = int(self.ui.tablaView.item(i+1, 5).text())
                    celdaTj1 = QTableWidgetItem(str(valorTj0))
                    celdaTj1.setTextAlignment(Qt.AlignCenter)
                    self.ui.tablaView.setItem(i, 5, celdaTj1)
                    self.Tj1.append(valorTj0)
                    
                    celdaTi1 = QTableWidgetItem(str(valorTj0 - self.DijOij[0][i]))
                    celdaTi1.setTextAlignment(Qt.AlignCenter)
                    self.ui.tablaView.setItem(i, 3, celdaTi1)
                    self.Ti1.append(valorTj0 - self.DijOij[0][i])
                else:
                    valorPreceMin = []
                    for valor in indexFilaLast:
                        valorTj0 = int(self.ui.tablaView.item(valor,3).text())
                        valorPreceMin.append(valorTj0)
                    
                    valorMin = min(valorPreceMin)
                    celdaTj1 = QTableWidgetItem(str(valorMin))
                    celdaTj1.setTextAlignment(Qt.AlignCenter)
                    self.ui.tablaView.setItem(i, 5, celdaTj1)
                    self.Tj1.append(valorMin)
                    
                    celdaTi1 = QTableWidgetItem(str(valorMin - self.DijOij[0][i]))
                    celdaTi1.setTextAlignment(Qt.AlignCenter)
                    self.ui.tablaView.setItem(i, 3, celdaTi1)
                    self.Ti1.append(valorMin - self.DijOij[0][i])
                    
        # Ejecutamos el método para hallar las holguras
        self.calcularMtMl(filas)
    
    # Método: Genera los valores de los Margenes Totales y Libres
    def calcularMtMl(self, filas):
        self.MTij = []
        self.MLij = []
        tj1 = list(reversed(self.Tj1))
        ti0 = self.Ti0
        tj0 = self.Tj0
        dij = self.DijOij[0]
        
        for f in range(filas):
            mtij = (tj1[f] - ti0[f] - dij[f])
            celdaMTij = QTableWidgetItem(str(mtij))
            celdaMTij.setTextAlignment(Qt.AlignCenter)
            self.ui.tablaView.setItem(f, 6, celdaMTij)
            self.MTij.append(mtij)
            
            mlij = (tj0[f] - ti0[f] - dij[f])
            celdaMLij = QTableWidgetItem(str(mlij))
            celdaMLij.setTextAlignment(Qt.AlignCenter)
            self.ui.tablaView.setItem(f, 7, celdaMLij)
            self.MLij.append(mlij)
        

    # Método: Obtine los días no laborables
    def getDiasNoLab(self):
        self.diasNoLab = []
        
        if(self.dialog.ui.boxLunes.isChecked()):
            dia = "Monday"
            self.diasNoLab.append(dia)
            
        if(self.dialog.ui.boxMartes.isChecked()):
            dia = "Tuesday"
            self.diasNoLab.append(dia)
            
        if(self.dialog.ui.boxMiercoles.isChecked()):
            dia = "Wednesday"
            self.diasNoLab.append(dia)
            
        if(self.dialog.ui.boxJueves.isChecked()):
            dia = "Thursday"
            self.diasNoLab.append(dia)
            
        if(self.dialog.ui.boxViernes.isChecked()):
            dia = "Friday"
            self.diasNoLab.append(dia)
            
        if(self.dialog.ui.boxSabado.isChecked()):
            dia = "Saturday"
            self.diasNoLab.append(dia)
            
        if(self.dialog.ui.BoxDomingo.isChecked()):
            dia = "Sunday"
            self.diasNoLab.append(dia)
       
     # fehc
    def fechaobten(self):
        self.fechInicio = self.dialog.ui.Date.selectedDate().toPyDate()
        self.getDiasNoLab()
        self.generateDate(self.variables)

    #callcular lad fechas
    def calcuFecha(self, tiempo):
        self.fechaLab = self.fechInicio
        i = 0
        while(i < tiempo):
            if(i == 0):
                dia = self.fechInicio + timedelta(days=i)
            else:
                self.fechaLab = self.fechaLab + timedelta(days=1)
                diaActual = self.fechaLab.strftime("%A")
                if(diaActual in self.diasNoLab):
                    i -= 1
            i += 1

        return self.fechaLab
            
        
    # Método: Calcula e inserta las fechas
    def generateDate(self, filas):
        
        self.Ti1 = list(reversed(self.Ti1))
        self.Tj1 = list(reversed(self.Tj1))
        for f in range(filas):
            
            ti0 = self.Ti0[f]
            ti1 = self.Ti1[f]
            tj0 = self.Tj0[f]
            tj1 = self.Tj1[f]

            # Fecha Inicio Temprano
            fi0 = self.calcuFecha(ti0)
            diaStr = QTableWidgetItem(fi0.strftime("%d/%m/%Y"))
            diaStr.setTextAlignment(Qt.AlignCenter)
            self.ui.tablaView.setItem(f,8,diaStr)
            
            # Fecha Inicio Tardio
            fi1 = self.calcuFecha(ti1)
            diaStr = QTableWidgetItem(fi1.strftime("%d/%m/%Y"))
            diaStr.setTextAlignment(Qt.AlignCenter)
            self.ui.tablaView.setItem(f,9,diaStr)
            
            # Fecha Fin Temprano
            fj0 = self.calcuFecha(tj0)
            diaStr = QTableWidgetItem(fj0.strftime("%d/%m/%Y"))
            diaStr.setTextAlignment(Qt.AlignCenter)
            self.ui.tablaView.setItem(f,10,diaStr)
            
            # Fecha Fin Tardio
            fj1 = self.calcuFecha(tj1)
            diaStr = QTableWidgetItem(fj1.strftime("%d/%m/%Y"))
            diaStr.setTextAlignment(Qt.AlignCenter)
            self.ui.tablaView.setItem(f,11,diaStr)
            
        # Búcle: colorea las actividades críticas
        rutaCritica = [index for index in range(len(self.MTij)) if self.MTij[index] == 0]
        
        for ruta in rutaCritica:
            for g in range(6):
                self.ui.tabla.item(ruta,g).setBackground(QtGui.QColor('red'))
            for k in range(12):
                self.ui.tablaView.item(ruta,k).setBackground(QtGui.QColor('red'))
            
    

    #limpiar la tabla
    def limpia(self):
        self.ui.btnCalcular.setEnabled(False)
        self.ui.tabla.clearContents()
        self.ui.tabla.setRowCount(0)
        self.ui.tablaView.clearContents()
        self.ui.tablaView.setRowCount(0)


#####
#####
##          VENTANA FECHA
class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  
        self.setWindowTitle("Fecha")
        self.ui.btnFecha.clicked.connect(self.close)


######
######
###         SIMPLEX




# Inicia la aplicación
if __name__ == '__main__':    
    app = QApplication([])
    mi_App = MainWindow()
    mi_App.show()
    sys.exit(app.exec_())