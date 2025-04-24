#!/bin/bash


# Get the actual uptime string from macOS
uptime_str=$(uptime)

# Extract number of days if present
days=$(echo "$uptime_str" | grep -oE '[0-9]+ days' | grep -oE '[0-9]+')

# If no days found, assume 0 (less than a day)
if [ -z "$days" ]; then
  days=0
fi

# Compose the message
msg="$days days"
emoji="📊"

# Add epic emoji progression
if (( days >= 60 )); then
  msg+=" 👑 Champion 2 Month"
  emoji="👑"  
elif (( days >= 30 )); then
  msg+=" 🏆 1 Month"
  emoji="🏆"  
elif (( days >= 21 )); then
  msg+=" 🛡️ Week 3"
  emoji="🛡️"
elif (( days >= 14 )); then
  msg+=" ⚔️ Week 2"
  emoji="⚔️"
elif (( days >= 7 )); then
  msg+=" 🔥 Week 1"
  emoji="🔥"
else
  msg+=" 🐣 Just Hatched"
  emoji="🐣"
fi


echo "$emoji"
echo "---"
echo "$msg uptime"
echo "Refresh... | refresh=true"

