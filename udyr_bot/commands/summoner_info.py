from enum import Enum
from logging import getLogger
from typing import List

import requests
from discord import Colour, Embed

from ..constants import RIOT_DEV_API_KEY

log = getLogger(__name__)

riot_api_params = {
    'api_key': RIOT_DEV_API_KEY
}


class Region(Enum):
    BR = 'BR'
    EUNE = 'EUNE'
    EUW = 'EUW'
    JP = 'JP'
    KR = 'KR'
    LAN = 'LAN'
    LAS = 'LAS'
    NA = 'NA'
    OCE = 'OC'
    TR = 'TR'
    RU = 'RU'

    @classmethod
    def from_str(cls, str_):
        try:
            return cls(str_)
        except ValueError:
            return None


class RiotAPIDomain(Enum):
    EUNE = 'eun1.api.riotgames.com'
    EUW = 'euw1.api.riotgames.com'
    NA = 'na1.api.riotgames.com'
    BR = 'br1.api.riotgames.com'
    JP = 'jp1.api.riotgames.com'
    KR = 'kr.api.riotgames.com'
    LAN = 'la1.api.riotgames.com'
    LAS = 'la2.api.riotgames.com'
    OCE = 'oc1.api.riotgames.com'
    TR = 'tr1.api.riotgames.com'
    RU = 'ru.api.riotgames.com'

    @classmethod
    def get_domain(cls, region: Region):
        if region == Region.EUNE:
            return cls.EUNE.value

        if region == Region.EUW:
            return cls.EUW.value

        if region == Region.NA:
            return cls.NA.value

        if region == Region.BR:
            return cls.BR.value

        if region == Region.JP:
            return cls.JP.value

        if region == Region.KR:
            return cls.KR.value

        if region == Region.LAN:
            return cls.LAN.value

        if region == Region.LAS:
            return cls.LAS.value

        if region == Region.OCE:
            return cls.OCE.value

        if region == Region.TR:
            return cls.TR.value

        if region == Region.RU:
            return cls.RU.value

        return None


class SummonerDTO:
    """Represents a summoner"""

    def __init__(self, profile_icon_id, name, puuid, summoner_level, revision_date, id, account_id):
        self.profile_icon_id = profile_icon_id
        self.name = name
        self.puuid = puuid
        self.summoner_level = summoner_level
        self.revision_date = revision_date
        self.id = id
        self.account_id = account_id

    @classmethod
    def from_json(cls, data):
        return cls(data['profileIconId'], data['name'],
                   data['puuid'], data['summonerLevel'],
                   data['revisionDate'], data['id'],
                   data['accountId'])

    def __str__(self):
        return (f'SummonerDTO(profileIconId={self.profile_icon_id}, name={self.name}, '
                f'puuid={self.puuid}, summoner_level={self.summoner_level}, '
                f'revision_date={self.revision_date}, id={self.id}, '
                f'account_id={self.account_id})')


class LeagueEntryDTO:
    """Information on a ranked queue"""

    def __init__(self, queue_type, summoner_name, hot_streak, mini_series,
                 wins, veteran, losses, rank, league_id, inactive, fresh_blood,
                 tier, summoner_id, league_points):
        self.queue_type: str = queue_type
        self.summoner_name: str = summoner_name
        self.hot_streak: bool = hot_streak
        self.mini_series = mini_series
        self.wins: int = wins
        self.veteran: bool = veteran
        self.losses: int = losses
        self.rank: str = rank
        self.league_id: str = league_id
        self.inactive: bool = inactive
        self.fresh_blood: bool = fresh_blood
        self.tier: str = tier
        self.summoner_id: str = summoner_id
        self.league_points: int = league_points

    @classmethod
    def from_json(cls, data):
        return cls(data['queueType'], data['summonerName'], data['hotStreak'],
                   data.get('miniSeries', None), data['wins'], data['veteran'],
                   data['losses'], data['rank'], data['leagueId'], data['inactive'],
                   data['freshBlood'], data['tier'], data['summonerId'],
                   data['leaguePoints'])

    def pretty(self):

        if self.queue_type == 'RANKED_SOLO_5x5':
            type_ = 'Ranked Solo'
        elif self.queue_type == 'RANKED_FLEX_SR':
            type_ = 'Ranked Flex SR'
        else:
            return None
        return f'{type_} - {self.tier} {self.rank} - {self.league_points} LP - {self.wins} wins - {self.losses} losses'

    def __str__(self):
        return (f'LeagueEntryDTO(queueType={self.queue_type}, summonerName={self.summoner_name}, '
                f'hotStreak={self.hot_streak}, miniSeries={self.mini_series}, '
                f'wins={self.wins}, losses={self.losses}, veteran={self.veteran}, '
                f'tier={self.tier}, rank={self.rank}, leaguePoints={self.league_points}')


