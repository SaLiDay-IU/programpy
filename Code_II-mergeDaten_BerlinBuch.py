#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 22:05:16 2025

@author: sarah

Dieses Skript führt Temperaturdaten des DWD mit Ozon-Tagesmittelwerten zusammen.
Beide Datensätze werden über das Datum gematcht und als zusammengeführte Datei gespeichert.
"""
import pandas as pd

# Einlesen der DWD-Temperaturdaten
df_dwd_basis = pd.read_csv("/home/sarah/Dokumente/IU_Akademie/Code/ZusammenfuehrenTemperaturdaten_DWD", sep=",")
# Einlesen der Ozon-Tagesmittelwerte
df_dwd_new = pd.read_csv("ozon_tagesmittel_2025.csv")

# Entfernen von Leerzeichen in den Spaltennamen falls vorhanden 
df_dwd_basis.columns = df_dwd_basis.columns.str.strip()
df_dwd_new.columns = df_dwd_new.columns.str.strip()


# Zusammenführen beider Datensätze anhand des Datums
df_merged = pd.merge(
            df_dwd_basis, 
            df_dwd_new, 
            left_on="MESS_DATUM", 
            right_on="Tag", 
            how="left")


# Spalte "Tag" wird entfernt 
df_merged = df_merged.drop(columns=["Tag"], errors="ignore")

# Ergebnisse werden in einer neuen CSV-Datei zusammengefügt und gespeichert 
df_merged.to_csv("Wetterdaten_merge_BerlinBuch", index=False, float_format="%.1f")


print("Spalten erfolgreich hinzugefügt und gespeichert.")