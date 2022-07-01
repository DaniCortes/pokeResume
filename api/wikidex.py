import requests
from bs4 import BeautifulSoup


def wikidex_types(soup_data):
    pokemon_type_table = soup_data.find("table", {"class": "datos resalto"})
    pokemon_type_row = pokemon_type_table.find(
        "tr", {"title": "Tipos a los que pertenece"})
    pokemon_type_cells = pokemon_type_row.find("td")
    pokemon_type_links = pokemon_type_cells.find_all("a")

    pokemon_types = []

    for pokemon_type in pokemon_type_links:
        pokemon_type = pokemon_type.get(
            'title').replace('Tipo ', '').capitalize()
        pokemon_types += [pokemon_type]


    return pokemon_types


def wikidex_stats(soup_data):

    pokemon_stats_table = soup_data.find_all(
        "table", {"class": "tabpokemon"})
    pokemon_stats_table = pokemon_stats_table[1]
    pokemon_stats_rows = pokemon_stats_table.find_all("tr")

    pokemon_stats_rows.pop(0)
    pokemon_stats_rows.pop()
    pokemon_stats_rows.pop()
    pokemon_stats = {}

    for row in pokemon_stats_rows:
        pokemon_stats.update(
            {row.find("th").find("a").get("title").replace(" (estadística)", "")
             : row.find_all("td")[0].text.strip()})

    return pokemon_stats


def wikidex_abilities(soup_data):
    pokemon_ability_table = soup_data.find("table", {"class": "datos resalto"})
    pokemon_ability_row = pokemon_ability_table.find(
        "tr", {"title": "Habilidades que puede conocer"})

    pokemon_ability_cells = pokemon_ability_row.find("td")
    pokemon_ability_links = pokemon_ability_cells.find_all("a")
    pokemon_ability_list = []

    for pokemon_ability in pokemon_ability_links:
        pokemon_ability = pokemon_ability.get('title')
        pokemon_ability_list += [pokemon_ability]

    pokemon_abilities = {"abilities": pokemon_ability_list}

    return pokemon_abilities


def wikidex_hidden_ability(soup_data):
    pokemon_ability_table = soup_data.find("table", {"class": "datos resalto"})
    pokemon_ability_row = pokemon_ability_table.find(
        "tr", {"title": "Habilidad oculta"})

    pokemon_ability_cell = pokemon_ability_row.find("td")
    pokemon_ability_link = pokemon_ability_cell.find("a")

    pokemon_ability = pokemon_ability_link.get('title')

    return pokemon_ability


def wikidex_data(pokemon):
    url = "https://www.wikidex.net/wiki/{}".format(pokemon)
    raw_data = requests.get(url)
    soup_data = BeautifulSoup(raw_data.text, "html5lib")
    pokemon_id = soup_data.find(id="numeronacional").text
    pokemon_name = soup_data.find(id="nombrepokemon").text
    pokemon_types = wikidex_types(soup_data)
    pokemon_stats = wikidex_stats(soup_data)
    pokemon_abilities = wikidex_abilities(soup_data)
    try:
        pokemon_hidden_ability = wikidex_hidden_ability(soup_data)
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
    print(wikidex_data("bulbasaur"))
