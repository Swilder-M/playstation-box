import os

from psn import PSN
from utils import (
    clean_game_name, convert_play_duration, duration_sorter, generate_bar_chart,
    truncate_strings, update_gist, update_github_repo_secret
)

npsso = os.environ.get('PSN_NPSSO')
psn_access_token = os.environ.get('PSN_ACCESS_TOKEN')
psn_refresh_token = os.environ.get('PSN_REFRESH_TOKEN')
github_token = os.environ.get('GH_TOKEN')
github_repo = os.environ.get('GITHUB_REPOSITORY')
gist_id = os.environ.get('GIST_ID')


if __name__ == '__main__':
    print('Fetching PlayStation data...')
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
            'name': clean_game_name(game['name']),
            'playDuration': play_duration,
            'definedTrophiesTotal': sum(trophy_progress['definedTrophies'].values()),
            'earnedTrophiesTotal': sum(trophy_progress['earnedTrophies'].values())
        }
        record['progress'] = int(record['earnedTrophiesTotal'] / record['definedTrophiesTotal'] * 100)
        show_records.append(record)
    show_records.sort(key=duration_sorter, reverse=True)

    print(f'Found {len(show_records)} games with play history')
    print(f'\nTop {min(20, len(show_records))} games by play time:')
    print('-' * 55)
    gist_content = ''
    for record in show_records[:20]:
        line = [
            truncate_strings(record['name'], 17).ljust(17),
            record['playDuration'].rjust(16),
            generate_bar_chart(record['progress'], 13),
            str(record['progress']).rjust(3) + '%'
        ]
        line = ' '.join(line)
        print(line)
        gist_content += line + '\n'
    print('-' * 55)

    print('\nUpdating gist...')
    update_gist(gist_id, github_token, gist_content.strip())
    print('Done!')