class BannedChampion:
    def __init__(self, pick_turn, champion_id, team_id):
        self.pick_turn: int = pick_turn
        self.champion_id: int = champion_id
        self.team_id: int = team_id

    @classmethod
    def from_json(cls, data):
        return cls(data['pickTurn'], data['championId'], data['teamId'])

    def __str__(self):
        return f'BannedChampion(pick_turn={self.pick_turn}, champion_id={self.champion_id})'


class Observer:
    def __init__(self, encryption_key):
        self.encryption_key = encryption_key

    @classmethod
    def from_json(cls, data):
        return cls(data['encryptionKey'])

    def __str__(self):
        return f'Observer(encrypton_key={self.encryption_key})'


class CurrentGameParticipant:

    def __init__(self, profile_icon_id, champion_id, summoner_name, team_id, spell1_id, spell2_id, summoner_id):
        self.profile_icon_id: int = profile_icon_id
        self.champion_id: int = champion_id
        self.summoner_name: str = summoner_name
        self.team_id: int = team_id
        self.spell1_id: int = spell1_id
        self.spell2_id: int = spell2_id
        self.summoner_id: str = summoner_id

    @classmethod
    def from_json(cls, data):
        return cls(data['profileIconId'], data['championId'], data['summonerName'],
                   data['teamId'], data['spell1Id'], data['spell2Id'], data['summonerId'])

    def __str__(self):
        return (f'{self.summoner_name} | {self.champion_id} | '
                f'{self.spell1_id} | {self.spell2_id}')


class CurrentGameInfo:
    def __init__(self, game_id, game_start_time, platform_id, game_mode, map_id, game_type, banned_champions,
                 observers, participants, game_len, game_queue_config_id):
        self.game_id: int = game_id
        self.game_start_time: int = game_start_time
        self.platform_id: str = platform_id
        self.game_mode: str = game_mode
        self.map_id: int = map_id
        self.game_type: str = game_type
        self.banned_champions: List[BannedChampion] = [
            BannedChampion.from_json(entry) for entry in banned_champions]
        self.observers: Observer = Observer.from_json(observers)
        self.participants: List[CurrentGameParticipant] = [CurrentGameParticipant.from_json(entry) for
                                                           entry in participants]
        self.game_len: int = game_len
        self.game_queue_config_id: int = game_queue_config_id

    @classmethod
    def from_json(cls, data):
        return cls(data['gameId'], data['gameStartTime'], data['platformId'],
                   data['gameMode'], data['mapId'], data['gameType'], data['bannedChampions'],
                   data['observers'], data['participants'], data['gameLength'], data['gameQueueConfigId'])

    def __str__(self):
        str_participants = '\n'.join([str(part) for part in self.participants])
        return (f'game_mode={self.game_mode}, game_len={self.game_len}\n'
                f'{str_participants}')


def get_username_region(msg: List[str]) -> (str, Region):
    if '--region' in msg:
        index = msg.index('--region')
        region = Region.from_str(msg[index+1])
        username = ''.join(msg[:index])
    else:
        region: Region = Region.EUNE
        username: str = ''.join(msg)
    return username, region


