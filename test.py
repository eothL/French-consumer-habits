import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Fonction 
def Ouverture(nom):
    '''
    ouvre un fichier csv dans le dossier datasets
    '''
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'datasets', f'{nom}.csv')
    print(f"Tentative d'ouverture du fichier : {file_path}")
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path, sep=';')
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier {file_path}: {e}")
            return None
    else:
        print(f"Le fichier {file_path} n'existe pas.")
        return None

# Afficher le répertoire courant
print(f"Répertoire de travail actuel : {os.getcwd()}")

# Ouverture des fichiers 
actphys_sd_df = Ouverture("actphys-sedent") # données activité physique sédentaire
app_nut_df = Ouverture("apports-nut-alim") # données apport nutriment alimentaire

# Afficher les premières lignes du DataFrame
if actphys_sd_df is not None:
    print(actphys_sd_df.head())
else:
    print("Le DataFrame actphys_sd_df est vide.")
