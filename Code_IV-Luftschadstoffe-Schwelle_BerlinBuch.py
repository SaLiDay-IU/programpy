#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 15:25:10 2025

@author: sarah

Dieses Skript analysiert Luftschadstoffwerte an warmen Tagen (ab einer definierten 
Temperaturschwelle größer/gleich 20° Celsius) und stellt diese grafisch dar.
"""
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates


# Pfad zur CSV-Datei
csv_dateipfad = "/home/sarah/Dokumente/IU_Akademie/Code/Wetterdaten_merge_BerlinBuch"

# CSV-Datei laden
df = pd.read_csv(csv_dateipfad, sep=None, engine='python')
#  Entfernt überflüssige Leerzeichen in den Spaltennamen
df.columns = df.columns.str.strip() 

# Wandelt die Spalte 'MESS_DATUM' in ein Datumsformat um
df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'].astype(str).str.replace('.0', '', regex=False))

# Konvertiert Ozonwerte in numerische Werte
df['Ozon'] = pd.to_numeric(df['Ozon'], errors='coerce')

# Definition heißer Tage (ab 20 °C Tagesmitteltemperatur)
schwelle = 20

# Filtert DataFrame auf definierte heiße Tage (schwelle)
heisse_tage = df[df['TMK'] >= schwelle]

# Grafikformat mit definierter Größe
plt.figure(figsize=(16,8))

# Streudiagramme für verschiedene Luftschadstoffe an heißen Tagen

# Ozonwerte in blau
plt.scatter(heisse_tage['MESS_DATUM'], heisse_tage['Ozon'], label='Ozon (µg/m³)', color='tab:blue')
# Feinstaub PM10 in orange
plt.scatter(heisse_tage['MESS_DATUM'], heisse_tage['PM₁₀'], label='PM10 (µg/m³)', color='tab:orange')
# Feinstaub PM2.5 in grün
plt.scatter(heisse_tage['MESS_DATUM'], heisse_tage['PM₂,₅'], label='PM2.5 (µg/m³)', color='tab:green')
# Stickstoffdioxid in rot 
plt.scatter(heisse_tage['MESS_DATUM'], heisse_tage['NO₂'], label='NO2 (µg/m³)', color='tab:red')

# Achsenbeschriftung und Titel
plt.xlabel('Datum')
plt.ylabel('Konzentration (µg/m³)')
plt.title(f'Luftschadstoffe an heißen Tagen in 2024 & 2025 (TMK ≥ {schwelle} °C)')

# Legende und Raster
plt.legend()
plt.grid(True)

# Datumsformat auf der x-Achse anpassen: Jahr-Monat
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator())       # Jeden Monat eine Markierung
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format: Jahr-Monat

# Layout anpassen 
plt.tight_layout()

# Diagramm anzeigen 
plt.show()