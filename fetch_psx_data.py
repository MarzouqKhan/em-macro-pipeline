import requests
from bs4 import BeautifulSoup
base_url = 'https://dps.psx.com.pk' # Note: Don't scrape the PSX website for commercial purposes without permission, per their data policy.

# Function that scrapes PSX website and returns High, Low, Current, Change, and % Change of the requested symbol as a dict
def psx_index_fetch(symbol):
    index_url = f'{base_url}/indices'
    try:
        r = requests.get(index_url,timeout=10)
        r.raise_for_status()
    except requests.ConnectionError as e:
        print(f"Encountered {e}, please ensure you are connected to the Internet.")
        return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    indices = soup.find('tbody', class_='tbl__body') # Main table
    symbol_data = None
    for row in indices.find_all('tr'):
        if row.find('b').text == symbol:
            cells = row.find_all('td')
            symbol_data = { # Organizes all relevant symbol data into dict
            'high': float(cells[1]['data-order']),
            'low': float(cells[2]['data-order']),
            'current': float(cells[3]['data-order']),
            'change': float(cells[4]['data-order']),
            'percent_change': float(cells[5]['data-order'])
            }
            break
    return symbol_data

if __name__ == "__main__":
    print(psx_index_fetch('KSE100'))
    print(psx_index_fetch('KSE100')['high'])