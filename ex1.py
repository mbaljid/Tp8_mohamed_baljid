import contextlib
from pathlib import Path
from contextlib import contextmanager, ExitStack

def main():
    print("=== Partie 1 : Gestion manuelle avec une classe ===")
    
    class TempFileWriter:
        def __enter__(self):
            self.filepath = Path("temp_part1.txt")
            print(f"[Partie 1] Création du fichier : {self.filepath}")
            self.f = self.filepath.open("w")
            return self.f

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.f.close()
            if self.filepath.exists():
                self.filepath.unlink()
                print(f"[Partie 1] Suppression du fichier : {self.filepath}")

    # Exécution Partie 1
    with TempFileWriter() as f:
        f.write("Contenu temporaire via Class\n")
        print("[Partie 1] Écriture terminée.")

    print("\n" + "-"*40 + "\n")

    print("=== Partie 2 : Utilisation de contextlib.contextmanager ===")

    @contextmanager
    def temp_file_generator():
        path = Path("temp_part2.txt")
        print(f"[Partie 2] Création du fichier : {path}")
        f = path.open("w")
        try:
            yield f
        finally:
            f.close()
            if path.exists():
                path.unlink()
                print(f"[Partie 2] Suppression du fichier : {path}")

    # Exécution Partie 2
    with temp_file_generator() as f:
        f.write("Autre test via Generator\n")
        print("[Partie 2] Écriture terminée.")

    print("\n" + "-"*40 + "\n")

    print("=== Partie 3 : Multiples ressources avec ExitStack ===")

    paths = ["a.txt", "b.txt", "c.txt"]
    
    # Exécution Partie 3
    with ExitStack() as stack:
        # On ouvre tous les fichiers et on les ajoute à la stack pour fermeture auto
        files = [stack.enter_context(open(p, "w")) for p in paths]
        
        print(f"[Partie 3] Fichiers ouverts : {paths}")
        for f in files:
            f.write("test\n")
        print("[Partie 3] Écriture dans tous les fichiers terminée.")

    # Nettoyage optionnel pour l'exercice (pour ne pas laisser de fichiers traîner)
    print("[Partie 3] Nettoyage (suppression des fichiers créés)...")
    for p in paths:
        path_obj = Path(p)
        if path_obj.exists():
            path_obj.unlink()
            
    print("=== Fin de l'exercice ===")

if __name__ == "__main__":
    main()