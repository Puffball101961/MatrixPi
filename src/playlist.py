from datetime import datetime

def getPlaylist(playlistConfig, time):
    # Get the playlist that matches the current time, if no playlists have a matching time, return the default playlist's plugins and interval
    for playlist in playlistConfig.config['playlists']:
        start_time = datetime.strptime(playlist['startTime'], "%H:%M").time()
        end_time = datetime.strptime(playlist['endTime'], "%H:%M").time()

        if start_time <= end_time:
            if start_time <= time <= end_time:
                return playlist['plugins'], playlist['changeEvery']
        else:  # Handles the case where the time range wraps around midnight
            if time >= start_time or time <= end_time:
                return playlist['plugins'], playlist['changeEvery']
    