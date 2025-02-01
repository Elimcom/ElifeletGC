import sqlite3
import pandas as pd
import streamlit as st

# Connexion à la base de données SQLite
conn = sqlite3.connect('invitations.db')

# Exécuter la requête SQL pour récupérer toutes les inscriptions
query = "SELECT * FROM inscriptions"
df = pd.read_sql_query(query, conn)

# Afficher les résultats dans Streamlit
st.write("Liste des inscriptions :")
st.dataframe(df)  # Affiche sous forme de tableau interactif

# Fermer la connexion à la base de données
conn.close()
