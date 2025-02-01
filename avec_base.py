import streamlit as st
import pandas as pd
from fpdf import FPDF
import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('invitations.db')
cursor = conn.cursor()

# Créer une table si elle n'existe pas déjà
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        church TEXT,
        training TEXT,
        source TEXT
    )
''')
conn.commit()

# Fonction pour générer la carte d'invitation
def generate_invitation(name, church, training, source):
    if not name or not church:
        st.warning("Veuillez remplir tous les champs.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Invitation au Concert d'Evangelisation", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Cher/Chère {name},", ln=True, align='L')
    pdf.cell(200, 10, txt="Vous êtes cordialement invité(e) au concert d'évangélisation", ln=True, align='L')
    pdf.cell(200, 10, txt="et à participer à l'enseignement pastoral.", ln=True, align='L')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Eglise de provenance : {church}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Formation pastorale : {training}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Lien obtenu via : {source}", ln=True, align='L')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Détails de l'événement :", ln=True, align='L')
    pdf.cell(200, 10, txt="Date : 15 août 2024", ln=True, align='L')
    pdf.cell(200, 10, txt="Heure : 18h00", ln=True, align='L')
    pdf.cell(200, 10, txt="Lieu : Église Centrale, 123 Rue de la Foi, Paris", ln=True, align='L')

    # Sauvegarde le PDF
    file_name = f"Invitation_{name.replace(' ', '_')}.pdf"
    pdf.output(file_name)

    # Enregistrer dans la base de données
    cursor.execute('''
        INSERT INTO inscriptions (name, church, training, source)
        VALUES (?, ?, ?, ?)
    ''', (name, church, training, source))
    conn.commit()

    return file_name

# Interface avec Streamlit
st.title("Formulaire d'Invitation")

# Champs du formulaire
name = st.text_input("Nom et Prénoms")
church = st.text_input("Eglise de provenance")
training = st.selectbox("Formation pastorale", ["Oui", "Non"])
source = st.selectbox("De quelle façon avez-vous eu ce lien ?", ["Sur Facebook", "Par courriel", "Par le biais d'un(e) ami(e) sur WhatsApp", "Autres"])

# Bouton pour générer la carte d'invitation
if st.button("Générer la carte d'invitation"):
    file_name = generate_invitation(name, church, training, source)
    if file_name:
        st.success(f"Invitation pour {name} générée avec succès!")
        with open(file_name, "rb") as file:
            st.download_button("Télécharger l'invitation", file, file_name)

# Afficher les inscriptions
st.subheader("Liste des inscriptions")
df = pd.read_sql_query("SELECT * FROM inscriptions", conn)
st.write(df)

