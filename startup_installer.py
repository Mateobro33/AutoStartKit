import os
import sys
import winreg
import shutil
from pathlib import Path

# ========================================
# CONFIGURATION
# ========================================
FICHIER_CIBLE = "texte.exe"           # Nom du fichier .exe à lancer au démarrage
FICHIERS_NECESSAIRES = ["logs"]       # Fichiers/dossiers à copier avec l'exe (logs, config.txt, etc.)
AFFICHER_CONSOLE = True              # True = voir ce qui se passe, False = invisible
# ========================================

def copier_fichiers_vers_destination(dossier_source, dossier_destination):
    """
    Copie l'exe et les fichiers nécessaires vers un dossier permanent
    """
    try:
        # Créer le dossier de destination s'il n'existe pas
        dossier_destination.mkdir(parents=True, exist_ok=True)
        
        # Copier l'exe principal
        source_exe = dossier_source / FICHIER_CIBLE
        dest_exe = dossier_destination / FICHIER_CIBLE
        
        if source_exe.exists():
            shutil.copy2(source_exe, dest_exe)
        else:
            return False, f"Erreur: {FICHIER_CIBLE} n'existe pas!"
        
        # Copier les fichiers/dossiers nécessaires
        for item in FICHIERS_NECESSAIRES:
            source_item = dossier_source / item
            dest_item = dossier_destination / item
            
            if source_item.exists():
                if source_item.is_dir():
                    # Copier le dossier entier
                    if dest_item.exists():
                        shutil.rmtree(dest_item)
                    shutil.copytree(source_item, dest_item)
                else:
                    # Copier le fichier
                    shutil.copy2(source_item, dest_item)
        
        return True, str(dest_exe)
    
    except Exception as e:
        return False, f"Erreur lors de la copie: {str(e)}"

def ajouter_au_demarrage(chemin_exe_cible):
    """
    Ajoute un exécutable au démarrage de Windows via le registre
    """
    try:
        nom_app = Path(chemin_exe_cible).stem
        cle_registre = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        cle = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            cle_registre,
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.SetValueEx(cle, nom_app, 0, winreg.REG_SZ, chemin_exe_cible)
        winreg.CloseKey(cle)
        
        return True, "Programme ajouté au démarrage avec succès!"
    
    except Exception as e:
        return False, f"Erreur registre: {str(e)}"

def main():
    # Obtenir le dossier du programme actuel
    if getattr(sys, 'frozen', False):
        dossier_actuel = Path(sys.executable).parent
    else:
        dossier_actuel = Path(__file__).parent
    
    # Définir le dossier de destination (AppData local)
    dossier_destination = Path(os.getenv('LOCALAPPDATA')) / Path(FICHIER_CIBLE).stem
    
    if AFFICHER_CONSOLE:
        print("=" * 60)
        print("INSTALLATION AU DÉMARRAGE WINDOWS")
        print("=" * 60)
        print(f"\nDossier source: {dossier_actuel}")
        print(f"Dossier destination: {dossier_destination}")
        print(f"Fichier cible: {FICHIER_CIBLE}")
        print(f"Fichiers nécessaires: {', '.join(FICHIERS_NECESSAIRES)}")
        print()
    
    # Copier les fichiers
    if AFFICHER_CONSOLE:
        print("Copie des fichiers...")
    
    succes, resultat = copier_fichiers_vers_destination(dossier_actuel, dossier_destination)
    
    if not succes:
        if AFFICHER_CONSOLE:
            print(f"✗ {resultat}")
            input("\nAppuyez sur Entrée pour quitter...")
        return
    
    chemin_exe_destination = resultat
    
    if AFFICHER_CONSOLE:
        print(f"✓ Fichiers copiés vers: {dossier_destination}")
        print()
    
    # Ajouter au démarrage
    if AFFICHER_CONSOLE:
        print("Ajout au démarrage Windows...")
    
    succes, message = ajouter_au_demarrage(chemin_exe_destination)
    
    if AFFICHER_CONSOLE:
        if succes:
            print(f"✓ {message}")
            print(f"\n{FICHIER_CIBLE} se lancera automatiquement au démarrage!")
            print(f"Emplacement: {chemin_exe_destination}")
        else:
            print(f"✗ {message}")
        
        print()
        input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()