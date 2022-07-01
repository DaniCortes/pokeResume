# PokéResume
Práctica de ISI.

En esta práctica hemos implementado un buscador de Pokémon.
Este buscador nos muestra el ID, el nombre, los tipos, las estadísticas, las habilidades y una imagen del Pokémon buscado.

Recomendamos instalar los módulos de Python en un [entorno virtual](https://docs.python.org/3/library/venv.html).

Live demo [aquí](https://pokemon.danielcortes.dev).

## Instalación y puesta en marcha

```bash
git clone https://github.com/DaniCortes/pokeResume.git
```

```bash
python3 -m venv pokeResume/api/.venv
```
```bash
source pokeResume/api/.venv/bin/activate
```
```bash
pip install -r pokeResume/api/requirements.txt
```
```bash
pokeResume/api/.venv/bin/python pokeResume/api/isi_api.py
```

## Visualización de la página web
Doble click a ```pokeResume/web/index.html```. Esta página recolecta los datos de [mi API](https://api.danielcortes.dev/pokemon) para mayor facilidad a la hora de probarlo.

## Autores
Daniel Cortés y Cristian Guerra
