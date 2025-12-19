import sys
from datetime import datetime
from contextlib import ExitStack

# === Partie 1 : Classe ConnectionManager ===
class ConnectionManager:
    def __init__(self, service_name):
        self.service_name = service_name

    def __enter__(self):
        # Simulation de l'établissement de connexion
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [Conn] Connexion à {self.service_name} établie.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Ce code s'exécute toujours, erreur ou pas
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [Conn] Déconnexion de {self.service_name}.")
        
        # Gestion de l'erreur si elle existe
        if exc_type:
            print(f" -> Erreur détectée et gérée dans __exit__ : {exc_type.__name__} — {exc_value}")
        
        # Retourner False propage l'erreur (le comportement par défaut). 
        # Retourner True supprimerait l'erreur.
        return False

def main():
    log_filename = "log.txt"

    print("=== Partie 2 : Composition avec ExitStack (Cas nominal) ===")
    
    with ExitStack() as stack:
        # Ouverture du fichier de log
        log = stack.enter_context(open(log_filename, "a"))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [File] Fichier {log_filename} ouvert.")
        
        # Ouverture de la connexion
        conn = stack.enter_context(ConnectionManager("Serveur X"))
        
        # Action
        msg = f"[{datetime.now()}] Tâche effectuée sur {conn.service_name}\n"
        log.write(msg)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [Acti] Log écrit : {msg.strip()}")

    print("\n" + "-"*50 + "\n")

    print("=== Partie 3 : Simulation d'erreur et nettoyage ===")
    
    try:
        with ExitStack() as stack:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [Init] Initialisation de la pile (Stack)...")
            
            log = stack.enter_context(open(log_filename, "a"))
            conn = stack.enter_context(ConnectionManager("Base Y"))
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [Acti] Tentative de traitement critique...")
            
            # Simulation de l'erreur
            raise RuntimeError("Erreur de traitement critique !")
            
            # Cette ligne ne sera jamais atteinte
            log.write("Ceci ne sera pas écrit.\n")

    except RuntimeError as e:
        print(f"\n[Main] Exception attrapée dans le bloc principal : {e}")

    print("\n" + "-"*50 + "\n")
    
    print("=== Vérification du fichier log ===")
    try:
        with open(log_filename, "r") as f:
            print(f"Contenu de {log_filename} :")
            print(f.read())
    except FileNotFoundError:
        print("Fichier log introuvable.")

if __name__ == "__main__":
    main()