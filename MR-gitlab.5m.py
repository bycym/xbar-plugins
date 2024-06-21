#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
import datetime
import time
from requests.auth import HTTPBasicAuth
import json
from base64 import b64encode

# ######## CONFIG ########################################################################################
CACHE_FILE="not/MR-gitlab.cache"
GITLAB_TOKEN=""
AUTHOR_ID="" # user id
AUTHOR=""
ORG=""
HOST=""
###########################################################################################################


if not GITLAB_TOKEN or not AUTHOR or not ORG or not AUTHOR_ID:
  print("MR 💀")
  print("---")
  print('Refresh... | refresh=true')
  print("Missing variables. 💀")
  exit(0)

MERGE_REQUEST_API=f"{HOST}/api/v4/merge_requests"

PR_SCRIPT_OUTPUT = []
CLOSED_QUERY=f"{HOST}/{ORG}/dashboard/merge_requests?author_username={AUTHOR}&draft=no&scope=all&sort=closed_at&state=merged"
CREATED_QUERY=f"?author_id={AUTHOR_ID}&state=opened&order_by=updated_at&sort=desc"
REVIEW_QUERY=f"?scope=all&state=opened&reviewer_username={AUTHOR}&not[author_username]={AUTHOR}&not[approved_by_usernames][]={AUTHOR}&order_by=updated_at&sort=desc"
ASSIGNED_QUERY=f"?scope=assigned_to_me"

def fallback():
  with open(CACHE_FILE, "r") as f:
    stored_feed = f.read()
  if(len(stored_feed) > 0):
    print('\n'.join(stored_feed))
  else:
    print ("No cache...")  

def put(array, string):
  array.append("%s" % (string))

def createRequest(url):
  result = []
  headers = {
    'PRIVATE-TOKEN': f"{GITLAB_TOKEN}",
  }

  try:
    response = requests.request("GET", url, headers=headers, timeout=3)
    responseJSON = json.loads(response.text)    
  except Exception as e:
    print("MR 💀")
    print("---")
    print('Refresh... | refresh=true')
    print("Couldn't parse response. 💀")
    print(f"url: {url}. 💀")
    fallback()
    # print(e)
    # print(f"message: {response.text}. 💀")
    exit(0)
  for line in responseJSON:
    put(result,f"{line['title']} :: ({line['references']['full'].rsplit('/', 1)[-1]}) | href='{line['web_url']}'")

  return result


def createdPRQuery():
  url=f'{MERGE_REQUEST_API}{CREATED_QUERY}'
  return createRequest(url)
def assignedQuery():
  url=f'{MERGE_REQUEST_API}{ASSIGNED_QUERY}'
  return createRequest(url)
def reviewQuery():
  url=f'{MERGE_REQUEST_API}{REVIEW_QUERY}'
  return createRequest(url)

PRArray = createdPRQuery()
assignedArray = assignedQuery()
reviewArray = reviewQuery()

PR_SCRIPT_OUTPUT = [ f"🌱MR ({len(reviewArray)})" ]
put(PR_SCRIPT_OUTPUT, '---')
put(PR_SCRIPT_OUTPUT, f"Updated on: {time.ctime()}")
put(PR_SCRIPT_OUTPUT, f"Closed MRs |href={CLOSED_QUERY}")
put(PR_SCRIPT_OUTPUT, 'Refresh... | refresh=true')
# ##### Created PRs #########################################
put(PR_SCRIPT_OUTPUT, "---")
put(PR_SCRIPT_OUTPUT, "✍️ author:")
put(PR_SCRIPT_OUTPUT, "---")
PR_SCRIPT_OUTPUT += PRArray
# ##### Assigned PRs ########################################
put(PR_SCRIPT_OUTPUT, '---')
put(PR_SCRIPT_OUTPUT, f"⚓️ assignee ({len(assignedArray)}): | href={HOST}/dashboard/merge_requests/{ASSIGNED_QUERY}")
put(PR_SCRIPT_OUTPUT, "---")
PR_SCRIPT_OUTPUT += assignedArray
# ##### Waiting for review ##################################
put(PR_SCRIPT_OUTPUT, '---')
put(PR_SCRIPT_OUTPUT, f"👀 Waiting for review ({len(reviewArray)}): | href={HOST}/dashboard/merge_requests/{REVIEW_QUERY}")
put(PR_SCRIPT_OUTPUT, "---")
PR_SCRIPT_OUTPUT += reviewArray

content = '\n'.join(PR_SCRIPT_OUTPUT)
print(content)

with open(CACHE_FILE, "w+") as f:
  f.write(content)
  f.write("\n---\n")
  f.write("cached\n")
  f.write(time.ctime())
  f.close()
