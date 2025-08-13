#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 12:42:47 2025

@author: sarah

# Dieses Skript liest Niederschlagsdaten (RSK) ein, filtert sie für das Jahr 2024 
und erstellt daraus ein interaktives Balkendiagramm im Browser (HTML) mit Bokeh

"""

import pandas as pd
from bokeh.plotting import figure, show, output_file


# Pfad zur CSV-Datei angeben
csv_dateipfad = "/home/sarah/Dokumente/IU_Akademie/Code/Wetterdaten_merge_BerlinBuch"

# CSV-Datei laden
df = pd.read_csv(csv_dateipfad, sep=None, engine='python')
# Entfernt überflüssige Leerzeichen an den Spaltennamen
df.columns = df.columns.str.strip() 

# Kovertiert Datumsspalte in datetime-Format
df['MESS_DATUM'] = pd.to_datetime(
    df['MESS_DATUM'].astype(str).str.replace('.0', '', regex=False)
)
# Konvertiert Niederschlagswerte (RSK) in numerische Werte und Fehler oder leere Werte werden als NaN markiert
df['RSK'] = pd.to_numeric(df['RSK'], errors='coerce')

# Datensatz wird auf das Jahr 2024 gefiltert
df_2024 = df[df['MESS_DATUM'].dt.year == 2024].copy()
# Entfernt Zeilen bei denen kein gültiger Niederschlagswert (RSK) vorhanden ist
df_2024.dropna(subset=['RSK'], inplace=True)
# Ausgabe-Datei spezifizieren
output_file("berlinbuchniederschlag.html")

# Bokeh Figur (interaktives Diagramm) wird erstellt 
plot = figure(
    x_axis_type="datetime",
    width=1000,
    height=500, 
    title="Niederschlag in Berlin-Buch für 2024",
    x_axis_label="Datum",
    y_axis_label="Niederschlag (mm)"
)
# vertikale Balken hinzufügen
plot.vbar(
    x=df_2024['MESS_DATUM'],
    top=df_2024['RSK'],
    width=0.8,
    legend_label="Niederschlag"
)

# erzeugten Plot im Browser anzeigen
show(plot)