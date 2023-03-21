from base64 import b64encode

import requests
from nacl import encoding, public


def convert_play_duration(duration_str):
    if not duration_str:
        return '0 mins'
    duration_str = duration_str.replace('PT', '')
    duration_str = duration_str.replace('S', ' secs')
    duration_str = duration_str.replace('M', ' mins ')
    duration_str = duration_str.replace('H', ' hrs ')
    if 'mins' not in duration_str:
        if 'hrs' not in duration_str:
            return '0 mins'
        duration_str = duration_str.split('hrs')[0] + 'hrs'
    else:
        duration_str = duration_str.split('mins')[0] + 'mins'
    return duration_str.strip()


def duration_sorter(item):
    duration = item['playDuration']
    hrs = 0
    mins = 0
    if 'hrs' in duration:
        hrs = int(duration.split('hrs')[0].strip())

    if 'mins' in duration:
        mins = int(duration.split('mins')[0].strip().split(' ')[-1])

    return hrs * 60 + mins


def generate_bar_chart(percent, size):
    percent = int(percent)
    syms = '░▏▎▍▌▋▊▉█'

    frac = (size * 8 * percent) // 100
    bars_full = frac // 8
    if bars_full >= size:
        return syms[8:9] * size
    semi = frac % 8

    return (syms[8:9] * bars_full) + syms[semi:semi+1] + syms[0:1] * (size - bars_full - 1)


def truncate_strings(strings, length):
    strings = strings.strip()
    if len(strings) > length:
        return strings[:length - 3] + '...'
    else:
        return strings


def update_gist(gist_id, github_token, content):
    url = f'https://api.github.com/gists/{gist_id}'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {github_token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    data = {
        'files': {
            'playstation-box': {
                'content': content
            }
        }
    }
    resp = requests.patch(url, headers=headers, json=data)
    if resp.status_code != 200:
        raise Exception(f'Failed to update gist: {resp.status_code} {resp.text}')


def update_github_repo_secret(repo, github_token, secret_records):
    request_headers = {
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization': f'Bearer {github_token}'
    }
    public_key_info = requests.get(
        url=f'https://api.github.com/repos/{repo}/actions/secrets/public-key',
        headers=request_headers
    ).json()
    public_key = public.PublicKey(public_key_info['key'].encode('utf-8'), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)

    url = f'https://api.github.com/repos/{repo}/actions/secrets/'
    for k, v in secret_records.items():
        encrypted = sealed_box.encrypt(v.encode('utf-8'))
        data = {
            'encrypted_value': b64encode(encrypted).decode('utf-8'),
            'key_id': public_key_info['key_id']
        }
        resp = requests.put(url + k, headers=request_headers, json=data)
        if resp.status_code >= 400:
            raise Exception(f'Failed to update secret: {resp.status_code} {resp.text}')
