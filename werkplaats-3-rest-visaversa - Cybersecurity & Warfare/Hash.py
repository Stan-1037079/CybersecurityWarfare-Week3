import sqlite3
import hashlib

conn = sqlite3.connect('Database.db')  
cursor = conn.cursor()

cursor.execute("SELECT persoon_id, password FROM personen")
gebruikers = cursor.fetchall()

for gebruiker in gebruikers:
    persoon_id, wachtwoord = gebruiker

    if wachtwoord:
        gehasht_wachtwoord = hashlib.sha256(wachtwoord.encode()).hexdigest()

        cursor.execute("UPDATE personen SET password = ? WHERE persoon_id = ?", (gehasht_wachtwoord, persoon_id))

conn.commit()
conn.close()








