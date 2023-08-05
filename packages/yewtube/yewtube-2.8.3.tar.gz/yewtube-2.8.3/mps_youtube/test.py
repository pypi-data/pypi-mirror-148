import pafy
from youtubesearchpython import *
playlist = pafy.get_playlist('PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
old = Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')

print(playlist)

