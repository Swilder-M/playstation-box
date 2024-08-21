import os

from psn import PSN
from utils import (
    convert_play_duration, duration_sorter, generate_bar_chart,
    truncate_strings, update_gist, update_github_repo_secret
)

npsso = os.environ.get('PSN_NPSSO')
psn_access_token = os.environ.get('PSN_ACCESS_TOKEN')
psn_refresh_token = os.environ.get('PSN_REFRESH_TOKEN')
github_token = os.environ.get('GH_TOKEN')
github_repo = os.environ.get('GITHUB_REPOSITORY')
gist_id = os.environ.get('GIST_ID')


if __name__ == '__main__':
    psn_client = PSN(npsso=npsso, access_token=psn_access_token, refresh_token=psn_refresh_token)
    update_github_repo_secret(repo=github_repo, github_token=github_token,
                              secret_records={
                                  'PSN_ACCESS_TOKEN': psn_client.access_token,
                                  'PSN_REFRESH_TOKEN': psn_client.refresh_token
                              })
    show_records = []
    for game in psn_client.game_list():
        play_duration = convert_play_duration(game.get('playDuration'))
        if play_duration == '0 mins':
            continue

        trophy_progress = psn_client.game_trophy_progress(game['titleId'])
        if not trophy_progress:
            continue

        record = {
            'name': game['name'],
            'playDuration': play_duration,
            'definedTrophiesTotal': sum(trophy_progress['definedTrophies'].values()),
            'earnedTrophiesTotal': sum(trophy_progress['earnedTrophies'].values())
        }
        record['progress'] = int(record['earnedTrophiesTotal'] / record['definedTrophiesTotal'] * 100)
        show_records.append(record)
    show_records.sort(key=duration_sorter, reverse=True)
    gist_content = ''
    for record in show_records[:20]:
        line = [
            truncate_strings(record['name'], 17).ljust(18),
            record['playDuration'].ljust(16),
            generate_bar_chart(record['progress'], 13),
            str(record['progress']).rjust(2) + '%'
        ]
        line = ' '.join(line)
        gist_content += line + '\n'
    update_gist(gist_id, github_token, gist_content.strip())
