import xml.etree.ElementTree as ET
import html
import re
import os
import shutil
# Définition des répertoires
BASE_DIR = "./output"
JAVA_DIR = os.path.join(BASE_DIR, "java")
SQL_DIR = os.path.join(BASE_DIR, "sql")
JS_DIR = os.path.join(BASE_DIR, "js")
# Fonction pour supprimer les anciens fichiers
def clear_output_directory():
    """ Supprime les fichiers existants dans les répertoires de sortie. """
    for directory in [JAVA_DIR, SQL_DIR, JS_DIR]:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                try:
                    os.remove(file_path)
                    print(f":corbeille: Supprimé : {file_path}")
                except Exception as e:
                    print(f":danger: Impossible de supprimer {file_path}: {e}")
# Création des dossiers si non existants
os.makedirs(JAVA_DIR, exist_ok=True)
os.makedirs(SQL_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)
# Supprimer les anciens fichiers avant extraction
clear_output_directory()
# Charger et parser le fichier XML
XML_FILE = "./appDefinition.xml"
if not os.path.exists(XML_FILE):
    print(f":x: ERREUR : Fichier XML introuvable {XML_FILE}")
    exit(1)
tree = ET.parse(XML_FILE)
root = tree.getroot()
# Expressions régulières pour détecter les langages
java_pattern = re.compile(r"\b(import java|public class|void main|System\.out\.println)\b")
sql_pattern = re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|TRUNCATE|FROM|WHERE)\b", re.IGNORECASE)
js_pattern = re.compile(r"\b(function|console\.log|let |var |const |document\.)\b")
# Fonction pour nettoyer et formater le code
import re
def format_code(code):
    """ Nettoie et formate le code pour une meilleure lisibilité. """
    import html
    code = html.unescape(code)  # Décoder les caractères HTML
    code = re.sub(r'^\{"script":"|"\}$', '', code).strip()  # Supprimer les délimiteurs JSON
    code = code.replace("\\r\\n", "\n").replace("\\r", "\n").replace("\\n", "\n")  # Nettoyer les retours de ligne
    # :loupe_gauche: Supprimer les caractères invalides
    code = re.sub(r'[^\x20-\x7E\n\t]', '', code)  # Garde uniquement les caractères imprimables ASCII
    lines = [line.rstrip() for line in code.split("\n") if line.strip()]  # Supprimer les lignes vides
    # Ajouter indentation propre pour Java
    formatted_code = []
    indent_level = 0
    for line in lines:
        if line.strip().startswith("}") and indent_level > 0:
            indent_level -= 1
        formatted_code.append("    " * indent_level + line)
        if line.strip().endswith("{"):
            indent_level += 1
    return "\n".join(formatted_code) + "\n\n"
# Fonction pour extraire le nom de la classe Java
def extract_java_class_name(code):
    """ Extrait le nom de la classe Java et ajoute un numéro unique si nécessaire. """
    match = re.search(r"\bclass\s+(\w+)", code)
    class_name = match.group(1) if match else "UnknownClass"
    # Ajout d'un numéro unique pour éviter les conflits
    if class_name == "UnknownClass":
        class_name += f"_{len(os.listdir(JAVA_DIR)) + 1}"
    return class_name
# Fonction pour enregistrer le fichier avec un nom unique
def save_file(directory, base_name, extension, content):
    """ Sauvegarde un fichier avec un nom unique en évitant les collisions. """
    counter = 1
    file_name = f"{base_name}.{extension}"
    file_path = os.path.join(directory, file_name)
    # Si le fichier existe déjà, incrémenter le compteur
    while os.path.exists(file_path):
        file_name = f"{base_name}_{counter}.{extension}"
        file_path = os.path.join(directory, file_name)
        counter += 1
    # Écriture du fichier
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f":coche_blanche: Fichier généré : {file_path}")
# Parcourir les éléments XML pour extraire les scripts
for elem in root.iter():
    if elem.tag == "pluginProperties":
        raw_code = elem.text
        if raw_code:
            cleaned_code = format_code(raw_code)
            # Vérifier le type de code et l'enregistrer dans un fichier distinct
            if java_pattern.search(cleaned_code):
                class_name = extract_java_class_name(cleaned_code)
                save_file(JAVA_DIR, class_name, "java", cleaned_code)
            elif sql_pattern.search(cleaned_code):
                save_file(SQL_DIR, f"query_{len(os.listdir(SQL_DIR)) + 1}", "sql", cleaned_code)
            elif js_pattern.search(cleaned_code):
                save_file(JS_DIR, f"script_{len(os.listdir(JS_DIR)) + 1}", "js", cleaned_code)
print("\n:tada: Extraction et formatage terminés ! Codes enregistrés dans './output/'")
