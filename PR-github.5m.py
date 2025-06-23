#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
import datetime
import time
from requests.auth import HTTPBasicAuth
import json
from base64 import b64encode

# ######## CONFIG ########################################################################################
CACHE_FILE="not/PR-github.cache"
GITHUB_APIKEY=""
AUTHOR=""
ORG=""
GITHUB_TEAMMEMBERS=["teamMember1", "teamMember2"]
###########################################################################################################


if not GITHUB_APIKEY or not AUTHOR or not ORG:
  print("PR 💀")
  print("---")
  print("Missing variables. 💀")
  exit(0)

PR_SCRIPT_OUTPUT = []
PR_QUERY=f"?q=type:pr+is:open+author:{AUTHOR}+sort:updated-desc"
ASSIGNED_QUERY=f"?q=type:pr+is:open+assignee:{AUTHOR}+sort:updated-desc"
TEAM_REVIEW_QUERY=f"?q=is%3Apr+review-requested:{AUTHOR}+is:open+archived:false+draft:false+{''.join(str(f'author:{x}+') for x in GITHUB_TEAMMEMBERS)}"
REVIEW_QUERY=f"?q=is%3Apr+review-requested:{AUTHOR}+is:open+archived:false"

def fallback():
  with open(CACHE_FILE, "r") as f:
    stored_feed = f.read()
  if(len(stored_feed) > 0):
    print(stored_feed)
  else:
    print ("No cache...")  

# Authorization token: we need to base 64 encode it 
# and then decode it to acsii as python 3 stores it as a byte string
def basic_auth(username, password):
  token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
  return f'Basic {token}'

def put(array, string):
  array.append("%s" % (string))

def createRequest(url):
  result = []
  headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Connection': 'keep-alive',
    'Authorization': f"{basic_auth(GITHUB_APIKEY, 'x-oauth-basic')}",
    'User-Agent': 'Python'
  }

  try:
    response = requests.request("GET", url, headers=headers)
    responseJSON = json.loads(response.text)    
  except:
    print("PR 💀")
    print("---")
    print("Couldn't parse response. 💀")
    print(f"url: {url}. 💀")
    # print(f"message: {response.text}. 💀")
    fallback()
    exit(0)

  for line in responseJSON['items']:
    put(result,f"{line['title']} :: ({line['repository_url'].rsplit('/', 1)[-1]}) [{line['user']['login']}] | href='{line['html_url']}'")

  return result


def createdPRQuery():
  url=f'https://api.github.com/search/issues{PR_QUERY}'
  return createRequest(url)
def assignedQuery():
  url=f'https://api.github.com/search/issues{ASSIGNED_QUERY}'
  return createRequest(url)
def teamReviewQuery():
  url=f'https://api.github.com/search/issues{TEAM_REVIEW_QUERY[:-1]}'
  return createRequest(url)
def reviewQuery():
  url=f'https://api.github.com/search/issues{REVIEW_QUERY}'
  return createRequest(url)

PRArray = createdPRQuery()
assignedArray = assignedQuery()
teamReviewArray = teamReviewQuery()
reviewArray = reviewQuery()

PR_SCRIPT_OUTPUT = [ f"🌱PR ({len(teamReviewArray)})" ]
put(PR_SCRIPT_OUTPUT, '---')
put(PR_SCRIPT_OUTPUT, f"Updated on: {time.ctime()}")
put(PR_SCRIPT_OUTPUT, 'Refresh... | refresh=true')
# ##### Created PRs #########################################
put(PR_SCRIPT_OUTPUT, "---")
put(PR_SCRIPT_OUTPUT, "📄 author:")
put(PR_SCRIPT_OUTPUT, "---")
PR_SCRIPT_OUTPUT += PRArray
# ##### Assigned PRs ########################################
put(PR_SCRIPT_OUTPUT, '---')
put(PR_SCRIPT_OUTPUT, f"assignee ({len(assignedArray)}): | href=https://github.com/issues/{ASSIGNED_QUERY}")
put(PR_SCRIPT_OUTPUT, "---")
PR_SCRIPT_OUTPUT += assignedArray
# ##### Waiting for teammate review ##################################
put(PR_SCRIPT_OUTPUT, '---')
put(PR_SCRIPT_OUTPUT, f"👪 Waiting for team review ({len(teamReviewArray)}): | href=https://github.com/issues/{TEAM_REVIEW_QUERY[:-1]}")
put(PR_SCRIPT_OUTPUT, "---")
PR_SCRIPT_OUTPUT += teamReviewArray
# ##### Waiting for review ##################################
put(PR_SCRIPT_OUTPUT, '---')
put(PR_SCRIPT_OUTPUT, f"👀 Waiting for review ({len(reviewArray)}): | href=https://github.com/issues/{REVIEW_QUERY}")
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
