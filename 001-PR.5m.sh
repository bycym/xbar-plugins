#!/bin/bash

GITHUB_APIKEY=""
AUTHOR=""
ORG=""
REPOSITORY=""
CLOSED_PRS="https://github.com/${ORG}/${REPOSITORY}/pulls?q=is%3Apr+author:${AUTHOR}+is:closed"
PR_QUERY="?q=type:pr+is:open+author:${AUTHOR}+sort:updated-desc"
# echo "curl -s -u ${GITHUB_APIKEY}:x-oauth-basic https://api.github.com/search/issues${PR_QUERY} -H Accept: application/vnd.github.v3+json"
PR_COMMAND_RESULT=$(curl -s -u "${GITHUB_APIKEY}:x-oauth-basic" "https://api.github.com/search/issues${PR_QUERY}" -H "Accept: application/vnd.github.v3+json" | \
	/opt/homebrew/bin/jq -r '.items[] | (.title) + " :: "+ (.repository_url | split("/") | .[5])+ " |href="+ (.html_url)')
echo "PR"
echo "---"
echo "Updated on: $(date +%m/%d/%Y~%H:%m)"
echo "Closed PRs |href=${CLOSED_PRS}"
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
echo "assignee: | href=https://github.com/issues/${ASSIGNED_QUERY}"
echo "---"
(
	IFS=$'\n'
	for PRs in "$ASSIGNED_COMMAND_RESULT"; do
	 	echo "${PRs}"
	done 
)

REVIEW_QUERY=?q=is%3Apr+review-requested:${AUTHOR}+is:open+archived:false
#echo "curl -s -u ${GITHUB_APIKEY}:x-oauth-basic https://api.github.com/search/issues${QUERY} -H Accept: application/vnd.github.v3+json"
REVIEW_COMMAND_RESULT=$(curl -s -u "${GITHUB_APIKEY}:x-oauth-basic" "https://api.github.com/search/issues${REVIEW_QUERY}" -H "Accept: application/vnd.github.v3+json" | \
	/opt/homebrew/bin/jq -r '.items[] | (.title) + " :: "+ (.repository_url | split("/") | .[5])+ " |href="+ (.html_url)')
echo "---"
echo "Waiting for review: | href=https://github.com/issues/${REVIEW_QUERY}"
echo "---"
(
	IFS=$'\n'
	for PRs in "$REVIEW_COMMAND_RESULT"; do
	 	echo "${PRs}"
	done 
)

echo "---"
echo "Refresh... | refresh=true"