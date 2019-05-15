# -*- coding: utf-8 -*-
"""
Created on Thu May  9 23:07:01 2019

@author: TranA
"""


from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtGui import QBrush, QPen,QPainter, QImage, QPalette
from PyQt5.QtCore import Qt, QSize
import time
import math
import os
import pandas as pd
from pathlib import Path


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Détection d'obstacle PyQt"
        self.top = 200
        self.left = 500
        self.width = 900
        self.height = 900
        self.mid = 450
        self.InitWindow()
        
        #Ajout de la liste d'Objet;
        self.lstOfObject = []
        self.lstOfColor = []
        self.boolTraitement = 0
        
        
        #Ajout du background:
        oImage = QImage("background.png")
        sImage = oImage.scaled(QSize(900,900))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.show()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        #painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.setBrush(QBrush(Qt.red, Qt.VerPattern))

        self.getLstOfObject();
        if self.boolTraitement == 1 or self.lstOfObject:
            cpt = 0
            self.erase(painter);
            for obj in self.lstOfObject:
                polarPoint = obj
                
                if self.lstOfColor[cpt] == 'G':
                    painter.setPen(QPen(Qt.green, 5, Qt.SolidLine))
                    cpt += 1
                elif self.lstOfColor[cpt] == 'Y':
                    painter.setPen(QPen(Qt.yellow, 5, Qt.SolidLine))
                    cpt += 1
                elif self.lstOfColor[cpt] == 'R':
                    painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
                    cpt += 1
                    
                for element in polarPoint:
                    #Choix de la couleur pour le crayon :
                    
                    rad = math.radians(element[0]);
                    real_x = int((element[1] /100)* math.degrees(math.cos(rad))) + self.mid;
                    real_y = int((element[1] /100) * math.degrees(math.sin(rad))) + self.mid;
                    #print("x :", real_x, "y :", real_y);
                    painter.drawPoint(real_x, real_y);
            
        self.update();

    def erase(self, painter):
        painter.eraseRect(0, 0, self.width, self.height);
        
    def getLstOfObject(self):
        dec = 0.4;
        dec_dist = 2;
        drap = 0;
        result_lst = [];
        tmp_lst = [];
    
        try:    
            config = Path("./save.csv");
        except FileNotFoundError:
            print("File not found")
        
        
        if config.is_file():
            self.boolTraitement = 1;
            time.sleep(.05);
            df = pd.read_csv("./save.csv");
            print("Fichier existant !\n");
            l = df.values.tolist();
            
            
            
            for element in l:
                if result_lst == []:
                    tmp_lst.append(element);
                    result_lst.append(tmp_lst);
                else:
                    for values in result_lst:
                    #Recherche d'une place potentiel dans les tableaux éxistants
                        values_len = len(values);
                        for i in range(values_len):
                            actualAngl = values[i][0];
                            actualDist = values[i][1];
                            elementAngl = element[0];
                            elementDist = element[1];
                            if  elementAngl >= actualAngl and  elementAngl <= actualAngl + dec and elementDist >= actualDist - dec_dist and elementDist <= actualDist + dec_dist:
                                values.insert(i + 1, element);
                                drap = 1;
                            elif elementAngl >= actualAngl - dec and elementAngl <= actualAngl and elementDist >= actualDist - dec_dist and elementDist <= actualDist + dec_dist:
                                values.insert(i, element);
                                drap = 1;
                         #Fin de la boucle range
        
                    #Fin de la boucle values
                if drap == 0:
                    tmp_lst = [];
                    tmp_lst.append(element);
                    result_lst.append(tmp_lst);              
                      
                drap = 0;
                #Fin de la boucle element                    
                
                
                
            #Résultat objts:
            #print(result_lst[5]);
            #print(len(result_lst));
            
            tabColor = [];
            tabForce = [];
            
            #end = time.time();
            
            
            #Ajout du tableau de couleur avec la réprésentation des poids:
            
            coefDistance = 5;
            coefTaille = 3.5;
            
            for i in range(len(result_lst)):
                objLen = len(result_lst[i]);
                distanceMin = result_lst[i][0][1];
                for j in range(objLen):
                    if result_lst[i][j][1] <= distanceMin:
                        distanceMin = result_lst[i][j][1];
                tabForce.append(objLen* coefTaille + coefDistance * distanceMin);
                
            
            #print(tabForce)
            
            def Average(lst): 
                return sum(lst) / len(lst)
            
            #print(Average(tabForce))
            
            sortedPoints = tabForce.copy()
            sortedPoints.sort()
            
            if (len(sortedPoints) % 2 == 0):
               # even
               lowerQ = Average(sortedPoints[:int(len(sortedPoints)/2)])
               upperQ = Average(sortedPoints[int(len(sortedPoints)/2):])
            else:
               # odd
               lowerQ = Average(sortedPoints[:int(len(sortedPoints)/2)])  # same as even
               upperQ = Average(sortedPoints[int(len(sortedPoints)/2+1):])
            
            #print(lowerQ, "and :", upperQ)
            
            for element in tabForce:
                if element >= 0 and element < lowerQ:
                    tabColor.append('R')
                elif element >= lowerQ and element < upperQ:
                    tabColor.append('Y')
                else:
                    tabColor.append('G');
                    
                    
            #print(tabColor)
            self.lstOfObject = result_lst.copy()
            self.lstOfColor = tabColor.copy()
            
            
            os.remove("./save.csv");
        else:
            self.boolTraitement = 0;
        

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
