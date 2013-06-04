dota2.py
========

API
---


### `Dota2API.get_steam_id(vanity_name, **params)`

> Gets Steam id by vanity name (e.g. http://steamcommunity.com/id/vanity_name)

Arguments
* `vanity_name` (`str`)

### `Dota2API.get_player_summaries(steam_ids, **params)`

> Gets player summaries given Steam ids

Arguments
* `steam_ids` (`str` or iterable)

### `Dota2API.get_heroes(**params)`

> Gets available heroes list

### `Dota2API.get_match_history(player_name=None, hero_id=None, game_mode=None,skill=0, date_min=None, date_max=None, min_players=None, account_id=None, league_id=None, start_at_match_id=None, matches_requested=25, tournament_games_only=None, **params)`

> Gets list of match history

Arguments
* `player_name` (`str`)
* `hero_id` (`int` or `str`) (check `dota2.HEROES`)
* `game_mode` (`int`) (check `dota2.MATCH_GAME_MODES`)
* `skill` (`int`) (check `dota2.MATCH_SKILL_LEVELS`)
* `date_min` (`datetime.datetime` or `int`)
* `date_max` (`datetime.datetime` or `int`)
* `min_players` (`int`)
* `account_id` (`int`)
* `league_id` (`int`)
* `start_at_match_id` (`int`)
* `matches_requested` (`int`)
* `tournament_games_only` (`int`)

### `Dota2API.get_match_details(match_id, **params)`

> Gets details of a match given its id

Arguments
* `match_id` (`int`)

### `Dota2API.get_league_listing(**params)`

> Gets list of leagues

### `Dota2API.get_live_league_games(**params)`

> Gets list of live league games

