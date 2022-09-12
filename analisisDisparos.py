# Objetivo: Utilizando las coordenadas del campo desde la que un jugador ha realizado un disparo a porteria, analizar la finalización de cada jugador y mostrar los resultados en un cuadro de mando de PowerBi
# Se replica dos veces el mismo código para diferenciar los disparos de cada equipo y de sus respectivos jugadores.

import re
import pandas as pd
import numpy as np
import traceback
import matplotlib.pyplot as plt

df = pd.read_csv("./Disparos_2019-2020.csv",encoding='utf-8')

#Creamos un df1 con las columnas necesarias, filtramos equipos liga española, situacion de juego normal y borramos gol en propia

df1 = df[['result','X','Y','player','h_a','situation','shotType','h_team','a_team','lastAction']]

df2 = df1[(df1.h_team == 'Alaves') | (df1.h_team == 'Athletic Club') | (df1.h_team == 'Atletico Madrid') | (df1.h_team == 'Barcelona') 
  | (df1.h_team == 'Real Betis') | (df1.h_team == 'Celta Vigo') | (df1.h_team == 'Eibar')| (df1.h_team == 'Espanyol')
  | (df1.h_team == 'Getafe') | (df1.h_team == 'Granada') | (df1.h_team == 'Leganes') | (df1.h_team == 'Levante')
  | (df1.h_team == 'Mallorca') | (df1.h_team == 'Osasuna') | (df1.h_team == 'Real Sociedad') | (df1.h_team == 'Real Madrid')
  | (df1.h_team == 'Real Valladolid') | (df1.h_team == 'Sevilla') | (df1.h_team == 'Valencia') | (df1.h_team == 'Villarreal')]

df2 = df2[df2['situation'] == "OpenPlay"]
df2 = df2[df2.result != 'OwnGoal']

#Añadimos la columna equipo para agrupar todo y borramos las columnas que ya no queremos
df2['Equipo'] = np.where(df2.h_a == 'h',df2.h_team,df2.a_team)
df2 = df2.drop(columns=['a_team'])
df2 = df2.sort_values('Equipo')
df3 = df2

#Pasamos a valor sobre 100
df3.X = (df3.X *100)
df3.Y = (df3.Y *100)


#Establecemos cada una de las zonas del campo mediante el uso de coordenadas.
def get_status(df3):
    if  (66.66>=df3['X']<75.00) & (0.00<=df3['Y']<20.00):
        return 1
    elif (66.66>=df3['X']<75.00) & (20.00<=df3['Y']<40.00):
        return 2
    elif (66.66>=df3['X']<75.00) & (40.00<=df3['Y']<60.00):
        return 3
    elif (66.66>=df3['X']<75.00) & (60.00<=df3['Y']<80.00):
        return 4
    elif (66.66>=df3['X']<75.00) & (80.00<=df3['Y']<100.00):
        return 5
    elif (75.00<=df3['X']<83.33) & (0.00<=df3['Y']<20.00):
        return 6
    elif (75.00<=df3['X']<83.33) & (20.00<=df3['Y']<40.00):
        return 7
    elif (75.00<=df3['X']<83.33) & (40.00<=df3['Y']<60.00):
        return 8
    elif (75.00<=df3['X']<83.33) & (60.00<=df3['Y']<80.00):
        return 9
    elif (75.00<=df3['X']<83.33) & (80.00<=df3['Y']<100.00):
        return 10
    elif (83.33<=df3['X']<91.66) & (0.00<=df3['Y']<20.00):
        return 11
    elif (83.33<=df3['X']<91.66) & (20.00<=df3['Y']<40.00):
        return 12
    elif (83.33<=df3['X']<91.66) & (40.00<=df3['Y']<60.00):
        return 13
    elif (83.33<=df3['X']<91.66) & (60.00<=df3['Y']<80.00):
        return 14
    elif (83.33<=df3['X']<91.66) & (80.00<=df3['Y']<100.00):
        return 15
    elif (91.66<=df3['X']<100.00) & (0.00<=df3['Y']<20.00):
        return 16
    elif (91.66<=df3['X']<100.00) & (20.00<=df3['Y']<40.00):
        return 17
    elif (91.66<=df3['X']<100.00) & (40.00<=df3['Y']<60.00):
        return 18
    elif (91.66<=df3['X']<100.00) & (60.00<=df3['Y']<80.00):
        return 19
    elif (91.66<=df3['X']<100.00) & (80.00<=df3['Y']<100.00):
        return 20
    else:
        return -1

