import webbrowser
from urllib.parse import quote

rwr_uri = "steam://rungameid/270150//"
rwr_cmd = ["package=media/packages/CB7",
           "map=media/packages/vanilla/maps/map2",
           "verbose", "debugmode", "metagame_debugmode", "big_water"]
webbrowser.open_new(f"{rwr_uri}{'%20'.join(quote(c, safe='') for c in rwr_cmd)}")
