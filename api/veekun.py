import requests
from bs4 import BeautifulSoup

def veekun_id(soup_data):
    pokemon_id_column = soup_data.find("div", {"class":
                                               "dex-column"}).find("dl")
    pokemon_id = pokemon_id_column.find_all("dd").pop(1).text.strip()
    pokemon_id = pokemon_id.zfill(3)
    return pokemon_id
    


def veekun_types(soup_data):
    pokemon_type_div = soup_data.find(id="dex-page-types")
    pokemon_type_links = pokemon_type_div.find_all("a")

    pokemon_types = []

    for pokemon_type in pokemon_type_links:
        pokemon_type = pokemon_type.find("img").get('title')
        pokemon_types += [pokemon_type]

    return pokemon_types


def veekun_stats(soup_data):
    pokemon_stats_table = soup_data.find(
        "table", {"class": "dex-pokemon-stats"}).find("tbody")
    pokemon_stats_rows = pokemon_stats_table.find_all("tr")

    pokemon_stats = {}

    for pokemon_stat in pokemon_stats_rows:
        pokemon_stats.update(
            {pokemon_stat.find("th").text: 
                pokemon_stat.find_next("td").find("div", {"class": 
                    "dex-pokemon-stats-bar"}).text})

    return pokemon_stats


def veekun_abilities(soup_data):
    pokemon_abilities_column = soup_data.find("dl", {"class": 
                                                     "pokemon-abilities"})
    pokemon_abilities_raws = pokemon_abilities_column.find_all("dt")
    
    pokemon_abilities = []
    
    for pokemon_ability in pokemon_abilities_raws:
        pokemon_abilities += [pokemon_ability.find("a").text]
        
    pokemon_abilities = {"abilities": pokemon_abilities}
        
    return pokemon_abilities


def veekun_hidden_ability(soup_data):
    pokemon_abilities_column = soup_data.find_all("dl", {"class":
                                                         "pokemon-abilities"})
    
    pokemon_ability = pokemon_abilities_column.pop(1).find("dt").find("a").text
    return pokemon_ability


def veekun_data(pokemon):
    url = "https://veekun.com/dex/pokemon/{}".format(pokemon)
    raw_data = requests.get(url)
    soup_data = BeautifulSoup(raw_data.text, "html5lib")
    pokemon_name = soup_data.find(id="dex-page-name").text
    pokemon_id = veekun_id(soup_data)
    pokemon_types = veekun_types(soup_data)
    pokemon_stats = veekun_stats(soup_data)
    pokemon_abilities = veekun_abilities(soup_data)
    try:
        pokemon_hidden_ability = veekun_hidden_ability(soup_data)
    except:
        pokemon_hidden_ability = None

    pokemon_abilities["hidden_ability"] = pokemon_hidden_ability

    pokemon_data = {"id": pokemon_id,
                    "name": pokemon_name,
                    "types": pokemon_types,
                    "stats": pokemon_stats,
                    "abilities": pokemon_abilities}
    
    return pokemon_data


if __name__ == "__main__":
    print(veekun_data("chikorita"))
