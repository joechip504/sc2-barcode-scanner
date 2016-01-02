# Until I fix init file, this will play nice with django shell
import sys
from main.lib_sc2 import tree
sys.modules['tree'] = tree

# from project root directory (inside venv)
# python manage.py shell < main/lib_sc2/update_tournament_data.py
from main.lib_sc2.api import SC2BarcodeScannerAPI
SC2BarcodeScannerAPI().add_tournament_replay_directory('main/static/main/tournament_replays/')