# Importation des bibliothèques nécessaires à l'execution du programme
import pandas as pd #traitement des données
import numpy as np 
import matplotlib.pyplot as plt #visualisation
import seaborn as sns #visualisation 
import os 

# fonction 
def ouverture(nom):
    '''ouvre un fichier csv dans un dossier local nommé datasets et retourne les données sous forme de dataframe pandas''' 

    # Obtenir le répertoire contenant le script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Contrsuire le chemin complet vers le fichier CSV 
    file_path = os.path.join(script_dir,'datasets', f'{nom}.csv')

    return (pd.read_csv(file_path,sep=';')) # Lire le fichier CSV avec une séparation ;

def ouverture_url(url):
    '''ouvre un fichier csv directement depuis le site et retourne les données sous forme de dataframe pandas'''

    try : # ouverture du fichier CSV 
        return (pd.io.parsers.read_csv(url, sep=';', low_memory=False)) # pd.io.parsers permet de récupérer directement les données sur le site et avec low_memory =False pour mieux identifier les types de données par colonne
    except FileNotFoundError as e :
        print(f"Erreur: le fichier CSV n'a pas pu être trouvé : {e}")
        return None
    except Exception as e :
        print(f"Erreur inconnue lors de l'ouverture du fichier : {e}")
        return None

# Récupération des données directement depuis le site de l'état avec des urls
liste_URL = [
    "https://www.data.gouv.fr/fr/datasets/r/e9a34b81-2105-4d82-a023-c14947fb2b2c", # 1. actphy-sedent
    "https://www.data.gouv.fr/fr/datasets/r/bffa997f-f92a-47ae-a669-e64fe91463c9", # 2. conso-compo-alim
    "https://www.data.gouv.fr/fr/datasets/r/76881e8e-e07c-44b6-915c-3a2b5cee4e0c", # 3. occasions
    "https://www.data.gouv.fr/fr/datasets/r/13550bb4-efd8-4e42-a913-35f3c93729d6", # 4. nomenclature
    "https://www.data.gouv.fr/fr/datasets/r/c88bf218-dcda-4f7a-b35a-eb6dc0fc5060", # 5. habitude menage
    "https://www.data.gouv.fr/fr/datasets/r/099351b9-e32e-4e38-8f23-dec21fd07c71", # 6. habitude indivuelle
    "https://www.data.gouv.fr/fr/datasets/r/32e79499-9897-423b-acd6-143121340f86", # 7. fréquentiel alimentaire fpq
    "https://www.data.gouv.fr/fr/datasets/r/f982ee4a-b2db-4608-ab95-bfe51dfc4897", # 8. description individuelle
    "https://www.data.gouv.fr/fr/datasets/r/7f520c93-f0ef-4e77-b5a5-1e0ef5855ac7", # 9. consommation par groupe
    "https://www.data.gouv.fr/fr/datasets/r/e7f48716-368f-48e1-a7c3-ea0638b0d6a7", # 10. apport nutri
    "https://www.data.gouv.fr/fr/datasets/r/90991f9a-0e54-40c4-a7cc-550d050d9360", # 11. conso complément alimentaire production 
    "https://www.data.gouv.fr/fr/datasets/r/337316a1-a224-456a-97b2-341a6a152793", # 12. conso CA indiv
    ]

# Chargement des données à partir des URLs
dataframes = []
for url in liste_URL:
    # On utilise la fonction ouverture_url pour récupérer les données directement depuis le site
    df = ouverture_url(url)
    if df is not None: # on vérifie que la liste n'est pas vide 
        dataframes.append(df)
    else: 
        print(f"l'url: {url} n'est pas bonne et n'as pas été ajouté à la liste")

# Nommage des DataFrames pour un accès plus facile pour la suite 
actphys_sd_df = dataframes[0] # donnée activité physique sédentaire
conso_compo_df = dataframes[1] # donnée composition alimentaire 
occas_df = dataframes[2] # donnée sur les occasions de consommation 
nomencl_df = dataframes[3] # donnée nomenclature nourriture 
habitude_menage_df = dataframes[4] # donnée habitude ménagère
habitude_indiv_df = dataframes[5] # donnée habitude individuelle
freq_alim_df = dataframes[6] # donnée fréquentiel alimentaire fpq
desc_indiv_df = dataframes[7] # donnée description individuelle
conso_groupe_df = dataframes[8] # donnée consommation par groupe
app_nut_df = dataframes[9] # donnée apport nutriment alimentaire
conso_comp_alim_prod_df = dataframes[10] # donnée consommation complément alimentaire production 
conso_ca_indiv_df = dataframes[11] # donnée consommation CA individuelle

# Nettoie les données
for df in dataframes : 
    # on enlève les colonnes dont le nombre de valeur nulle est supérieur à 99,5% car il n'y a pas assez de valeur pour que ce soit intéressant à analyser
    df.dropna(axis=1, thresh=int(len(df)*0.995)) 

# on va analyser habitude individuelle et ménager des français 
# Dictionnaires de mappage pour les différents formats permettant une meilleure compréhension en passant d'une échelle à un texte 
format_lieu_achat = {
    1: "Grandes surfaces",
    2: "Au marché",
    3: "Commerces de proximité",
    4: "N'achète jamais cet aliment",
    5: "Ne sait pas"
}

format_preference = {
    1: 'Beaucoup',
    2: 'Assez',
    3: 'Un peu',
    4: 'Pas du tout',
    5: 'Ne sait pas'
}

format_influence_achat = {
    1: 'Influence toujours',
    2: 'Parfois',
    3: 'Jamais',
    4: 'Ne lit jamais cette partie'
}

