#!/bin/sh
set -e

if [[ -n "$SSH_PRIVATE_KEY" ]]
then
  mkdir -p /root/.ssh
  echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa
  chmod 600 /root/.ssh/id_rsa
fi

mkdir -p ~/.ssh
cp /root/.ssh/* ~/.ssh/ 2> /dev/null || true

git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
git config --global user.name "github-actions[bot]"

python3 -m pip install requests
python3 /main.py