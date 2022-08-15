import re
import json


inicio_regex = re.compile(r".*InitGame:.*")
kill_regex = re.compile(r".*Kill:.*:(.*).*killed(.*)by")
fim_jogo = re.compile(r".*ShutdownGame:.*")

players = {}


def parse_game(logfile):
    game_count = 1

    parsed_matches = {}
    with open(logfile, "r", encoding="utf-8") as log:
        for line in log.readlines():
            if inicio_regex.match(line):
                game = f"game-{game_count}"
                parsed_matches[game] = {
                    "total_kills": 0,
                    "players": []
                }
                game_count += 1

            if kill_regex.match(line):
                criaDicJogadorKill(line, parsed_matches[game])
            if fim_jogo.match(line):
                criaEstrutura(parsed_matches[game])
                players.clear()
    result_data = json.dumps(parsed_matches, indent=4)
    return result_data


def criaDicJogadorKill(line, game_match):
    linha = kill_regex.match(line)
    player_vivo = linha.group(1).strip()
    player_morto = linha.group(2).strip()

    game_match["total_kills"] += 1

    if player_vivo != "<world>" and player_vivo not in players:
        players[player_vivo] = 0

    if player_morto not in players:
        players[player_morto] = 0

    if player_vivo != "<world>" and player_vivo != player_morto:
        if player_vivo in players:
            players[player_vivo] += 1
        else:
            players[player_vivo] = 1
    else:
        if player_morto in players:
            players[player_morto] -= 1
        else:
            players[player_morto] = -1
    return players


def criaEstrutura(game_match):
    nomes = list(players.keys())
    kills = list(players.values())
    for i in range(len(nomes)):
        jogador = {
            "id": nomes.index(nomes[i]) + 1,
            "nome": nomes[i],
            "kills": kills[i]
        }
        game_match["players"].append(jogador)


print(parse_game("Quake.txt"))
