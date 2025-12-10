[README (3).md](https://github.com/user-attachments/files/24078122/README.3.md)
# AutoStartKit

**Un outil simple et efficace pour gérer le démarrage automatique de vos programmes sous Windows.**

AutoStartKit permet d'installer, vérifier et désinstaller un programme pour qu'il se lance automatiquement au démarrage de Windows, **sans nécessiter de droits administrateur**.

---

## 📦 Structure du Projet

```
AutoStartKit/
├── README.md
├── KIT_INSTALLATION/
│   ├── AutoStartKit_Installer.exe   # Installe le programme au démarrage
│   ├── MonProgramme.exe             # Remplacez par votre programme
│   └── logs/                        # Dossier pour les logs
├── outils_supplementaires/
│   ├── AutoStartKit_Verifier.exe     # Vérifie l'installation
│   └── AutoStartKit_Desinstaller.exe # Désinstalle le programme
└── source_et_dev/
    ├── installer.py                 # Code source de l'installeur
    ├── verifier.py                  # Code source du vérificateur
    ├── desinstaller.py             # Code source du désinstalleur
    ├── txt/                         # Documentation technique
    └── fichiers_spec/               # Fichiers de compilation PyInstaller
```

---

## 🚀 Utilisation

### 1. Installer un Programme au Démarrage
1. Placez **votre programme** (ex: `MonProgramme.exe`) dans le dossier `KIT_INSTALLATION/`.
2. Double-cliquez sur `AutoStartKit_Installer.exe`.
3. Votre programme est maintenant configuré pour se lancer automatiquement au démarrage de Windows.

**Emplacement d'installation** :

%LOCALAPPDATA%\MonProgramme```

---

### 2. Vérifier l'Installation
1. Ouvrez le dossier `outils_supplementaires/`.
2. Lancez `AutoStartKit_Verifier.exe`.
3. Le programme affiche :
   - ✅ L'état de l'entrée dans le registre Windows.
   - ✅ La présence des fichiers installés.
   - ✅ L'emplacement exact des fichiers.

---

### 3. Désinstaller
1. Ouvrez le dossier `outils_supplementaires/`.
2. Lancez `AutoStartKit_Desinstaller.exe`.
3. Confirmez la désinstallation en tapant `o` puis **Entrée**. 
4. Le programme supprime :
   - ✅ L'entrée du registre Windows.
   - ✅ Tous les fichiers installés.

---

## ⚙️ Configuration Avancée

### Personnaliser le Kit
Pour adapter AutoStartKit à vos besoins, modifiez les variables dans les fichiers Python (`source_et_dev/`) :

**Dans `installer.py`** :
```python
FICHIER_CIBLE = "MonProgramme.exe"  # Nom de votre programme
FICHIERS_NECESSAIRES = ["logs"]     # Fichiers/dossiers à copier
AFFICHER_CONSOLE = False            # Masquer la console (True pour la voir)
```

**Dans `verifier.py` et `desinstaller.py`** :
```python
FICHIER_CIBLE = "MonProgramme.exe"  # Doit correspondre au nom installé
AFFICHER_CONSOLE = True             # Mode verbose pour le débogage
```

---

### Recompiler les `.exe`
1. **Prérequis** : Installez Python et PyInstaller :
   ```bash
   pip install pyinstaller
   ```
2. Placez-vous dans `source_et_dev/` :
   ```bash
   cd source_et_dev/
   ```
3. Compilez les scripts :
   ```bash
   # Installeur (sans console)
   pyinstaller --onefile --noconsole installer.py
   # Vérificateur (avec console)
   pyinstaller --onefile --console verifier.py
   # Désinstalleur (avec console)
   pyinstaller --onefile --console desinstaller.py
   ```
4. Copiez les `.exe` générés (dans `dist/`) :
   - `installer.exe` → `KIT_INSTALLATION/AutoStartKit_Installer.exe`
   - `verifier.exe` → `outils_supplementaires/AutoStartKit_Verifier.exe`
   - `desinstaller.exe` → `outils_supplementaires/AutoStartKit_Desinstaller.exe`

---

## ❓ FAQ (Questions Fréquentes)

**Q : Où les fichiers sont-ils installés ?**
R : Dans `%LOCALAPPDATA%\MonProgramme\`.

**Q : Comment vérifier manuellement ?**
R :
- **Méthode 1** : Appuyez sur `Win + R`, tapez `%LOCALAPPDATA%`, et cherchez le dossier `MonProgramme`.
- **Méthode 2** : Ouvrez `regedit` et vérifiez la clé `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`.

**Q : Le programme ne se lance pas au démarrage.**
R :
1. Exécutez `AutoStartKit_Verifier.exe`.
2. Vérifiez que votre antivirus n'a pas bloqué `MonProgramme.exe`.
3. Réinstallez avec `AutoStartKit_Installer.exe`.

**Q : Puis-je renommer les fichiers ?**
R : Oui, mais modifiez aussi les variables `FICHIER_CIBLE` dans les scripts Python et recompilez.

---

## 🔧 Dépannage

| **Problème**                     | **Solution**                                                                 |
|----------------------------------|------------------------------------------------------------------------------|
| L'installation échoue            | Vérifiez que `MonProgramme.exe` et `logs/` sont dans `KIT_INSTALLATION/`.   |
| Le programme ne démarre pas      | Utilisez `AutoStartKit_Verifier.exe` et vérifiez l'antivirus.               |
| Erreur "Fichier introuvable"     | Assurez-vous que `MonProgramme.exe` est présent dans le dossier d'installation. |

---

## 📝 Notes Techniques
- **Méthode** : Ajout d'une entrée dans le registre Windows (`Run`).
- **Permissions** : Aucun droit administrateur requis.
- **Compatibilité** : Windows 7, 8, 10, et 11.
- **Langage** : Python 3.x, compilé avec PyInstaller.

---

## 📜 Licence
**Libre d'utilisation et de modification** pour un usage personnel ou professionnel.

**Version** : 1.0
**Date** : Décembre 2025

---

## 🔹 Résumé Rapide

| **Action**          | **Fichier**                                      |
|---------------------|--------------------------------------------------|
| **Installer**       | `KIT_INSTALLATION/AutoStartKit_Installer.exe`     |
| **Vérifier**        | `outils_supplementaires/AutoStartKit_Verifier.exe` |
| **Désinstaller**    | `outils_supplementaires/AutoStartKit_Desinstaller.exe` |
