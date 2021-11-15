import requests
import json
import os

BASE_URL = 'https://api.github.com'

def get_file():
  return open('prs.json', 'w')


def fetch_prs_page(user, token, owner, repo, page):
  resp = requests.get(f'{BASE_URL}/repos/{owner}/{repo}/pulls?state=closed&per_page=100&page={page}', auth=(user,token))
  return resp.json()

def run(user, token, owner, repo):
  total_prs = []
  writer = get_file()
  for page in range(0, 15):
    print(f'fetching page {page}')
    pr_page = fetch_prs_page(user, token, owner, repo, page)
    print(f'page {page} retrived')
    total_prs.extend(pr_page)
  writer.write(json.dumps(total_prs))

if __name__ == '__main__':
  user = os.getenv('USER')
  token = os.getenv('TOKEN')
  user_repo = os.getenv('REPO')
  [owner, repo] = user_repo.split(':')
  run(user, token, owner, repo)