import csv
import sys
from datetime import datetime
from pathlib import Path

# === Configuration ===
CSV_FILE = "operations.csv"
LOG_FILE = "journal.log"

# Création d'un fichier CSV factice pour l'exercice
def setup_environment():
    data = [
        ["user_update", "id=101"],
        ["data_sync", "source=api"],
        ["error_trigger", "simulate_crash"], # Pour tester la gestion d'erreur
        ["email_send", "admin@local"]
    ]
    with open(CSV_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["operation", "params"])
        writer.writerows(data)
    print(f"[Setup] Fichier '{CSV_FILE}' généré.")

# === Classe BatchProcessor ===
class BatchProcessor:
    def __init__(self, csv_filename, log_filename):
        self.csv_filename = csv_filename
        self.log_filename = log_filename
        self.csv_file = None
        self.log_file = None
        self.writer = None

    def _log(self, message):
        """Méthode helper pour écrire dans le log avec timestamp"""
        if self.log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_file.write(f"[{timestamp}] {message}\n")
            # Flush pour s'assurer que c'est écrit sur le disque immédiatement
            self.log_file.flush()

    def __enter__(self):
        try:
            # Ouverture des deux ressources
            self.csv_file = open(self.csv_filename, "r", newline='', encoding='utf-8')
            self.log_file = open(self.log_filename, "a", encoding='utf-8')
            
            self._log(f"SESSION START - Fichier source: {self.csv_filename}")
            return self
            
        except OSError as e:
            # Si l'ouverture échoue, on s'assure de ne rien laisser ouvert
            if self.csv_file: self.csv_file.close()
            if self.log_file: self.log_file.close()
            print(f"Erreur critique lors de l'ouverture des fichiers : {e}")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Gestion de la fermeture et des logs de fin
        if self.log_file:
            if exc_type:
                self._log(f"SESSION ERROR - Exception: {exc_type.__name__} -> {exc_val}")
            else:
                self._log("SESSION SUCCESS - Fin du traitement normal.")
            
            self.log_file.close()
            print("[BatchProcessor] Fichier journal fermé.")

        if self.csv_file:
            self.csv_file.close()
            print("[BatchProcessor] Fichier CSV fermé.")

        # On ne supprime pas l'exception (return False par défaut), 
        # pour que le programme principal sache qu'il y a eu un crash.
        return False

    def process(self):
        """Lit le CSV et simule le traitement"""
        reader = csv.reader(self.csv_file)
        next(reader, None) # Sauter l'en-tête
        
        for i, row in enumerate(reader, 1):
            op, param = row
            print(f" -> Traitement ligne {i}: {op} ({param})")
            self._log(f"Processing: {op} with {param}")
            
            # Simulation d'un crash pour tester __exit__
            if op == "error_trigger":
                raise ValueError("Crash simulé durant le traitement !")

# === Exécution ===
def main():
    setup_environment()
    
    print("\n=== Démarrage du BatchProcessor ===")
    try:
        with BatchProcessor(CSV_FILE, LOG_FILE) as batch:
            batch.process()
    except ValueError as e:
        print(f"\n[Main] Exception attrapée dans le main : {e}")
    except Exception as e:
        print(f"\n[Main] Erreur imprévue : {e}")

    print("\n=== Vérification du fichier journal ===")
    if Path(LOG_FILE).exists():
        with open(LOG_FILE, "r") as f:
            print(f.read())

if __name__ == "__main__":
    main()