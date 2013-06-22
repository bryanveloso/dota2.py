import datetime
import time
import requests


# Last updated: 5/31/2013
HEROES = dict(
    abaddon=102,
    alchemist=73,
    ancient_apparition=68,
    antimage=1,
    axe=2,
    bane=3,
    batrider=65,
    beastmaster=38,
    bloodseeker=4,
    bounty_hunter=62,
    brewmaster=78,
    bristleback=99,
    broodmother=61,
    centaur=96,
    chaos_knight=81,
    chen=66,
    clinkz=56,
    crystal_maiden=5,
    dark_seer=55,
    dazzle=50,
    death_prophet=43,
    disruptor=87,
    doom_bringer=69,
    dragon_knight=49,
    drow_ranger=6,
    earthshaker=7,
    elder_titan=103,
    enchantress=58,
    enigma=33,
    faceless_void=41,
    furion=53,
    gyrocopter=72,
    huskar=59,
    invoker=74,
    jakiro=64,
    juggernaut=8,
    keeper_of_the_light=90,
    kunkka=23,
    legion_commander=104,
    leshrac=52,
    lich=31,
    life_stealer=54,
    lina=25,
    lion=26,
    lone_druid=80,
    luna=48,
    lycan=77,
    magnataur=97,
    medusa=94,
    meepo=82,
    mirana=9,
    morphling=10,
    naga_siren=89,
    necrolyte=36,
    nevermore=11,
    night_stalker=60,
    nyx_assassin=88,
    obsidian_destroyer=76,
    ogre_magi=84,
    omniknight=57,
    phantom_assassin=44,
    phantom_lancer=12,
    puck=13,
    pudge=14,
    pugna=45,
    queenofpain=39,
    rattletrap=51,
    razor=15,
    riki=32,
    rubick=86,
    sand_king=16,
    shadow_demon=79,
    shadow_shaman=27,
    shredder=98,
    silencer=75,
    skeleton_king=42,
    skywrath_mage=101,
    slardar=28,
    slark=93,
    sniper=35,
    spectre=67,
    spirit_breaker=71,
    storm_spirit=17,
    sven=18,
    templar_assassin=46,
    tidehunter=29,
    tinker=34,
    tiny=19,
    treant=83,
    troll_warlord=95,
    tusk=100,
    undying=85,
    ursa=70,
    vengefulspirit=20,
    venomancer=40,
    viper=47,
    visage=92,
    warlock=37,
    weaver=63,
    windrunner=21,
    wisp=91,
    witch_doctor=30,
    zuus=22,
)

MATCH_SKILL_LEVELS = (
    0,  # Any
    1,  # Normal
    2,  # High
    3,  # Very high
)

MATCH_GAME_MODES = (
    1,  # All Pick
    2,  # Captains Mode
    3,  # Random Draft
    4,  # Single Draft
    5,  # All Random
    6,  # ?? INTRO/DEATH ??
    7,  # The Diretide
    8,  # Reverse Captains Mode
    9,  # Greeviling
    10,  # Tutorial
    11,  # Mid Only
    12,  # Least Played
    13,  # New Player Poo
)


class Dota2APIError(Exception):
    pass


class Dota2API(object):

    base_url = 'https://api.steampowered.com'
    api_key = None

    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        if base_url:
            self.base_url = base_url

    def __request(self, method, path, **kwargs):
        url = self.base_url + path
        if not self.api_key:
            raise AttributeError('api_key not yet set')
        kwargs.setdefault('params', dict()).update(key=self.api_key)
        return requests.request(method, url, **kwargs).json()

    def __to_timestamp(self, date):
        if type(date) == datetime.datetime:
            date = time.mktime(date.timetuple())
        return int(date)

    def get_steam_id(self, vanity_name, **params):
        path = '/ISteamUser/ResolveVanityURL/v0001'
        params.update(
            vanityurl=vanity_name,
        )
        response = self.__request('get', path, params=params).get('response')
        if response and response['success']:
            return response['steamid']

    def get_player_summaries(self, steam_ids, **params):
        if type(steam_ids) not in (str, unicode):
            steam_ids = ','.join(map(str, steam_ids))

        path = '/ISteamUser/GetPlayerSummaries/v0002'
        params.update(
            steamids=steam_ids,
        )
        return (self.__request('get', path, params=params)
                .get('response', {})
                .get('players', []))

    def get_heroes(self, **params):
        path = '/IEconDOTA2_570/GetHeroes/v0001'
        params.setdefault('language', 'en_us')
        return (self.__request('get', path, params=params)
                .get('result', {})
                .get('heroes', []))

    def get_match_history(self, player_name=None, hero_id=None, game_mode=None,
                          skill=0, date_min=None, date_max=None,
                          min_players=None, account_id=None, league_id=None,
                          start_at_match_id=None, matches_requested=25,
                          tournament_games_only=None, **params):

        if hero_id:
            if type(hero_id) == 'str':
                hero_id = HEROES[hero_id]
            hero_id = int(hero_id)
            if hero_id not in HEROES.values():
                raise ValueError('Invalid hero id: %r', hero_id)

        if game_mode:
            game_mode = int(game_mode)
            if game_mode not in MATCH_GAME_MODES:
                raise ValueError('Invalid match game mode: %r' % game_mode)

        if skill:
            skill = int(skill)
            if skill not in MATCH_SKILL_LEVELS:
                raise ValueError('Invalid match skill level: %r' % skill)

        if date_min:
            date_min = self.__to_timestamp(date_min)
        if date_max:
            date_max = self.__to_timestamp(date_max)

        matches_requested = int(matches_requested)
        if matches_requested > 25:
            req_count, last_req = divmod(matches_requested, 25)
            if last_req > 0:
                req_count += 1
            matches_requested = 25
        else:
            req_count, last_req = 1, matches_requested

        path = '/IDOTA2Match_570/GetMatchHistory/v001'
        params.update(
            player_name=player_name,
            hero_id=hero_id,
            game_mode=game_mode,
            skill=skill,
            date_min=date_min,
            date_max=date_max,
            min_players=min_players,
            account_id=account_id,
            league_id=league_id,
            start_at_match_id=start_at_match_id,
            matches_requested=matches_requested,
            tournament_games_only=tournament_games_only,
        )

        matches = []
        for i in range(req_count):
            if i + 1 == req_count and last_req > 0:
                params.update(matches_requested=last_req)
            response = self.__request('get', path, params=params)
            if response['result']['status'] != 1:
                raise Dota2APIError(response['result']['statusDetail'])
            curr_matches = response['result']['matches']
            if len(curr_matches) > 0:
                params.update(
                    start_at_match_id=curr_matches[-1]['match_id'] - 1,
                )
            matches.extend(curr_matches)
            if response['result']['results_remaining'] < 1:
                break

        response['result'].update(
            matches=matches,
            num_results=len(matches),
        )
        return response['result']

    def get_match_details(self, match_id, **params):
        path = '/IDOTA2Match_570/GetMatchDetails/v001'
        params.update(
            match_id=match_id,
        )
        return self.__request('get', path, params=params).get('result')

    def get_league_listing(self):
        path = '/IDOTA2Match_570/GetLeagueListing/v001'
        return (self.__request('get', path)
                .get('result', {})
                .get('leagues', []))

    def get_live_league_games(self):
        path = '/IDOTA2Match_570/GetLiveLeagueGames/v001'
        return (self.__request('get', path)
                .get('result', {})
                .get('games', []))
