"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Michal Bouška
email: michal.bouska93@gmail.com
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def download_page(url):
    ''' Stáhne HTML stránku z dané adresy URL a vrátí její obsah jako text. '''
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def make_soup(html):
    ''' Vytvoří a vrátí objekt BeautifulSoup, který umožňuje snadno hledat data v HTML. '''
    return BeautifulSoup(html, "html.parser")

def find_municipalities(soup):
    ''' Najde všechny obce a jejich odkazy na podrobné výsledky. '''
    municipalities = {}
    for row in soup.find_all("tr"):
        code_cell = row.find("td", class_="cislo")
        name_cell = row.find("td", class_="overflow_name")
        if code_cell and name_cell:
            link = code_cell.find("a", href=True)
            if link:
                code = link.text.strip()
                name = name_cell.text.strip()
                url = "https://www.volby.cz/pls/ps2017nss/" + link["href"]
                municipalities[code] = {"url": url, "name": name}
    return municipalities

def process_municipality(code, url, name):
    ''' Zpracuje stránku jedné obce – voliče, platné hlasy a hlasy stran. '''
    html = download_page(url)
    soup = make_soup(html)

    voters = int(soup.find("td", headers="sa2").text.replace("\xa0", "").replace(" ", ""))
    envelopes = int(soup.find("td", headers="sa3").text.replace("\xa0", "").replace(" ", ""))
    valid_votes = int(soup.find("td", headers="sa6").text.replace("\xa0", "").replace(" ", ""))

    votes_per_party = {}
    parties_table = soup.find_all("table", class_="table")[1]
    for row in parties_table.find_all("tr")[2:]:
        cols = row.find_all("td")
        if len(cols) >= 3:
            party_name = cols[1].text.strip()
            votes_text = cols[2].text.strip().replace("\xa0", "").replace(" ", "")
            try:
                votes = int(votes_text)
            except:
                votes = 0
            votes_per_party[party_name] = votes

    data = {
        "municipality_code": code,
        "municipality_name": name,
        "voters_listed": voters,
        "envelopes_issued": envelopes,
        "valid_votes": valid_votes
    }
    data.update(votes_per_party)
    return data

if __name__ == "__main__":
    ''' Hlavní část programu – zpracuje argumenty, stáhne data a uloží výsledky do CSV '''
    if len(sys.argv) != 3:
        print("Použití: python volby.py <URL> <vystup.csv>")
        sys.exit(1)

    input_url = sys.argv[1]
    output_file = sys.argv[2]

    html = download_page(input_url)
    soup = make_soup(html)
    municipalities = find_municipalities(soup)
    print(f"Bylo nalezeno {len(municipalities)} obcí.")
    print(f"Program zpracovává obec:")
    results = []
    for code, info in municipalities.items():
        print(f"{info['name']} ({code})")
        try:
            data = process_municipality(code, info["url"], info["name"])
            results.append(data)
        except Exception as e:
            print(f"Chyba u obce {code}: {e}")

    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False, encoding="utf-8", sep=",")
    print(f"Výsledky byly uloženy do '{output_file}'")
