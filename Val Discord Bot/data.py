import requests
import json

def get_general_data(username, tagline):

    url =  f'https://api.henrikdev.xyz/valorant/v1/account/{username}/{tagline}'

    r = requests.get(url)
    x = json.loads(r.text)
    gen_data = x['data']
    return gen_data

def get_account_lvl(gen_data):
    account_lvl = gen_data['account_level']
    return account_lvl

def get_mmr_data(username, tagline):

    url = f'https://api.henrikdev.xyz/valorant/v1/mmr/na/{username}/{tagline}'

    r = requests.get(url)
    x = json.loads(r.text)
    mmr_data = x['data']
    return mmr_data

def get_rank(mmr_data):
    rank = mmr_data['currenttierpatched']
    return rank

def get_rank_icon(mmr_data):
    rank_icon_link = mmr_data['images']['small']
    return rank_icon_link

def get_rr(mmr_data):
    rr = mmr_data['ranking_in_tier']
    return rr

def get_mmr_history(username,tagline):

    url = f'https://api.henrikdev.xyz/valorant/v1/mmr-history/na/{username}/{tagline}'
    r = requests.get(url)
    x = json.loads(r.text)
    mmr_history = x['data']
    return mmr_history

def get_wl_history(mmr_history):
    wl_history = []
    for dict in mmr_history:
        for key in dict:
            if key == 'mmr_change_to_last_game':
                if dict[key] > 4:
                    wl_history.append('W')
                elif dict[key]>=0:
                    wl_history.append('D')
                else:
                    wl_history.append('L')
    wl_history = ''.join(wl_history)
    return(wl_history)

def get_match_history(username,tagline):
    url = f'https://api.henrikdev.xyz/valorant/v3/matches/na/{username}/{tagline}?filter=competitive'
    r = requests.get(url)
    x = json.loads(r.text)
    match_history = x['data']
    return match_history

def get_last_played(match_history,username):
    last_5_history = []
    last_5_agents = []
    for i in range(len(match_history)):
        for r in range(len(match_history[i]['players']['all_players'])):
            if match_history[i]['players']['all_players'][r]['name'].lower() == username.lower():
                last_5_history.append(match_history[i]['players']['all_players'][r]['stats'])
                last_5_agents.append(match_history[i]['players']['all_players'][r]['character'])
    return last_5_history,last_5_agents

def get_last_5_stats(last_5_history,match_history):
    acs = []
    kills = []
    deaths = []
    assists = []
    hs = []
    map = []
    for i in range(5):
        score = last_5_history[i]['score']
        rounds = match_history[i]['metadata']['rounds_played']
        kills.append(last_5_history[i]['kills'])
        acs.append(round(int(score)/int(rounds),2))
        deaths.append(last_5_history[i]['deaths'])
        assists.append(last_5_history[i]['assists'])
        total_shots = int(last_5_history[i]['bodyshots'])+int(last_5_history[i]['legshots']) + int(last_5_history[i]['headshots'])
        hs.append(round(int(last_5_history[i]['headshots'])/total_shots*100,2))
        map.append(match_history[i]['metadata']['map'])
    return acs, kills, deaths, assists, hs, map
