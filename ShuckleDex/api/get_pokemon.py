import requests
from requests import RequestException

def main():
    pass

def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    return response

if __name__ == '__main__':
    main()
