from bs4 import BeautifulSoup
import requests
import csv
import datetime


mcdonald_url = "https://mcdonalds.pl/"
kfc_url = "https://kfc.pl/"
burgerking_url = "https://burgerking.pl/pl/"

def scrape_prices():
    prices = {}
    # Symulacja żądania z prawdziwej przeglądarki
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(mcdonald_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        mc_section = soup.find('section', class_="menu-section")
        mc_price = mc_section.find(string="Zestaw Happy Meal").find_next('span', class_='price').text.strip('zł')
        prices["McDonald's"] = float(mc_price.replace(',', '.'))
    except Exception as e:
        print("Failed to scrape McDonald's", e)
        prices["McDonald's"] = None

    try:
        response = requests.get(kfc_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        kfc_section = soup.find("div", class_="menu-item")
        kfc_price = kfc_section.find(string="Zestaw dla dzieci").find_next('span', class_='price').text.strip('zł')
        prices["KFC"] = float(kfc_price.replace(',', '.'))
    except Exception as e:
        print("Failed to scrape KFC's", e)
        prices["KFC"] = None

    try:
        response = requests.get(burgerking_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Przykładowy selektor (dostosuj po inspekcji strony)
        bk_section = soup.find('div', class_="menu-section")
        bk_price = bk_section.find(string="King Jr. Meal").find_next('span', class_='price').text.strip('zł')
        prices["Burger King"] = float(bk_price.replace(',', '.'))
    except Exception as e:
        print("Failed to scrape Burger King's", e)
        prices["Burger King"] = None

    return prices

def append_csv(prices):
    file_name = "prices.csv"
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    row = [today] + [prices.get("McDonald's"), prices.get("KFC"), prices.get("Burger King")]

    try:
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Dodaj nagłówki, jeśli plik jest pusty
                writer.writerow(["Data", "McDonald's", "KFC", "Burger King"])
            writer.writerow(row)
    except Exception as e:
        print(f"Błąd podczas zapisu do CSV: {e}")


if __name__ == "__main__":
    prices = scrape_prices()
    print("Today's price of kids menus: ", prices)
    append_csv(prices)
