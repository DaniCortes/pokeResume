import requests
from bs4 import BeautifulSoup


def pokemondb_id(soup_data):
    pokemon_id_table = soup_data.find("table", {"class":
                                                "vitals-table"}).find("tbody")
    pokemon_id = pokemon_id_table.find("tr").find(
        "td").find("strong").text
    return pokemon_id


def pokemondb_types(soup_data):
    pokemon_types_table = soup_data.find("table", {"class":
                                                   "vitals-table"}).find("tbody")
    pokemon_type_links = pokemon_types_table.find_all(
        "a", {"class": "type-icon"})

    pokemon_types = []

    for pokemon_type in pokemon_type_links:
        pokemon_type = pokemon_type.text
        pokemon_types += [pokemon_type]

    return pokemon_types


def pokemondb_stats(soup_data):
    pokemon_stats_table = soup_data.find(
        "div", {"class": "resp-scroll"}).find("table").find("tbody")
    pokemon_stats_rows = pokemon_stats_table.find_all("tr")

    pokemon_stats = {}

    for pokemon_stat in pokemon_stats_rows:
        pokemon_stats.update(
            {pokemon_stat.find("th").text:
                pokemon_stat.find("td").text})

    return pokemon_stats


def pokemondb_abilities(soup_data):
    pokemon_abilities_table = soup_data.find("table", {"class":
                                                       "vitals-table"}).find("tbody")
    pokemon_abilities_spans = pokemon_abilities_table.find_all("span")

    pokemon_abilities = []

    for pokemon_ability in pokemon_abilities_spans:
        pokemon_abilities += [pokemon_ability.find("a").text]

    pokemon_abilities = {"abilities": pokemon_abilities}

    return pokemon_abilities


def pokemondb_hidden_ability(soup_data):
    pokemon_abilities_table = soup_data.find("table", {"class":
                                                       "vitals-table"}).find("tbody")

    pokemon_ability = pokemon_abilities_table.find("small").find("a").text

    return pokemon_ability


def pokemondb_data(pokemon):
    url = "https://pokemondb.net/pokedex/{}".format(pokemon)
    raw_data = requests.get(url)
    soup_data = BeautifulSoup(raw_data.text, "html5lib")
    pokemon_id = pokemondb_id(soup_data)
    pokemon_name = soup_data.find("h1").text
    pokemon_types = pokemondb_types(soup_data)
    pokemon_stats = pokemondb_stats(soup_data)
    pokemon_abilities = pokemondb_abilities(soup_data)
    try:
        pokemon_hidden_ability = pokemondb_hidden_ability(soup_data)
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
    print(pokemondb_data("bulbasaur"))
