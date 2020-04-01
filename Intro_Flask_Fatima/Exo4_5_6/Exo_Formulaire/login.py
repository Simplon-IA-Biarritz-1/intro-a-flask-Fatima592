from flask import Flask, render_template, request

app = Flask(__name__)

# fonction qui renvoi le contenu du template test-formaulaire.html 
@app.route("/")
def home():
    return render_template('test-formulaire.html')

# fonction qui récupère les donnée saisie dans test-formulaire
# et qui renvoi le contenue du template page_suivante.html
@app.route("/", methods=["POST"]) 
def text_box():  
    nom = request.form["nom"].upper()
    prenom = request.form["prenom"].upper()
    pseudo = request.form["pseudo"]

    genre = " "
    if request.form.get("Monsieur") == "Monsieur":
        genre += "Mr"
        
    if request.form.get("Madame") == "Madame":
        genre += "Mme"
    
    perso = genre + " " + nom + " " + prenom + " alias " + pseudo

    return render_template("page_suivante.html", message=perso)

if __name__=="__main__":
    app.run(debug=True)

# récupération des données saisies
# ajout des données saisies dans une table "users"
import mysql.connector

# ouvrir une connection
mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="formulaire"
    )

mycursor = mydatabase.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS formulaire")

mycursor.execute("USE formulaire") 
mycursor = mydatabase.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, prénoms VARCHAR(100), noms VARCHAR(100), genre BIT(1), pseudo VARCHAR(100))")

mydatabase.commit()

# fonction qui récupère les donnée saisie pour les insérer dans la table users
@app.route("/", methods=["POST"])

def formulaire():
    nom = request.form["nom"].upper()
    prenom = request.form["prenom"].upper()
    pseudo = request.form["pseudo"]
    genre = " "
    if request.form.get("Monsieur") == "Monsieur":
        genre += True    
    if request.form.get("Madame") == "Madame":
        genre += False
    
    sql = "INSERT INTO users (prénoms,noms, genre, pseudo) VALUES()"
    val = [
        (prenom, nom, genre, pseudo)
    ]
    mycursor.execute(sql, val)
    mydatabase.commit

if __name__=="__main__":
    app.run(debug=True)

# fermer la connection
mydatabase.close()    