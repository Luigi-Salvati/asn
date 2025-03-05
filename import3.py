import requests
from bs4 import BeautifulSoup
import os

# Dizionario con i settori scientifici disciplinari e i rispettivi URL
URLS = {
    "A1": "https://asn23.cineca.it/pubblico/miur/esito/13%252FA1/2/3",
    "A2": "https://asn23.cineca.it/pubblico/miur/esito/13%252FA2/2/3",
    "A3": "https://asn23.cineca.it/pubblico/miur/esito/13%252FA3/2/3",
    "A4": "https://asn23.cineca.it/pubblico/miur/esito/13%252FA4/2/3",
    "A5": "https://asn23.cineca.it/pubblico/miur/esito/13%252FA5/2/3",
    "C1": "https://asn23.cineca.it/pubblico/miur/esito/13%252FC1/2/3",
}

RESULTS_FILE = "README.md"


def get_page_content(url):
    """Scarica il contenuto della pagina web."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Errore nel recupero della pagina {url}: {e}")
        return None


def check_results():
    """Visita ogni URL e verifica se ci sono risultati pubblicati."""
    results = ["# Risultati area 13<br><br>"]
    
    for sector, url in URLS.items():
        content = get_page_content(url)
        if content is None:
            continue
        
        # Controlla se la frase "Non risultano presenti candidati" è nella pagina
        if "Non risultano presenti candidati" not in content:
            results.append(f"{sector}: Risultati pubblicati - {url}<br>")
            print(f"{sector}: Risultati pubblicati")
    print(f"Il file README.md sarà salvato in: {os.path.abspath(RESULTS_FILE)}")
    # Scrive i risultati nel file solo se ci sono risultati da scrivere
    if results:
        with open(RESULTS_FILE, "w", encoding="utf-8") as file:
            file.writelines(results)


if __name__ == "__main__":
    check_results()
