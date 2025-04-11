
# Mein Vue.js Projekt mit Backend

## Vorbereitung

1. **Clone des Repositories**  
   Clone das Repository, um mit der Entwicklung zu beginnen.

2. **.env-Datei anlegen**  
   Erstelle eine `.env`-Datei im Stammverzeichnis deines Projekts. Beispielinhalt:

   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=Passwort123
   ```

   Achte darauf, die Werte in der `.env`-Datei an deine eigene Datenbankkonfiguration anzupassen.

## Schritte, um das Projekt auszuführen

### 1. MySQL-Datenbank starten und anmelden
   - Stelle sicher, dass deine MySQL-Datenbank läuft.
   - Melde dich mit einem MySQL-Client, z.B. **MySQL Workbench**, an und gib dort deinen **Datenbank-Benutzernamen** und **Passwort** ein.  
   - Achte darauf, dass die Datenbank erreichbar ist, sonst bekommst du einen Fehler.

### 2. Backend starten
   - Gehe in das Verzeichnis, in dem die Datei `Backend.py` liegt.
   - Führe die Datei `Backend.py` aus, um den Backend-Server zu starten.
   
   ```
   python Backend.py
   ```

### 3. Frontend starten (Vue.js)
   - Gehe in das Verzeichnis deines Vue.js-Frontends.
   - Installiere alle notwendigen Abhängigkeiten, falls noch nicht geschehen:

     ```
     npm install
     ```

   - Starte das Frontend mit dem folgenden Befehl:

     ```
     npm run dev
     ```