def get_summoner_info(msg: List[str]):
    username, region = get_username_region(msg)

    if username == '':
        return 'Please provide a username'
    if region is None:
        return 'Please provide a valid region'

    log.info(f'Getting summoner info for region={region}, username={username}')

    base_url = RiotAPIDomain.get_domain(region)

    summoner_info_url = f'https://{base_url}/lol/summoner/v4/summoners/by-name/{username}'
    summoner_info_res = requests.get(summoner_info_url, params=riot_api_params)

    if summoner_info_res.status_code == 404:
        return f'Summoner {username} on region={region.value} was not found'

    if summoner_info_res.status_code != 200:
        log.error(
            f'Error when connecting to the Riot Games API. res.text={summoner_info_res.text}')
        return f'Error when connecting to the Riot Games API.'

    summoner = SummonerDTO.from_json(summoner_info_res.json())

    encrypted_id = summoner.id

    league_info_url = f'https://{base_url}/lol/league/v4/entries/by-summoner/{encrypted_id}'
    league_info_res = requests.get(league_info_url, params=riot_api_params)

    if league_info_res.status_code == 404:
        return f'Summoner {username} does not have any ranked queue entries'
    if league_info_res.status_code != 200:
        log.error(
            f'Error when connecting to the Riot Games API. res.text={summoner_info_res.text}')
        return f'Error when connecting to the Riot Games API.'

    league_info_set = []

    for entry in league_info_res.json():
        league_info_set.append(LeagueEntryDTO.from_json(entry))

    res_ = []
    try:
        for entry in league_info_set:
            entry_str = entry.pretty()
            if entry_str is None:
                continue

            if entry_str.startswith('Ranked Solo'):
                res_.insert(0, entry_str)
            else:
                res_.append(entry_str)

        if len(res_) == 0:
            return f'Summoner {summoner.name} has not played ranked on {region.value}'

        return f'Ranked Info for Summoner {summoner.name}\n' + '\n'.join(res_)
    except Exception as e:
        log.error(f'Exception, e={e}')


def get_game_info(msg: List[str]):
    username, region = get_username_region(msg)
    if username == '':
        return 'Please provide a username'
    if region is None:
        return 'Please provide a valid region'

    log.info(f'Getting game info for region={region}, username={username}')

    base_url = RiotAPIDomain.get_domain(region)

    summoner_info_url = f'https://{base_url}/lol/summoner/v4/summoners/by-name/{username}'
    summoner_info_res = requests.get(summoner_info_url, params=riot_api_params)

    if summoner_info_res.status_code == 404:
        return f'Summoner {username} on region={region.value} was not found'

    if summoner_info_res.status_code != 200:
        log.error(
            f'Error when connecting to the Riot Games API. res.text={summoner_info_res.text}')
        return f'Error when connecting to the Riot Games API.'

    summoner = SummonerDTO.from_json(summoner_info_res.json())

    encrypted_id = summoner.id
    game_info_url = f'https://{base_url}/lol/spectator/v4/active-games/by-summoner/{encrypted_id}'
    game_info_res = requests.get(game_info_url, params=riot_api_params)

    if game_info_res.status_code == 404:
        return f'Summoner {summoner.name} is not currently in a game'
    if game_info_res.status_code != 200:
        log.error(
            f'Error when connecting to the Riot Games API. res.text={game_info_res.text}')
        return f'Error when connecting to the Riot Games API.'

    curr_game: CurrentGameInfo = CurrentGameInfo.from_json(
        game_info_res.json())

    participants = []

    for part in curr_game.participants:
        str_ = f'`| {part.summoner_name} | {part.champion_id} | {part.spell1_id} | {part.spell2_id} |`'
        if part.team_id == 100:
            participants.insert(0, str_)
        else:
            participants.append(str_)

    participants.insert(0, '`| Summoner Name | Champion ID | Spell 1 ID | Spell 2 ID |`')

    res_str = '\n'.join(participants)

    embed_res = Embed(colour=Colour.dark_green(),
                      title=f'Game summary for {summoner.name}',
                      description=res_str)
    return embed_res
