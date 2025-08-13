#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 12:55:28 2025

@author: sarah

Dieses Skript kombiniert stündliche Ozonmessungen von mehreren CSV-Dateien,
korrigiert ungewöhnliche Zeitangaben („24:00“), berechnet Monatsdurchschnittswerte
pro Messstation für 2024 und visualisiert diese als Heatmap.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import calendar

# Pfad zu dem Ordner mit den CSV-Dateien 
verzeichnis =  Path("/home/sarah/Dokumente/IU_Akademie/Code/heatmap")

# Liste zur Speicherung aller DataFrames
alle_daten = []

def fix_24h_time(dt_str):
    """
     Korrigiert Zeitangaben mit "24:00", indem ein Tag hinzugerechnet wird und die Uhrzeit auf 00:00 gesetzt wird.
     Wenn der Eintrag kein String ist oder kein "24:00" enthält, wird pd.to_datetime verwendet.
   """
    if isinstance(dt_str, str):
        if "24:00" in dt_str:
            date_part = dt_str.split(" ")[0]
            date = pd.to_datetime(date_part, format="%d.%m.%Y") + pd.Timedelta(days=1)
            return date.replace(hour=0, minute=0)
        else:
            return pd.to_datetime(dt_str, format="%d.%m.%Y %H:%M")
    else:
        return pd.NaT

# Liest die CSV-Dateien im Ordner ein 
for datei in verzeichnis.glob("*.csv"):
    df = pd.read_csv(datei, 
                     sep=';',           # Semikolon als Spaltentrenner
                     decimal=',',       # Dezimaltrennzeichen ist Komma
                     encoding='utf-8', 
                     on_bad_lines='skip'  # fehlerhafte Zeilen werden übersprungen
) 
    # Datumswerte bereinigen und korrigieren
    df['Datum'] = df['Datum'].str.strip("'").apply(fix_24h_time)
    # DataFrame zur Liste hinzufügen
    alle_daten.append(df) 
    
   
df = pd.concat(alle_daten, ignore_index=True) # Daten werden zusammengeführt 

df = df.rename(columns={"Ozon (O₃) Ein-Stunden-Mittelwert in µg/m³": "ozon"}) #  Spaltenname wird umbenannt 

df['ozon'] = pd.to_numeric(df['ozon'], errors='coerce') # Werte als nummeriche Werte umgewandelt 


df['jahr'] = df['Datum'].dt.year # Spalte Jahr
df['monat'] = df['Datum'].dt.month # Spalte Monat


# Codes der Stationen werden in ihre jeweiligen Städte umbenannt
df['Stationscode'] = df['Stationscode'].replace({
        'DEBW076' : 'Baden-Baden',
        'DENW059' : 'Koeln-RK',
        'DEBW009' : 'Heidelberg',
        'DETH041' : 'Jena',
        'DENW114' : 'Wuppertal',
        'DENI062' : 'Lueneburger-Heide'})


df_2024 = df[df['jahr'] == 2024] # Filtert nur Werte für das Jahr 2024


# print("Verfügbare Stationen:", df_2024['Stationscode'].unique())

# Mittlere Ozonwerte pro Station & Monat berechnen und tabellarisch aufbereiten
monatsmittel_station = (
    df_2024
    .groupby(['Stationscode', 'monat'])['ozon']
    .mean().
    unstack()
)
# Monatsnamen (statt Zahlen) als Spaltenbezeichnungen
monatsmittel_station.columns = [
    calendar.month_name[int(m)] for m in monatsmittel_station.columns
] 

# Heatmap plotten - Die Farbe zeigt den Ozonmittelwert 
plt.figure(figsize=(12, 8))
sns.heatmap(monatsmittel_station, 
            annot=True,          # Werte in Heatmap-Zellen anzeigen
            fmt=".1f",           # Format mit einer Nachkommastelle 
            cmap="rainbow",      # Farbkarte 
            cbar_kws={'label': 'Ozon (µg/m³)'} # Beschriftung der Farblegende 
)
plt.title("Monatliche Durchschnittswerte der Ozonkonzentration im Jahr 2024")
plt.xlabel("Monat")
plt.ylabel("Städte")
plt.tight_layout()
plt.show()