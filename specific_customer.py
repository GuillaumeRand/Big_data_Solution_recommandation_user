import pandas as pd
import numpy as np


# Importation des données
data = pd.read_csv('KaDo.csv')
df_client = pd.DataFrame()

def init_df_client(customer_id):
    global df_client
    df_client = data[data["CLI_ID"] == int(customer_id)]


def top_10_clients():

    # Grouper les données en fonction de l'ID du client et compter le nombre de ventes par client
    grouped_data = data.groupby(['CLI_ID']).size().reset_index(name='counts')

    # Trier les données en fonction du nombre de ventes par client
    grouped_data = grouped_data.sort_values(by='counts', ascending=False).reset_index(drop=True)

    # Sélectionner les 10 premières lignes (correspondant aux 10 clients avec le plus d'achats)
    return grouped_data.head(10)


def cross_sales(customer_id):
    # Récupère les produits achetés par le client
    bought_products = df_client.drop_duplicates(subset=['LIBELLE'], ignore_index=True)['LIBELLE']
    df_result = pd.DataFrame(0, index=bought_products, columns=bought_products)
    # Group ticket to search potential cross sales
    df_tickets = df_client.groupby("TICKET_ID")

    for product in bought_products:
        for ticket in df_tickets:
            prod_arr = np.array(ticket[1].LIBELLE)

            # Check if product was bought in currently order
            if np.isin(prod_arr, product).any() == 'false' :
                continue
            
            # Delete product on which we are searching cross sales
            prod_arr = np.delete(prod_arr, np.where(prod_arr == product))
            for l in prod_arr:
                df_result[product][l] = df_result[product][l] + 1

    return df_result


def customer_purchases_by_month(customer_id):

    # Groupby sur la colonne "MOIS_VENTE" et la colonne "CLI_ID" pour obtenir les dépenses totales par mois et client
    df_grouped_month = data.groupby(['MOIS_VENTE', 'CLI_ID'])['PRIX_NET'].sum().reset_index()

    # Filtrer les données pour un seul client
    df_filtered_month = df_grouped_month[df_grouped_month['CLI_ID'] == int(customer_id)]

    # Retourner les données
    return df_filtered_month


def customer_purchases_evol(customer_id):

    # Filtrer les données pour un seul client
    df_filtered = data[data['CLI_ID'] == int(customer_id)]

    # Groupby sur la colonne "MOIS_VENTE" et la colonne "CLI_ID" pour obtenir les dépenses totales par mois et client
    df_grouped = df_filtered.groupby(['MOIS_VENTE', 'CLI_ID'])['PRIX_NET'].sum().reset_index()

    # Retourner les données
    return df_grouped


def customer_purchases_by_category(customer_id):

    # Filtrer les données pour un seul client
    df_filtered = data[data['CLI_ID'] == int(customer_id)]

    # Groupby sur la colonne "FAMILLE" et la colonne "CLI_ID" pour obtenir les dépenses totales par catégorie et client
    df_grouped_by_category = df_filtered.groupby('FAMILLE').mean()
    df_mean = df_grouped_by_category['PRIX_NET']

    # Retourner les données
    return df_mean


def average_price_by_ticket(customer_id):

    # Filtrer les données pour un seul client
    df_filtered = data[data['CLI_ID'] == int(customer_id)]

    # Groupby sur la colonne "TICKET_ID" et la colonne "CLI_ID" pour obtenir les dépenses totales par ticket et client
    df_grouped = df_filtered.groupby(['TICKET_ID', 'CLI_ID'])['PRIX_NET'].sum().reset_index()

    # Calculer la moyenne des dépenses par ticket
    average = df_grouped['PRIX_NET'].mean()

    # Retourner la moyenne
    return average


def most_bought_products(customer_id):

    # Filtrer les données pour un seul client
    df_filtered = data[data['CLI_ID'] == int(customer_id)]

    # Groupby sur la colonne "LIBELLE" et la colonne "CLI_ID" pour obtenir le nombre d'achats par produit et client
    df_grouped = df_filtered.groupby(['LIBELLE']).size().reset_index(name='counts')

    # Trier les données en fonction du nombre d'achats par produit et client
    df_sorted = df_grouped.sort_values(by='counts', ascending=False).reset_index(drop=True)

    # Sélectionner les 10 premières lignes (correspondant aux produits les plus achetés)
    most_bought = df_sorted.head(10)

    # Retourner les produits les plus achetés
    return most_bought
