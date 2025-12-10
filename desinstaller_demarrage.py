import os
import winreg
import shutil
from pathlib import Path

# ========================================
# CONFIGURATION
# ========================================
FICHIER_CIBLE = "texte.exe"  # Nom du fichier à désinstaller
AFFICHER_CONSOLE = True      # True = voir ce qui se passe, False = invisible
# ========================================

def supprimer_du_registre():
    """
    Supprime l'entrée du registre de démarrage
    """
    try:
        nom_app = Path(FICHIER_CIBLE).stem
        cle_registre = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        cle = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            cle_registre,
            0,
            winreg.KEY_SET_VALUE
        )
        
        try:
            winreg.DeleteValue(cle, nom_app)
            winreg.CloseKey(cle)
            return True, "Entrée du registre supprimée"
        except FileNotFoundError:
            winreg.CloseKey(cle)
            return False, "L'entrée n'existait pas dans le registre"
    
    except Exception as e:
        return False, f"Erreur registre: {str(e)}"

def supprimer_fichiers():
    """
    Supprime le dossier contenant l'exe et ses fichiers
    """
    try:
        dossier_destination = Path(os.getenv('LOCALAPPDATA')) / Path(FICHIER_CIBLE).stem
        
        if dossier_destination.exists():
            shutil.rmtree(dossier_destination)
            return True, f"Dossier supprimé: {dossier_destination}"
        else:
            return False, f"Le dossier n'existait pas: {dossier_destination}"
    
    except Exception as e:
        return False, f"Erreur lors de la suppression: {str(e)}"

def main():
    if AFFICHER_CONSOLE:
        print("=" * 70)
        print("DÉSINSTALLATION DU DÉMARRAGE AUTOMATIQUE")
        print("=" * 70)
        print()
        print(f"Programme à désinstaller: {FICHIER_CIBLE}")
        print()
        
        # Confirmation
        reponse = input("Voulez-vous vraiment désinstaller ? (o/n): ").lower()
        
        if reponse != 'o' and reponse != 'oui':
            print("\nAnnulé.")
            input("\nAppuyez sur Entrée pour quitter...")
            return
        
        print()
    
    registre_supprime = False
    fichiers_supprimes = False
    
    # Supprimer du registre
    if AFFICHER_CONSOLE:
        print("🗑️  Suppression du registre Windows...")
    
    succes, message = supprimer_du_registre()
    registre_supprime = succes
    
    if AFFICHER_CONSOLE:
        if succes:
            print(f"  ✓ {message}")
        else:
            print(f"  ℹ {message}")
        print()
    
    # Supprimer les fichiers
    if AFFICHER_CONSOLE:
        print("🗑️  Suppression des fichiers...")
    
    succes, message = supprimer_fichiers()
    fichiers_supprimes = succes
    
    if AFFICHER_CONSOLE:
        if succes:
            print(f"  ✓ {message}")
        else:
            print(f"  ℹ {message}")
        print()
        
        print("=" * 70)
        print("RÉSUMÉ")
        print("=" * 70)
        
        if registre_supprime and fichiers_supprimes:
            print("✓ DÉSINSTALLATION COMPLÈTE!")
            print(f"  {FICHIER_CIBLE} ne se lancera plus au démarrage.")
        elif registre_supprime or fichiers_supprimes:
            print("⚠ DÉSINSTALLATION PARTIELLE")
            if registre_supprime and not fichiers_supprimes:
                print("  Le registre a été nettoyé mais les fichiers n'existaient pas.")
            elif not registre_supprime and fichiers_supprimes:
                print("  Les fichiers ont été supprimés mais le registre était déjà vide.")
        else:
            print("ℹ Rien à désinstaller - le programme n'était pas installé.")
        
        print()
        input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()