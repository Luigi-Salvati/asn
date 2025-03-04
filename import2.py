import requests
import hashlib
import os

# Lista di URL da monitorare e relativi settori
URLS = {
    "https://asn23.cineca.it/pubblico/miur/esito/13%252FA1/2/3": "A1 - Economia politica",
    "https://asn23.cineca.it/pubblico/miur/esito/13%252FA2/2/3": "A2 - Politica economica",
    "https://asn23.cineca.it/pubblico/miur/esito/13%252FA3/2/3": "A3 - Scienza delle finanze",
    "https://asn23.cineca.it/pubblico/miur/esito/13%252FA4/2/3": "A4 - Economia applicata",
    "https://asn23.cineca.it/pubblico/miur/esito/13%252FA5/2/3": "A5 - Econometria",
}

RESULTS_FILE = "risultati.txt"

def get_page_content(url):
    """Scarica il contenuto della pagina web."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Errore: impossibile accedere alla pagina {url} (status code: {response.status_code})")
        return None

def get_hash(content):
    """Restituisce l'hash del contenuto per il confronto."""
    return hashlib.sha256(content.encode()).hexdigest()

def save_content(content, filename):
    """Salva il contenuto della pagina in un file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

def load_previous_content(filename):
    """Carica il contenuto salvato in precedenza."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    return None

def check_changes(url, sector):
    """Verifica se il contenuto della pagina è cambiato e registra il risultato."""
    content = get_page_content(url)
    if content is None:
        return
    
    previous_content = load_previous_content(f"{sector}_content.txt")
    
    if previous_content is None:
        print(f"Salvataggio iniziale del contenuto della pagina {url}...")
        save_content(content, f"{sector}_content.txt")
    else:
        if get_hash(content) != get_hash(previous_content):
            print(f"La pagina {url} ({sector}) è cambiata!")
            save_content(content, f"{sector}_content.txt")
        else:
            print(f"Nessuna modifica rilevata per {url} ({sector}).")
    
    # Controlla se la pagina contiene la frase "Non risultano presenti candidati"
    if "Non risultano presenti candidati" in content:
        result = f"{sector}: Risultati non pubblicati\n"
    else:
        result = f"{sector}: Risultati pubblicati! - {url}\n"
    
    # Scrive il risultato nel file di output
    with open(RESULTS_FILE, "a", encoding="utf-8") as file:
        file.write(result)

def main():
    """Itera su tutte le pagine da monitorare."""
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)  # Pulisce il file dei risultati prima di ogni esecuzione
    
    for url, sector in URLS.items():
        check_changes(url, sector)

if __name__ == "__main__":
    main()