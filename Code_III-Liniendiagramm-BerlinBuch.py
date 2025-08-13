
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 14:45:46 2025

@author: sarah

Dieses Skript lädt Wetter- und Ozonmessdaten, verarbeitet sie und visualisiert
den Verlauf der Tagesmitteltemperatur sowie der Ozonwerte über die Zeit.

"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Pfad zur CSV-Datei 
csv_dateipfad = "/home/sarah/Dokumente/IU_Akademie/Code/Wetterdaten_merge_BerlinBuch"

# CSV-Datei laden
df = pd.read_csv(csv_dateipfad, sep=None, engine='python')

# Entfernt überflüssige Leerzeichen aus den Spaltennamen
df.columns = df.columns.str.strip() 


# Ersten Einträge anzeigen
# print(df.head())


# Konvertiert die Spalte 'MESS_DATUM' in ein Datumsformat
df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'].astype(str).str.replace('.0', '', regex=False))


# Ozon-Spalte wird in numerische Werte konvertiert
df['Ozon'] = pd.to_numeric(df['Ozon'], errors='coerce')

# Visualisierung 
plt.figure(figsize=(16,8))
# Linie für Tagesmitteltemperatur zeichnen
plt.plot(df['MESS_DATUM'], df['TMK'], label='Tagesmitteltemperatur', color='tab:red')


# Linie für Ozonwerte zeichnen 
plt.plot(df['MESS_DATUM'], df['Ozon'], label='Tagesmittel Ozon (µg/m³)', color='tab:blue')

# Titel und Achsenbeschriftung setzen 
plt.title('Tagesmitteltemperatur und Ozon Verlauf')
plt.xlabel('Datum')
plt.ylabel('Werte')

# Y-Achse in 5er Schritten
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))  
# Raster wird eingeblendet
plt.grid(True)
# Legende
plt.legend()
# Layout anpassen 
plt.tight_layout()
# Diagramm anzeigen 
plt.show()
