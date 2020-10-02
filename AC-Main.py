import json
import os
from pathlib import Path

from discord import Client

import pokeformat

__version__ = "v1.0.3-final"


def main():
    pokemon_list_dir = Path('lts/pokemon.json')
    bots: [int] = [716390085896962058]

    def read_pokemon() -> [str]:
        if os.path.exists(pokemon_list_dir):
            with open(pokemon_list_dir, 'r') as f:
                pf = json.load(f)
            return pf
        pokeformat.format_poke()
        read_pokemon()

    client: Client = Client()
    pokemon: [str] = read_pokemon()

    @client.event
    async def on_ready():
        print(f'Initialized PokeHelper {__version__}')

    @client.event
    async def on_message(msg):
        if msg.author.id in bots:
            print("heard bot message")
            if 'The pokémon is' in msg.content:
                content = str(msg.content).strip().strip('.').split(' ')
                pokemon_hint = ''
                for msg_piece in content:
                    if '_' in msg_piece:
                        if 'é' in msg_piece:
                            await msg.channel.send('Flabébé')
                            return
                        msg_piece = msg_piece.replace('\\', '')
                        pokemon_hint += (' ' + msg_piece)
                        pokemon_hint = pokemon_hint.strip()
                final_mons = search_mons(pokemon_hint)
                await msg.channel.send(str(final_mons).strip('_'))

    def search_mons(hint) -> [str]:
        possible_mons = pokemon
        print(hint)
        for i in range(len(hint)):
            if not (hint[i] == '_'):
                new_possible_mons = []
                for p in possible_mons:
                    if len(hint) == len(p) and hint[i] == p[i]:
                        new_possible_mons.append(p)
                possible_mons = new_possible_mons
        return possible_mons

    client.run(str(input('Please input bot Token: ')))


if __name__ == '__main__':
    main()
