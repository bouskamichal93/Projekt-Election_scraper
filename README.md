Volební scraper – volby do Poslanecké sněmovny 2017

Tento Python program stáhne výsledky voleb do Poslanecké sněmovny z webu volby.cz pro vybraný okres.

Co program dělá:
-Z webové stránky zjistí seznam obcí v daném okrese.
-Pro každou obec načte:
    -počet voličů,
    -počet vydaných obálek,
    -počet platných hlasů,
    -počet hlasů pro jednotlivé strany.
    -Data uloží do souboru '*.csv'

Obsah projektu:
  main.py – hlavní skript pro stažení a zpracování dat
  requirements.txt – seznam potřebných knihoven
  README.md – tento popis projektu

Funkce použité v programu:

-'download_page(url)':
    -Stáhne HTML stránku zadané adresy URL.
    -Vstup: 'url' – webová adresa
    -Výstup: HTML text

-'make_soup(html)':
    -Převede HTML text na 'BeautifulSoup' objekt, který usnadňuje hledání v HTML.
    -Vstup: 'html' – text HTML
    -Výstup: objekt 'soup'

-'find_municipalities(soup)':
    -Najde v HTML všechny obce (řádky v tabulce) a uloží jejich kódy, názvy a odkazy.
    -Vstup: 'soup' – objekt 'BeautifulSoup'
    -Výstup: slovník '{"kód": {"url": ..., "name": ...}}'

-'process_municipality(code, url, name)'
    -Načte detailní stránku obce a získá statistiku a počty hlasů.

Vstupy:
    -'code': kód obce (např. 538954),
    -'url': odkaz na stránku obce,
    -'name': název obce
Výstup: slovník s daty

Příklad výstupu:

{
  "municipality_code": "538954",
  "municipality_name": "Jesenice",
  "voters_listed": 2540,
  "envelopes_issued": 1985,
  "valid_votes": 1975,
  "ANO 2011": 680,
  "ODS": 432,
  ...
}

Jak spustit skript krok za krokem:
1.Nainstaluj potřebné knihovny
2.Otevři terminál (nebo příkazový řádek) a spusť následující příkaz:
    'pip install requests beautifulsoup4 pandas'
    
 Tento příkaz nainstaluje všechny potřebné knihovny, které skript používá:
      requests – pro stahování HTML stránek z webu
      beautifulsoup4 – pro parsování a extrakci dat z HTML
      pandas – pro uložení a zpracování dat ve formě tabulky (CSV)
   

3.Získej odkaz na stránku s obcemi
  Například:
  https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
  Tento odkaz odpovídá jednomu okresu – můžeš ho získat z oficiálního webu volebního serveru ČSÚ podle vybraného území.

4.Spusť skript z terminálu nebo příkazového řádku
    Přejdi do složky, kde je uložený soubor main.py, a spusť skript tímto způsobem:
    python3 main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vystup.csv
    První parametr (v uvozovkách) je URL adresa, odkud se načítají odkazy na obce.     
    Druhý parametr je název výstupního souboru, např. vystup.csv.       

Po dokončení Skript vypíše zprávu o počtu zpracovaných obcí a vytvoří soubor CSV ve stejné složce. 
Tento soubor obsahuje výsledky voleb podle obcí a lze jej otevřít např. v Excelu.
