import requests
from bs4 import BeautifulSoup
import time

# Fonction pour récupérer le contenu HTML d'une URL
def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Vérifie si la requête a réussi
        return response.content
    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Erreur de connexion: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Délai d'attente dépassé: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Erreur lors de la requête: {req_err}")
    return None

# Fonction pour extraire les EPS à partir du contenu HTML
def extract_eps(soup, period):
    eps_data = {}
    try:
        # Identifier la table contenant les données EPS
        table = soup.find("table", {"class": "financials-table"})
        if not table:
            print("Table des données financières non trouvée.")
            return None

        # Parcourir les lignes de la table
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 1:
                header = cols[0].get_text(strip=True)
                if period in header:
                    for i in range(1, len(cols)):
                        year = cols[i].get("data-year")
                        eps_value = cols[i].get_text(strip=True)
                        if year and eps_value:
                            eps_data[year] = eps_value
        return eps_data
    except Exception as e:
        print(f"Erreur lors de l'extraction des EPS: {e}")
        return None

# URL cible (exemple pour Apple Inc.)
url = "https://www.macrotrends.net/stocks/charts/AAPL/apple/eps-earnings-per-share-diluted"

# Récupérer le contenu HTML
html_content = fetch_html(url)
if html_content:
    # Parser le HTML avec BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extraire les EPS annuels
    print("EPS annuels :")
    annual_eps = extract_eps(soup, "Annual")
    if annual_eps:
        for year, eps in annual_eps.items():
            print(f"Année {year}: EPS = {eps}")
    else:
        print("Aucun EPS annuel trouvé.")

    # Pause pour éviter de surcharger le serveur
    time.sleep(2)

    # Extraire les EPS trimestriels
    print("\nEPS trimestriels :")
    quarterly_eps = extract_eps(soup, "Quarterly")
    if quarterly_eps:
        for year, eps in quarterly_eps.items():
            print(f"Trimestre {year}: EPS = {eps}")
    else:
        print("Aucun EPS trimestriel trouvé.")
else:
    print("Impossible de récupérer le contenu HTML.")
