import json
import math
import statistics
import os
from datetime import datetime

def read_file(filename):
  with open(filename, "r") as f:
    return json.loads(f.read())

def get_pr_lifetimes(prs, label = None):
  lifetimes = []
  date_format = '%Y-%m-%dT%H:%M:%SZ'
  for pr in prs:
    labels = list(map(lambda x: x["name"], pr['labels']))
    if pr['merged_at'] and (label == None or label in labels):
      created_at = datetime.strptime(pr['created_at'], date_format)
      merged_at = datetime.strptime(pr['merged_at'], date_format)
      pr_seconds_open = (merged_at - created_at).total_seconds()
      lifetimes.append(pr_seconds_open)
  lifetimes.sort()
  return lifetimes

def display_seconds_as_duration(seconds):
  hours, remainder = divmod(seconds, 60 * 60)
  minutes, seconds = divmod(remainder, 60)
  return '{:2} hours {:2} minutes {:2} seconds'.format(int(hours), int(minutes), int(seconds))

def main(label):
  filename = 'prs.json'
  prs = read_file(filename)
  lifetimes = get_pr_lifetimes(prs, label)
  median = statistics.median(lifetimes)
  mean = statistics.mean(lifetimes)
  stdev = statistics.stdev(lifetimes)
  print(len(lifetimes))
  print('median: ', display_seconds_as_duration(median))
  print('mean: ', display_seconds_as_duration(mean))
  print('stdev: ', display_seconds_as_duration(stdev))
  print('min: ', display_seconds_as_duration(lifetimes[0]))
  print('max: ', display_seconds_as_duration(lifetimes[-1]))

if __name__ == '__main__':
  label = os.getenv('LABEL')
  main(label)