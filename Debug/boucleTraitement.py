# -*- coding: utf-8 -*-
"""
TRAN Adrien

Premier test panda
"""

import pandas as pd
from pathlib import Path
import time
import os





#start = time.time();

while 1 == 1:
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
                        elif elementAngl >= actualAngl - dec and elementAngl <= actualAngl and actualDist >= actualDist - dec_dist and elementDist <= actualDist + dec_dist:
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
                tabColor.append('G')
            elif element >= lowerQ and element < upperQ:
                tabColor.append('Y')
            else:
                tabColor.append('R');
                
                
        print(tabColor)
        os.remove("./save.csv");
        
        
    
        #os.remove("./save.csv");
        
    

        