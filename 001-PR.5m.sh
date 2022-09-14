#!/bin/bash

# Expire Thu, Sep 1 2022.
GITHUB_APIKEY="GITHUB_APIKEY"
AUTHOR="AUTHOR"
PR_QUERY="?q=type:pr+is:open+author:${AUTHOR}+sort:updated-desc"
# echo "curl -s -u ${GITHUB_APIKEY}:x-oauth-basic https://api.github.com/search/issues${PR_QUERY} -H Accept: application/vnd.github.v3+json"
PR_COMMAND_RESULT=$(curl -s -u "${GITHUB_APIKEY}:x-oauth-basic" "https://api.github.com/search/issues${PR_QUERY}" -H "Accept: application/vnd.github.v3+json" | \
	/opt/homebrew/bin/jq -r '.items[] | (.title) + " :: "+ (.repository_url | split("/") | .[5])+ " |href="+ (.html_url)')
echo "PR"
echo "---"
echo "author:"
echo "---"
(
	IFS=$'\n'
	for PRs in "$PR_COMMAND_RESULT"; do
	 	echo "${PRs}"
	done 
)

ASSIGNED_QUERY="?q=type:pr+is:open+assignee:${AUTHOR}+sort:updated-desc"
#echo "curl -s -u ${GITHUB_APIKEY}:x-oauth-basic https://api.github.com/search/issues${QUERY} -H Accept: application/vnd.github.v3+json"
ASSIGNED_COMMAND_RESULT=$(curl -s -u "${GITHUB_APIKEY}:x-oauth-basic" "https://api.github.com/search/issues${ASSIGNED_QUERY}" -H "Accept: application/vnd.github.v3+json" | \
	/opt/homebrew/bin/jq -r '.items[] | (.title) + " :: "+ (.repository_url | split("/") | .[5])+ " |href="+ (.html_url)')
echo "---"
echo "assignee:"
echo "---"
(
	IFS=$'\n'
	for PRs in "$ASSIGNED_COMMAND_RESULT"; do
	 	echo "${PRs}"
	done 
)
echo "---"
echo "Refresh... | refresh=true"