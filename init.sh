#!/bin/bash

REPO_OWNER="Jessiebrig"
REPO_NAME="OmniSetup"

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
    echo "Failed to fetch branches. Defaulting to main."
    BRANCHES="main"
fi

# Display branches with last commit info
echo ""
echo "Available branches:"
i=1
declare -A branch_map

# main first
if echo "$BRANCHES" | grep -q '^main$'; then
    commit_data=$(curl -sL "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/commits/main")
    commit_msg=$(echo "$commit_data" | grep -m1 '"message":' | cut -d'"' -f4 | head -c 50)
    commit_date=$(echo "$commit_data" | grep '"date":' | head -1 | cut -d'"' -f4 | cut -dT -f1)
    [[ ${#commit_msg} -eq 50 ]] && commit_msg="${commit_msg}..."
    echo "  $i) main - $commit_msg ($commit_date)"
    branch_map[$i]="main"
    ((i++))
fi

# other branches alphabetically
while IFS= read -r branch; do
    [[ -z "$branch" || "$branch" == "main" ]] && continue
    commit_data=$(curl -sL "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/commits/$branch")
    commit_msg=$(echo "$commit_data" | grep -m1 '"message":' | cut -d'"' -f4 | head -c 50)
    commit_date=$(echo "$commit_data" | grep '"date":' | head -1 | cut -d'"' -f4 | cut -dT -f1)
    [[ ${#commit_msg} -eq 50 ]] && commit_msg="${commit_msg}..."
    echo "  $i) $branch - $commit_msg ($commit_date)"
    branch_map[$i]="$branch"
    ((i++))
done <<< "$(echo "$BRANCHES" | grep -v '^main$' | sort)"

echo ""
echo -n "Select branch [1]: " > /dev/tty
read -r choice < /dev/tty
choice=${choice:-1}

SELECTED_BRANCH="${branch_map[$choice]:-}"
if [[ -z "$SELECTED_BRANCH" ]]; then
    echo "Invalid choice. Defaulting to main."
    SELECTED_BRANCH="main"
fi

echo ""
echo "Selected: $SELECTED_BRANCH"
echo ""

# Download setup.sh from selected branch and run it
mkdir -p omnisetup
echo -n "Downloading setup.sh... "
curl -fsSL "https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/refs/heads/$SELECTED_BRANCH/setup.sh" -o omnisetup/setup.sh && echo "✓" || { echo "✗"; exit 1; }

export INSTALLER_BRANCH="$SELECTED_BRANCH"
exec < /dev/tty
cd omnisetup && bash setup.sh