df3['Zona'] = df3.apply(get_status, axis = 1)

#Borramos columnas innecesarias
df3 = df3.drop(columns=['h_a','h_team','X','Y'])
df3 = df3[df3['Zona'] != -1]


#Creamos nuevas columnas con el resultado y porcentaje de cada disparo.
df3['Fuera'] = np.where(df3['result'] == 'MissedShots',1,0)
df3['Bloqueado'] = np.where(df3['result'] == 'BlockedShot',1,0)
df3['Parado'] = np.where(df3['result'] == 'SavedShot',1,0)
df3['Gol'] = np.where(df3['result'] == 'Goal',1,0)
df3['Palo'] = np.where(df3['result'] == 'ShotOnPost',1,0)
df3['TirosTotales'] = 1
df4 = df3.groupby(['Equipo','Zona']).agg(np.sum)
df4['%Gol'] = ((df4['Gol']/df4['TirosTotales'])*100).round(2)
df4['%Fuera'] = ((df4['Fuera']/df4['TirosTotales'])*100).round(2)
df4['%Bloqueado'] = ((df4['Bloqueado']/df4['TirosTotales'])*100).round(2)
df4['%Palo'] = ((df4['Palo']/df4['TirosTotales'])*100).round(2)
df4['%Parado'] = ((df4['Parado']/df4['TirosTotales'])*100).round(2)
#df4.to_csv('bloque1EquiposV2.csv')


df5 = df3.groupby(['player','Zona','Equipo']).agg(np.sum)
df5['%Fuera'] = ((df5['Fuera']/df5['TirosTotales'])*100).round(2)
df5['%Bloqueado'] = ((df5['Bloqueado']/df5['TirosTotales'])*100).round(2)
df5['%Parado'] = ((df5['Parado']/df5['TirosTotales'])*100).round(2)
df5['%Gol'] = ((df5['Gol']/df5['TirosTotales'])*100).round(2)
df5['%Palo'] = ((df5['Palo']/df5['TirosTotales'])*100).round(2)
#df5.to_csv('bloque2JugadoresV2.csv',encoding='utf-8-sig')

#Análisis de equipos
df6 = df[['result','X','Y','h_a','situation','shotType','h_team','a_team','h_goals','a_goals']]
df7 = df6[(df1.h_team == 'Alaves') | (df6.h_team == 'Athletic Club') | (df6.h_team == 'Atletico Madrid') | (df6.h_team == 'Barcelona') 
  | (df6.h_team == 'Real Betis') | (df6.h_team == 'Celta Vigo') | (df6.h_team == 'Eibar')| (df6.h_team == 'Espanyol')
  | (df6.h_team == 'Getafe') | (df6.h_team == 'Granada') | (df6.h_team == 'Leganes') | (df6.h_team == 'Levante')
  | (df6.h_team == 'Mallorca') | (df6.h_team == 'Osasuna') | (df6.h_team == 'Real Sociedad') | (df6.h_team == 'Real Madrid')
  | (df6.h_team == 'Real Valladolid') | (df6.h_team == 'Sevilla') | (df6.h_team == 'Valencia') | (df6.h_team == 'Villarreal')]

df7 = df7[df7['situation'] == "OpenPlay"]
df7 = df7[df7.result != 'OwnGoal']

#Pasamos a valor sobre 100
df7.X = (df7.X *100)
df7.Y = (df7.Y *100)


