import flask
import json
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from jaccard_index.jaccard import jaccard_index
from Levenshtein import distance
from veekun import veekun_data
from pokemondb import pokemondb_data
from wikidex import wikidex_data


app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False


@app.route('/pokemon', methods=['GET'])
def hello_world():
  return {"message": "Hola, María Jesús"}, 200


@app.route('/pokemon/<pokemon>', methods=['GET'])
def get_pokemon_data(pokemon):
    pokemon = str(pokemon).lstrip('0').lower()
    url1 = "https://pokeapi.co/api/v2/pokemon-species/{}".format(pokemon)
    url2 = "https://pokeapi.co/api/v2/pokemon/{}".format(pokemon)

    pk_api_name = requests.get(url1)
    pk_api_data = requests.get(url2)
    try:
        pk_api_name = requests.get(url1)
        pk_api_data = requests.get(url2)
        pokemon = pk_api_name.json()['name']
        pk_wikidex_data = wikidex_data(pokemon)
        pk_veekun_data = veekun_data(pokemon)
        pk_pokemondb_data = pokemondb_data(pokemon)
    except:
        return {"error": "Pokémon not found"}, 404

    sprite = pk_api_data.json(
    )['sprites']['other']['official-artwork']['front_default']
    pk_id_distance = distance(pk_pokemondb_data['id'], pk_veekun_data['id'])
    pk_name_jaccard = jaccard_index(
        pk_pokemondb_data['name'], pk_wikidex_data['name'])

    if pk_id_distance < 1 and pk_name_jaccard > 0.7:
        pk_data = {
            "id": pk_pokemondb_data['id'],
            "name": pk_pokemondb_data['name'],
            "types": pk_wikidex_data['types'],
            "stats": pk_veekun_data['stats'],
            "abilities": pk_wikidex_data['abilities'],
            "sprite": sprite
        }
        return pk_data, 200

    return {"error": "Error during record linking"}, 400


if __name__ == "__main__":
    app.run()
