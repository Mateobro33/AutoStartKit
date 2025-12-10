import os
import winreg
from pathlib import Path

# ========================================
# CONFIGURATION
# ========================================
FICHIER_CIBLE = "texte.exe"  # Nom du fichier à vérifier
# ========================================

def verifier_registre():
    """
    Vérifie si le programme est dans le registre de démarrage
    """
    try:
        nom_app = Path(FICHIER_CIBLE).stem
        cle_registre = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        cle = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            cle_registre,
            0,
            winreg.KEY_READ
        )
        
        try:
            valeur, _ = winreg.QueryValueEx(cle, nom_app)
            winreg.CloseKey(cle)
            return True, valeur
        except FileNotFoundError:
            winreg.CloseKey(cle)
            return False, None
    
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def verifier_fichiers():
    """
    Vérifie si les fichiers existent dans l'emplacement de destination
    """
    dossier_destination = Path(os.getenv('LOCALAPPDATA')) / Path(FICHIER_CIBLE).stem
    chemin_exe = dossier_destination / FICHIER_CIBLE
    
    resultats = {
        'dossier_existe': dossier_destination.exists(),
        'exe_existe': chemin_exe.exists(),
        'chemin_dossier': str(dossier_destination),
        'chemin_exe': str(chemin_exe)
    }
    
    # Lister les fichiers dans le dossier
    if dossier_destination.exists():
        resultats['fichiers'] = [f.name for f in dossier_destination.iterdir()]
    else:
        resultats['fichiers'] = []
    
    return resultats

def main():
    print("=" * 70)
    print("VÉRIFICATION DE L'INSTALLATION AU DÉMARRAGE")
    print("=" * 70)
    print()
    
    # Vérifier le registre
    print("📋 VÉRIFICATION DU REGISTRE WINDOWS")
    print("-" * 70)
    dans_registre, chemin_registre = verifier_registre()
    
    if dans_registre:
        print(f"✓ {FICHIER_CIBLE} EST dans le démarrage Windows")
        print(f"  Chemin enregistré: {chemin_registre}")
    else:
        print(f"✗ {FICHIER_CIBLE} N'EST PAS dans le démarrage Windows")
    
    print()
    
    # Vérifier les fichiers
    print("📁 VÉRIFICATION DES FICHIERS")
    print("-" * 70)
    infos_fichiers = verifier_fichiers()
    
    print(f"Dossier: {infos_fichiers['chemin_dossier']}")
    
    if infos_fichiers['dossier_existe']:
        print(f"✓ Le dossier existe")
        print()
        print(f"Fichier exe: {infos_fichiers['chemin_exe']}")
        
        if infos_fichiers['exe_existe']:
            print(f"✓ L'exe existe")
        else:
            print(f"✗ L'exe N'EXISTE PAS")
        
        print()
        print("Contenu du dossier:")
        if infos_fichiers['fichiers']:
            for fichier in infos_fichiers['fichiers']:
                print(f"  - {fichier}")
        else:
            print("  (vide)")
    else:
        print(f"✗ Le dossier N'EXISTE PAS")
    
    print()
    print("=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    
    if dans_registre and infos_fichiers['exe_existe']:
        print("✓ TOUT EST BON! Le programme se lancera au démarrage.")
    elif dans_registre and not infos_fichiers['exe_existe']:
        print("⚠ ATTENTION! Le programme est dans le registre mais le fichier")
        print("  n'existe pas. Il faut réinstaller.")
    elif not dans_registre and infos_fichiers['exe_existe']:
        print("⚠ ATTENTION! Les fichiers existent mais le programme n'est pas")
        print("  dans le registre de démarrage. Il faut réinstaller.")
    else:
        print("✗ Le programme N'EST PAS installé.")
    
    print()
    input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()