def get_status(df7):
    if  (66.66>=df7['X']<75.00) & (0.00<=df7['Y']<20.00):
        return 1
    elif (66.66>=df7['X']<75.00) & (20.00<=df7['Y']<40.00):
        return 2
    elif (66.66>=df7['X']<75.00) & (40.00<=df7['Y']<60.00):
        return 3
    elif (66.66>=df7['X']<75.00) & (60.00<=df7['Y']<80.00):
        return 4
    elif (66.66>=df7['X']<75.00) & (80.00<=df7['Y']<100.00):
        return 5
    elif (75.00<=df7['X']<83.33) & (0.00<=df7['Y']<20.00):
        return 6
    elif (75.00<=df7['X']<83.33) & (20.00<=df7['Y']<40.00):
        return 7
    elif (75.00<=df7['X']<83.33) & (40.00<=df7['Y']<60.00):
        return 8
    elif (75.00<=df7['X']<83.33) & (60.00<=df7['Y']<80.00):
        return 9
    elif (75.00<=df7['X']<83.33) & (80.00<=df7['Y']<100.00):
        return 10
    elif (83.33<=df7['X']<91.66) & (0.00<=df7['Y']<20.00):
        return 11
    elif (83.33<=df7['X']<91.66) & (20.00<=df7['Y']<40.00):
        return 12
    elif (83.33<=df7['X']<91.66) & (40.00<=df7['Y']<60.00):
        return 13
    elif (83.33<=df7['X']<91.66) & (60.00<=df7['Y']<80.00):
        return 14
    elif (83.33<=df7['X']<91.66) & (80.00<=df7['Y']<100.00):
        return 15
    elif (91.66<=df7['X']<100.00) & (0.00<=df7['Y']<20.00):
        return 16
    elif (91.66<=df7['X']<100.00) & (20.00<=df7['Y']<40.00):
        return 17
    elif (91.66<=df7['X']<100.00) & (40.00<=df7['Y']<60.00):
        return 18
    elif (91.66<=df7['X']<100.00) & (60.00<=df7['Y']<80.00):
        return 19
    elif (91.66<=df7['X']<100.00) & (80.00<=df7['Y']<100.00):
        return 20
    else:
        return -1

df7['Zona'] = df7.apply(get_status, axis = 1)
df7 = df7[df7['Zona'] != -1]
df7 = df7.drop(columns=['situation','shotType','X','Y'])

df7['Fuera'] = np.where(df7['result'] == 'MissedShots',1,0)
df7['Bloqueado'] = np.where(df7['result'] == 'BlockedShot',1,0)
df7['Parado'] = np.where(df7['result'] == 'SavedShot',1,0)
df7['Gol'] = np.where(df7['result'] == 'Goal',1,0)
df7['Palo'] = np.where(df7['result'] == 'ShotOnPost',1,0)
df7['TirosTotales'] = 1
#df4.to_csv('bloque1EquiposV2.csv')


df7['Resultado'] = np.where(df7['h_goals']==df7['a_goals'],'E',np.where((df7['h_goals']>=df7['a_goals']) 
    & (df7['h_a']=='h'),'V',np.where((df7['h_goals']>=df7['a_goals']) 
    & (df7['h_a']=='a'),'D',np.where((df7['a_goals']>=df7['h_goals']) 
    & (df7['h_a']=='h'),'D','V'))))
#df7 = df7.drop(columns=['h_goals','a_goals'])

df7['Equipo'] = np.where(df7.h_a == 'h',df7.h_team,df7.a_team)
df7 = df7.drop(columns=['h_a','h_team','a_team','h_goals','a_goals'])

df8 = df7.groupby(['Equipo','Zona','Resultado']).agg(np.sum)
df8['%Gol'] = ((df8['Gol']/df8['TirosTotales'])*100).round(2)
df8['%Fuera'] = ((df8['Fuera']/df8['TirosTotales'])*100).round(2)
df8['%Bloqueado'] = ((df8['Bloqueado']/df8['TirosTotales'])*100).round(2)
df8['%Palo'] = ((df8['Palo']/df8['TirosTotales'])*100).round(2)
df8['%Parado'] = ((df8['Parado']/df8['TirosTotales'])*100).round(2)
df8.to_csv('bloque3resultados.csv',encoding='utf-8-sig')


