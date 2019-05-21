import json
from typing import Union

import pytest
from discord import Embed

import udyr_bot
from udyr_bot.commands.summoner_info import RiotGamesDAO


class MockResponse:
    def __init__(self, data: Union[dict, list, str, int,], status_code):
        self.text = json.dumps(data)
        self.json_ = data
        self.status_code = status_code

    def json(self):
        return self.json_


def test_get_summoner_info(monkeypatch):
    def mock_get(url, params=None):

        if url == 'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/dongerdingo':
            return MockResponse({
                "id": "iB-f3Dvos8LRyZM9bt0BhEJu6_3fiSk2G3GHJ-yKe_EwCMw",
                "accountId": "6mM7kS266PzEEW6XHC2-O7d3Ca1j7SXf4QDRJpWA9fwj5A",
                "puuid": "3HUWC1Ufug8vI8eEQ6CX1cPqLl6f5R-OgZSk7OTd6eDrGsHcKSF0yhkYT3ImI_4KoBsY9xUtgWFjRw",
                "name": "Donger Dingo",
                "profileIconId": 3478,
                "revisionDate": 1558185036000,
                "summonerLevel": 93
            }, 200)

        elif url == 'https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/' \
                    'iB-f3Dvos8LRyZM9bt0BhEJu6_3fiSk2G3GHJ-yKe_EwCMw':
            return MockResponse([
                {
                    "leagueId": "4b0e39d0-1fa1-11e9-8d9f-0649c773fbaf",
                    "queueType": "RANKED_SOLO_5x5",
                    "tier": "PLATINUM",
                    "rank": "III",
                    "summonerId": "iB-f3Dvos8LRyZM9bt0BhEJu6_3fiSk2G3GHJ-yKe_EwCMw",
                    "summonerName": "Donger Dingo",
                    "leaguePoints": 0,
                    "wins": 18,
                    "losses": 19,
                    "veteran": False,
                    "inactive": False,
                    "freshBlood": False,
                    "hotStreak": False
                }
            ], 200)

    dao = RiotGamesDAO(None)
    monkeypatch.setattr(dao.session, 'get', mock_get)

    args = 'donger dingo --region EUNE'.split()
    res: Embed = dao.get_summoner_info(args)

    if isinstance(res, str):
        pytest.fail(f'Expected to find `Embed` object. Found `str` instead. {res}')

    assert res.title == 'Ranked Info for Donger Dingo'
    assert res.description == 'Ranked Solo - PLATINUM III - 0 LP - 18 wins - 19 losses'


def test_get_summoner_info_nonexistant(monkeypatch):
    def mock_get(url, params=None):
        if url == 'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/unkownqweqwklehj':
            return MockResponse({
                "status": {
                    "message": "Data not found - summoner not found",
                    "status_code": 404
                }
            }, 404)

    dao = RiotGamesDAO(None)
    monkeypatch.setattr(dao.session, 'get', mock_get)

    monkeypatch.setattr(udyr_bot.commands.summoner_info.requests, 'get', mock_get)

    args = 'unkownqweqwklehj --region EUNE'.split()
    res: Embed = dao.get_summoner_info(args)

    assert isinstance(res, str)
