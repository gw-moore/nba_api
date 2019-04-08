import time

import pytest
import numpy as np

import nba_api.stats.endpoints as ep

# Create a version of an endpoint that defers evaluation.
def endpoint_tester(endpoint_class, **kwargs):
    def run():
        return endpoint_class(**kwargs)
    return run

# Once we run the test to call the endpoints, we'll cache the responses here.
called_eps = []

# A bunch of valid but uninstantiated endpoints for testing:
@pytest.fixture
def endpoints():
    eps = [ endpoint_tester(ep.AssistLeaders),
            endpoint_tester(ep.AssistTracker),
            endpoint_tester(ep.BoxScoreAdvancedV2, game_id='0021700807'),
            endpoint_tester(ep.BoxScoreDefensive, game_id='0021700807'),
            endpoint_tester(ep.BoxScoreFourFactorsV2, game_id='0021700807'),
            endpoint_tester(ep.BoxScoreMatchups, game_id='0021700807'),
            endpoint_tester(ep.BoxScoreMiscV2, game_id='0021700807'),
            endpoint_tester(ep.BoxScorePlayerTrackV2, game_id='0021700807'),
            endpoint_tester(ep.BoxScoreScoringV2, game_id='0021700807'),
            endpoint_tester(ep.BoxScoreSummaryV2, game_id='0021700807'),
            endpoint_tester(ep.BoxScoreTraditionalV2, game_id='0021700807'),
            endpoint_tester(ep.BoxScoreUsageV2, game_id='0021700807'),
            endpoint_tester(ep.CommonAllPlayers),
            endpoint_tester(ep.CommonPlayerInfo, player_id='2544'),
            endpoint_tester(ep.CommonPlayoffSeries),
            endpoint_tester(ep.CommonTeamRoster, team_id='1610612739'),
            endpoint_tester(ep.CommonTeamYears),
            endpoint_tester(ep.DefenseHub, season='2017-18'),
            endpoint_tester(ep.DraftCombineDrillResults),
            endpoint_tester(ep.DraftCombineNonStationaryShooting),
            endpoint_tester(ep.DraftCombinePlayerAnthro),
            endpoint_tester(ep.DraftCombineSpotShooting),
            endpoint_tester(ep.DraftCombineStats),
            endpoint_tester(ep.DraftHistory),
            endpoint_tester(ep.FantasyWidget),
            endpoint_tester(ep.FranchiseHistory),
            endpoint_tester(ep.FranchiseLeaders, team_id='1610612739'),
            endpoint_tester(ep.FranchisePlayers, team_id='1610612739'),
            endpoint_tester(ep.HomePageLeaders),
            endpoint_tester(ep.HomePageV2),
            endpoint_tester(ep.InfographicFanDuelPlayer, game_id='0021700807'),
            endpoint_tester(ep.LeadersTiles),
            endpoint_tester(ep.LeagueDashLineups),
            endpoint_tester(ep.LeagueDashPlayerBioStats),
            endpoint_tester(ep.LeagueDashPlayerClutch),
            endpoint_tester(ep.LeagueDashPlayerPtShot),
            endpoint_tester(ep.LeagueDashPlayerShotLocations),
            endpoint_tester(ep.LeagueDashPlayerStats),
            endpoint_tester(ep.LeagueDashPtDefend),
            endpoint_tester(ep.LeagueDashPtStats),
            endpoint_tester(ep.LeagueDashPtTeamDefend),
            endpoint_tester(ep.LeagueDashTeamClutch),
            endpoint_tester(ep.LeagueDashTeamPtShot),
            endpoint_tester(ep.LeagueDashTeamShotLocations),
            endpoint_tester(ep.LeagueDashTeamStats),
            endpoint_tester(ep.LeagueGameFinder),
            endpoint_tester(ep.LeagueGameLog),
            endpoint_tester(ep.LeagueLeaders),
            endpoint_tester(ep.LeaguePlayerOnDetails, team_id='1610612739'),
            endpoint_tester(ep.LeagueSeasonMatchups, off_player_id_nullable=2544,
                def_player_id_nullable='1610612739'),
            endpoint_tester(ep.LeagueStandings),
            endpoint_tester(ep.PlayByPlay, game_id='0021700807'),
            endpoint_tester(ep.PlayByPlayV2, game_id='0021700807'),
            endpoint_tester(ep.PlayerAwards, player_id='2544'),
            endpoint_tester(ep.PlayerCareerStats, player_id='2544'),
            endpoint_tester(ep.PlayerCompare, player_id_list='202681,203078,2544,201567,203954',
                    vs_player_id_list='201566,201939,201935,201142,203076'),
            endpoint_tester(ep.PlayerDashPtPass, player_id='2544', team_id='1610612739'),
            endpoint_tester(ep.PlayerDashPtReb, player_id='2544', team_id='1610612739'),
            endpoint_tester(ep.PlayerDashPtShotDefend, player_id='2544',
                    team_id='1610612739'),
            endpoint_tester(ep.PlayerDashPtShots, player_id='2544', team_id='1610612739'),
            endpoint_tester(ep.PlayerDashboardByClutch, player_id='2544'),
            endpoint_tester(ep.PlayerDashboardByGameSplits, player_id='2544'),
            endpoint_tester(ep.PlayerDashboardByGeneralSplits, player_id='2544'),
            endpoint_tester(ep.PlayerDashboardByLastNGames, player_id='2544'),
            endpoint_tester(ep.PlayerDashboardByOpponent, player_id='2544'),
            endpoint_tester(ep.PlayerDashboardByShootingSplits, player_id='2544'),
            endpoint_tester(ep.PlayerDashboardByTeamPerformance, player_id='2544'),
            endpoint_tester(ep.PlayerDashboardByYearOverYear, player_id='2544'),
            endpoint_tester(ep.PlayerFantasyProfile, player_id='2544'),
            endpoint_tester(ep.PlayerFantasyProfileBarGraph, player_id='2544'),
            endpoint_tester(ep.PlayerGameLog, player_id='2544'),
            endpoint_tester(ep.PlayerGameStreakFinder),
            endpoint_tester(ep.PlayerNextNGames, player_id='2544'),
            endpoint_tester(ep.PlayerProfileV2, player_id='2544'),
            endpoint_tester(ep.PlayerVsPlayer, player_id='2544', vs_player_id='202681'),
            endpoint_tester(ep.PlayoffPicture),
            endpoint_tester(ep.Scoreboard),
            endpoint_tester(ep.ScoreboardV2),
            endpoint_tester(ep.ShotChartDetail, player_id='2544', team_id='1610612739'),
            endpoint_tester(ep.ShotChartLineupDetail),
            endpoint_tester(ep.TeamAndPlayersVsPlayers,
                    team_id=1610612739,
                    player_id1=203954,
                    player_id2=201567,
                    player_id3=203507,
                    player_id4=203078,
                    player_id5=202681,
                    vs_team_id=1610612765,
                    vs_player_id1=203954,
                    vs_player_id2=201567,
                    vs_player_id3=203507,
                    vs_player_id4=203078,
                    vs_player_id5=202681),
            endpoint_tester(ep.TeamDashLineups, team_id='1610612739'),
            endpoint_tester(ep.TeamDashPtPass, team_id='1610612739'),
            endpoint_tester(ep.TeamDashPtReb, team_id='1610612739'),
            endpoint_tester(ep.TeamDashPtShots, team_id='1610612739'),
            endpoint_tester(ep.TeamDashboardByClutch, team_id='1610612739'),
            endpoint_tester(ep.TeamDashboardByGameSplits, team_id='1610612739'),
            endpoint_tester(ep.TeamDashboardByGeneralSplits, team_id='1610612739'),
            endpoint_tester(ep.TeamDashboardByLastNGames, team_id='1610612739'),
            endpoint_tester(ep.TeamDashboardByOpponent, team_id='1610612739'),
            endpoint_tester(ep.TeamDashboardByShootingSplits, team_id='1610612739'),
            endpoint_tester(ep.TeamDashboardByTeamPerformance, team_id='1610612739'),
            endpoint_tester(ep.TeamDashboardByYearOverYear, team_id='1610612739'),
            endpoint_tester(ep.TeamDetails, team_id='1610612739'),
            endpoint_tester(ep.TeamGameLog, team_id='1610612739'),
            endpoint_tester(ep.TeamGameStreakFinder),
            endpoint_tester(ep.TeamHistoricalLeaders, team_id='1610612739'),
            endpoint_tester(ep.TeamInfoCommon, team_id='1610612739'),
            endpoint_tester(ep.TeamPlayerDashboard, team_id='1610612739'),
            endpoint_tester(ep.TeamPlayerOnOffDetails, team_id='1610612739'),
            endpoint_tester(ep.TeamPlayerOnOffSummary, team_id='1610612739'),
            endpoint_tester(ep.TeamVsPlayer, team_id='1610612739', vs_player_id='2544'),
            endpoint_tester(ep.TeamYearByYearStats, team_id='1610612739'),
            endpoint_tester(ep.VideoDetails, player_id='2544', game_id='0021700807',
                    team_id='1610612739', start_period=1, end_period=1),
            endpoint_tester(ep.VideoEvents, game_id='0021700807'),
            endpoint_tester(ep.VideoStatus),
            endpoint_tester(ep.WinProbabilityPBP, game_id='0021700807')]
    return eps

def test_valid_endpoints(endpoints):
    '''This test will only fail if we try to import an invalid endpoint.'''
    return endpoints

def test_endpoints_run(endpoints):
    '''Test that all the endpoints are callable.
    
    This takes a very, very long time (10-20 minutes) because we don't want to
    barrage the NBA site with requests.'''
    for ep in endpoints:
        # Delay briefly.
        wait = np.random.gamma(shape=9, scale=0.4)
        time.sleep(wait)
        # Call the API.
        called_ep = ep()
        called_eps.append(called_ep)
    assert len(called_eps) == len(endpoints)

def test_valid_json():
    # Check that every called endpoint is valid json.
    valid = [ep.nba_response.valid_json() for ep in called_eps]
    assert all(valid)
