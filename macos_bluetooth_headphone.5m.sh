#!/bin/bash

# Define device and cache location
DEVICE_NAME="WH-1000XM4"
CACHE_DIR="$(dirname "$0")/not"
CACHE_FILE="$CACHE_DIR/${DEVICE_NAME}.cache"

# Make sure cache dir exists
mkdir -p "$CACHE_DIR"

# Initialize found flag

output=$(pmset -g accps | grep $DEVICE_NAME)
#macos_batt=$(pmset -g batt | sed -nE 's/.*\t([0-9]+%)\;.*; ([0-9]+:[0-9]+) remaining.*/\1 \2/p')
macos_batt=$(pmset -g batt | sed -nE 's/.*; ([0-9]+:[0-9]+) remaining.*/\1/p')
# Use grep and regex to extract percentage, e.g., 40%
percentage=$(echo "$output" | grep -o '[0-9]\{1,3\}%')

# Check if percentage was found
if [ -n "$percentage" ]; then
  echo "🎧 $percentage"
  echo "$percentage" > "$CACHE_FILE"
else
  if [[ -f "$CACHE_FILE" ]]; then
    cached_percent=$(cat "$CACHE_FILE")
    echo "🎧 $cached_percent"
    echo "---"
    echo "cached"
  else
    echo "🎧 ❌"
  fi
fi

echo "---"
echo "Headphone: $DEVICE_NAME"
echo "Refresh... | refresh=true"
echo "---"
echo $macos_batt remaining

REGEX="^\ -([^\ ]+)[^\t]*\t([0-9]+%)"

# pmset -g accps | while IFS= read -r line; do
#   if [[ "$line" =~ $REGEX ]]; then
#     name="${BASH_REMATCH[1]}"
#     percent="${BASH_REMATCH[2]}"
#     echo "$name :: $percent"
#   fi
# done
