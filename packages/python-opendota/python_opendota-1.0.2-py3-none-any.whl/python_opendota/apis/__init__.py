
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from python_opendota.api.benchmarks_api import BenchmarksApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from python_opendota.api.benchmarks_api import BenchmarksApi
from python_opendota.api.constants_api import ConstantsApi
from python_opendota.api.distributions_api import DistributionsApi
from python_opendota.api.explorer_api import ExplorerApi
from python_opendota.api.find_matches_api import FindMatchesApi
from python_opendota.api.health_api import HealthApi
from python_opendota.api.hero_stats_api import HeroStatsApi
from python_opendota.api.heroes_api import HeroesApi
from python_opendota.api.leagues_api import LeaguesApi
from python_opendota.api.live_api import LiveApi
from python_opendota.api.matches_api import MatchesApi
from python_opendota.api.metadata_api import MetadataApi
from python_opendota.api.parsed_matches_api import ParsedMatchesApi
from python_opendota.api.players_api import PlayersApi
from python_opendota.api.players_by_rank_api import PlayersByRankApi
from python_opendota.api.pro_matches_api import ProMatchesApi
from python_opendota.api.pro_players_api import ProPlayersApi
from python_opendota.api.public_matches_api import PublicMatchesApi
from python_opendota.api.rankings_api import RankingsApi
from python_opendota.api.records_api import RecordsApi
from python_opendota.api.replays_api import ReplaysApi
from python_opendota.api.request_api import RequestApi
from python_opendota.api.scenarios_api import ScenariosApi
from python_opendota.api.schema_api import SchemaApi
from python_opendota.api.search_api import SearchApi
from python_opendota.api.status_api import StatusApi
from python_opendota.api.teams_api import TeamsApi
