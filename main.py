# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Create  : 2021/5/23 2:22
# @Update  : 2021/5/23 2:22
# @Detail  :
import json
import os
import re
import subprocess
import sys

import requests

from config import *

if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)
hashtable_path = os.path.join(TEMP_PATH, 'hashtable')
repo_path = os.path.join(TEMP_PATH, 'out')


def run_shell(shell, cwd):
    cmd = subprocess.Popen(shell, cwd=cwd, stdin=subprocess.PIPE, stderr=sys.stderr, close_fds=True,
                           stdout=sys.stdout, universal_newlines=True, shell=True, bufsize=1)

    cmd.communicate()
    return cmd.returncode


def get_hero_list():
    response = requests.get(HERO_LIST)
    hero_list = response.json()
    version = hero_list['version']
    with open(os.path.join(repo_path, 'champions.json'), encoding='utf-8') as f:
        data = json.load(f)
    if version != data['version']:
        champion_path = os.path.join(repo_path, 'champions')
        if not os.path.exists(champion_path):
            os.makedirs(champion_path)
        res = []
        for item in hero_list['hero']:
            res.append(
                {"heroId": item["heroId"],
                 "name": item["name"],
                 "alias": item["alias"],
                 "title": item["title"],
                 "square": CHAMPION_SQUARE.format(name=item["alias"]),
                 "selectAudio": item['selectAudio'],
                 "banAudio": item['banAudio'],
                 "keywords": item['keywords'], }
            )
            this = get_champion_info(item['alias'])
            this.update(
                {
                    "version": version,
                    # "changeLabel": item['changeLabel'],
                }
            )
            with open(os.path.join(champion_path, f'{item["alias"]}.json'), 'w+', encoding='utf-8') as f:
                json.dump(this, f, ensure_ascii=False)

        with open(os.path.join(repo_path, 'champions.json'), 'w+', encoding='utf-8') as f:
            json.dump({
                'version': version,
                'data': res
            }, f, ensure_ascii=False)
        return version
    else:
        print('无更新')


def filter_skin(a, b, name, tid):
    res = []
    for i in b:
        _id = str(int(i['id'].replace(tid, '', 1)))
        if _id in a:
            i['image'] = CHAMPION_SKIN.format(id=i['id'])
            i['hash'] = HASHTABLE_CDN.format(name=name.lower(), id=_id)
            res.append(
                i
            )
    return res


def get_champion_info(name):
    version = requests.get(RIOT_VERSION).json()[0]
    url = RIOT_CHAMPION.format(version=version, name=name)
    if 'FiddleSticks' in url:
        name = 'Fiddlesticks'
        url = url.replace('FiddleSticks', 'Fiddlesticks')
    data = requests.get(url).json()['data']
    this = data[name]
    this['image'] = CHAMPION_SQUARE.format(name=name)
    this['skins'] = filter_skin(get_skins(name), this['skins'], this['id'], this['key'])
    del this['lore']
    del this['tags']
    del this['partype']
    del this['info']
    del this['stats']
    del this['spells']
    del this['passive']
    del this['recommended']
    return this


def get_skins(name):
    def sort_key(s):
        number = re.compile(r'\d+').findall(s)
        return int(number[0]) if number else -1

    path = os.path.join(hashtable_path, 'VO', 'zh_CN', 'characters', name.lower())
    ids = [re.compile(r'(\d+)(\.json)?').findall(i)[0][0] for i in os.listdir(path)]
    return list(sorted(ids, key=sort_key))


def sync(version):
    run_shell('git add .', repo_path)
    run_shell(f'git commit -m \'{version}\'', repo_path)
    run_shell(f'git tag \'data-{version}\'', repo_path)
    run_shell(f'git push origin data:data --force --tags', repo_path)


if __name__ == '__main__':
    run_shell(f'git clone {HASHTABLE_REPO} {hashtable_path}', TEMP_PATH)
    run_shell(f'git clone {THIS_REPO} {repo_path} -b data', TEMP_PATH)

    if v := get_hero_list():
        sync(v)
