#!/bin/bash

REPO_OWNER="Jessiebrig"
REPO_NAME="OmniSetup"
SCRIPT_NAME="setup.sh"

clear
echo ""
echo "┌─────────────────────────────────┐"
echo "│  OmniSetup - Universal Setup    │"
echo "└─────────────────────────────────┘"
echo ""

# Fetch available branches
echo "Fetching available branches..."
BRANCHES=$(curl -sL "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/branches" | grep '"name":' | cut -d'"' -f4)

if [[ -z "$BRANCHES" ]]; then
    echo "Error: Failed to fetch branches. Check your internet connection."
    exit 1
fi

# Display branches with last commit info
echo ""
echo "Available branches:"
i=1
declare -A branch_map

# main first
if echo "$BRANCHES" | grep -q '^main$'; then
    commit_data=$(curl -sL "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/commits/main")
    commit_msg=$(echo "$commit_data" | grep -m1 '"message":' | cut -d'"' -f4 | head -c 40)
    commit_datetime=$(echo "$commit_data" | grep '"date":' | head -1 | cut -d'"' -f4)
    commit_date=$(date -d "$commit_datetime" '+%Y-%m-%d' 2>/dev/null || echo "$commit_datetime" | cut -dT -f1)
    commit_time=$(date -d "$commit_datetime" '+%H:%M' 2>/dev/null || echo "$commit_datetime" | cut -dT -f2 | cut -d':' -f1,2)
    [[ ${#commit_msg} -eq 40 ]] && commit_msg="${commit_msg}..."
    echo "  $i) main - $commit_msg ($commit_date $commit_time)"
    branch_map[$i]="main"
    ((i++))
fi

# other branches alphabetically
while IFS= read -r branch; do
    [[ -z "$branch" || "$branch" == "main" ]] && continue
    commit_data=$(curl -sL "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/commits/$branch")
    commit_msg=$(echo "$commit_data" | grep -m1 '"message":' | cut -d'"' -f4 | head -c 40)
    commit_datetime=$(echo "$commit_data" | grep '"date":' | head -1 | cut -d'"' -f4)
    commit_date=$(date -d "$commit_datetime" '+%Y-%m-%d' 2>/dev/null || echo "$commit_datetime" | cut -dT -f1)
    commit_time=$(date -d "$commit_datetime" '+%H:%M' 2>/dev/null || echo "$commit_datetime" | cut -dT -f2 | cut -d':' -f1,2)
    [[ ${#commit_msg} -eq 40 ]] && commit_msg="${commit_msg}..."
    echo "  $i) $branch - $commit_msg ($commit_date $commit_time)"
    branch_map[$i]="$branch"
    ((i++))
done <<< "$(echo "$BRANCHES" | grep -v '^main$' | sort)"

# Get user choice
echo "" > /dev/tty
echo -n "Select branch [1]: " > /dev/tty
read -r choice < /dev/tty
choice=${choice:-1}

SELECTED_BRANCH="${branch_map[$choice]:-}"
if [[ -z "$SELECTED_BRANCH" ]]; then
    echo "Invalid choice. Defaulting to main."
    SELECTED_BRANCH="${branch_map[1]}"
fi

echo ""
echo "Selected: $SELECTED_BRANCH"
echo ""

# Download setup.sh from selected branch
SCRIPT_URL="https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/$SELECTED_BRANCH/$SCRIPT_NAME"

echo -n "Downloading setup.sh... "
if curl -sL "$SCRIPT_URL" -o "$SCRIPT_NAME" 2>/dev/null; then
    echo "✓"
else
    echo "✗"
    echo "Error: Failed to download setup.sh"
    exit 1
fi

# Verify file exists and has content
if [[ ! -f "$SCRIPT_NAME" ]] || [[ ! -s "$SCRIPT_NAME" ]]; then
    echo "Error: setup.sh is empty or missing"
    exit 1
fi

exec < /dev/tty
export INSTALLER_BRANCH="$SELECTED_BRANCH"
bash "$SCRIPT_NAME"
