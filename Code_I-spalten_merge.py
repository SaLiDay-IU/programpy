#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 21:06:44 2025

@author: sarah


Dieses Skript führt historische und aktuelle Klimadaten des DWD zusammen.
Daten vor dem 01.01.2024 werden aus dem historischen Datensatz gefiltert,
anschließend mit den neueren Daten kombiniert und gespeichert.

"""
import pandas as pd

# Einlesen der CSV Dateien (historische und aktuelle DWD Klimadaten)
df_historical = pd.read_csv("/home/sarah/Dokumente/IU_Akademie/Code/produkt_klima_tag_19610101_20241231_00400.txt", sep=';')
df_recent = pd.read_csv("/home/sarah/Dokumente/IU_Akademie/Code/produkt_klima_tag_20240125_20250727_00400.txt", sep=';')


# Umwandlung der Datumswerte von Strings in datetime-Objekte
df_historical["MESS_DATUM"] = pd.to_datetime(df_historical["MESS_DATUM"], format='%Y%m%d')
df_recent["MESS_DATUM"] = pd.to_datetime(df_recent["MESS_DATUM"], format='%Y%m%d')


# Definition des Zeitbereichs, der aus dem historischen Datensatz übernommen werden soll 
startdatum = pd.to_datetime("20240101", format='%Y%m%d')
enddatum = pd.to_datetime("20240124", format='%Y%m%d')

# Filtern des historischen Datensatzes auf den definierten Zeitraum 
df_filtered = df_historical[
    (df_historical["MESS_DATUM"] >= startdatum) &
    (df_historical["MESS_DATUM"] <= enddatum)
]

# gefiltere Daten anzeigen 
#print(df_filtered)

# Zusammenführen der gefilterten historischen Daten mit den aktuellen Daten 
df_neu = pd.concat([df_filtered, df_recent], ignore_index=True)

# Speichern der zusammengeführten Daten als neue CSV-Datei
df_neu.to_csv("ZusammenfuehrenTemperaturdaten_DWD", index=False)

print("ready")