format_ouinon = {
    1: 'Oui',
    0: 'Non'
}

# Colonnes à analyser
colonne_analyser = [
    "aime_legumes", # utilise le format_preference
    'aime_fruits', # utilise le format_preference
    'etiquette_ingredients', # utilise le format_influence_achat
    'etiquette_contenu_nutri', # utilise le format_influence_achat
    'etiquette_portions', # utilise le format_influence_achat
    'etiquette_message_nutri', # utilise le format_influence_achat
    'lieu_achat_fruits_frais', # utilise le format_lieu_achat
    'choix_aliment_facilite_prepa', # format_ouinon
    'choix_aliment_mode_prod', # format_ouinon
    'choix_aliment_gout', # format_ouinon
    'choix_aliment_signe_quali', # format_ouinon
    'choix_aliment_compo_nutri', # format_ouinon
    'choix_aliment_ingredients', # format_ouinon
    'choix_aliment_prix' # format_ouinon,
    'FR_total_freq_M',
    'FR_fraise_ON',
    'FR_pomme_ON',
    'FR_peche_ON',
    'FR_melon_ON',
    'FR_pomme_ON',
    'FR_raisin_ON', # format_ouinon
    'FR_raisin_freq_M',
    'FR_fraise_freq_M',
    'FR_pomme_freq_M',
    'FR_peche_freq_M',
    'FR_melon_freq_M',
    'FR_pomme_freq_M',
]

# Mappage des formats
format_mapping = {
    "aime_legumes": format_preference,
    'aime_fruits': format_preference,
    'etiquette_ingredients': format_influence_achat,
    'etiquette_contenu_nutri': format_influence_achat,
    'etiquette_portions': format_influence_achat,
    'etiquette_message_nutri': format_influence_achat,
    'lieu_achat_fruits_frais': format_lieu_achat,
    'choix_aliment_facilite_prepa': format_ouinon,
    'choix_aliment_mode_prod': format_ouinon,
    'choix_aliment_gout': format_ouinon,
    'choix_aliment_signe_quali': format_ouinon,
    'choix_aliment_compo_nutri': format_ouinon,
    'choix_aliment_ingredients': format_ouinon,
    'choix_aliment_prix': format_ouinon,
    'FR_raisin_ON' : format_ouinon,
    'FR_fraise_ON' : format_ouinon,
    'FR_pomme_ON' : format_ouinon,
    'FR_peche_ON' : format_ouinon,
    'FR_melon_ON' : format_ouinon,
    'FR_pomme_ON': format_ouinon,
}

# Fonction pour remplacer les valeurs et tracer les histogrammes
def plot_column_distribution(df, column, mapping):
    # Remplacer les valeurs selon le mapping
    df[column] = df[column].replace(mapping)
    
    # Imprimer les valeurs uniques après le remplacement pour vérification
    print(f"Valeurs uniques après remplacement pour {column}: {df[column].unique()}")
    
    # créer une figure pour l'histogramme
    plt.figure(figsize=(10, 6))
    # Tracer l'histogramme des valeurs de la colonne, en omettant les valeurs manquantes (NaN)
    sns.histplot(df[column].dropna(), discrete=True)
    plt.title(f'Distribution de {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.xticks(rotation=45)


# # Tracer les distributions pour les colonnes à analyser
# for df in dataframes[4:8]:
#     print("Nouveau DataFrame:")
#     # Pour chaque colonne du DataFrame
#     for column in df.columns:
#         # Si la colonne fait partie des colonnes à analyser
#         if column in colonne_analyser:
#             print(f"Traitement de la colonne: {column}")
#             # Tracer la distribution de la colonne en utilisant le dictionnaire de mappage approprié
#             plot_column_distribution(df, column, format_mapping.get(column, {}))


# plt.show()

# Comparaison des fruits 
fruit_liste = [
    'FR_fraise_ON',
    'FR_pomme_ON',
    'FR_peche_ON',
    'FR_melon_ON',
    'FR_pomme_ON',
    'FR_raisin_ON'
    ]
def compare_fruit_consommation(df,fruit_liste):
    consommation_dict = { fruit :df[fruit].value_counts() for fruit in fruit_liste}
    consommation_df = pd.DataFrame(consommation_dict)
    consommation_df.plot(kind='bar', figsize=(14, 8))
    plt.title('Comparaison de la consommation de plusieurs fruits')
    plt.xlabel('Consommation')
    plt.ylabel('Nombre de personnes')
    plt.xticks(rotation=0)
    plt.legend(title='Fruits')
    plt.show()

compare_fruit_consommation(freq_alim_df,fruit_liste)


def compare_fruit_frequence(df, fruits):
    mean_frequence={fruit : df[fruit].mean() for fruit in fruits}

    #convertir en dataframe 
    mean_frequence_df = pd.DataFrame(list(mean_frequence.items()),columns = ['fruit', 'Mean frequency'])
 
    plt.figure(figsize=(14, 8))
    sns.barplot(x='Fruit', y='Mean Frequency', data=mean_frequence_df)
    plt.title('Comparaison des moyennes des fréquences de consommation des différents fruits')
    plt.xlabel('Fruit')
    plt.ylabel('Moyenne des fréquences de consommation')
    plt.xticks(rotation=45)
    plt.show()
    
    # Afficher les moyennes pour chaque fruit
    print(mean_frequencies_df)

fruit_freq_columns = [
    'FR_raisin_freq_M',
    'FR_fraise_freq_M',
    'FR_pomme_freq_M',
    'FR_peche_freq_M',
    'FR_melon_freq_M'
]

compare_fruit_frequence(freq_alim_df, fruit_freq_columns)
