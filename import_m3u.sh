#!/bin/bash

# Variables
SOURCE_REPO="jsosao/m3u"
SOURCE_FILE="mylist.m3u8"
SOURCE_BRANCH="main"
DEST_REPO="git@github.com:zeknewbe/porong.git"
DEST_PATH="mylist.m3u8"   # Path where you want the file to be in the destination repo

# Setup Git configuration
GIT_EMAIL="visionintegral@gmail.com"
GIT_NAME="zeknewbe"

# Clone destination repo
echo "Cloning destination repository..."
git clone "$DEST_REPO" dest-repo && cd dest-repo

# Add source repo as a remote and fetch the file
echo "Adding source repository as remote..."
git remote add source_repo "https://github.com/$SOURCE_REPO.git"
git fetch source_repo $SOURCE_BRANCH

# Checkout the specific file from source repo
echo "Checking out file from source repository..."
git checkout source_repo/$SOURCE_BRANCH -- "$SOURCE_FILE"

# Configure Git
echo "Setting up Git configuration..."
git config user.email "$GIT_EMAIL"
git config user.name "$GIT_NAME"

# Check for changes
echo "Checking for changes..."
if [[ `git status --porcelain` ]]; then
    echo "Changes detected, committing the file..."
    git add "$SOURCE_FILE"
    git commit -m "Imported $SOURCE_FILE from $SOURCE_REPO"
    echo "Pushing changes to the repository..."
    git push origin main
    echo "File imported successfully!"
else
    echo "No changes detected, nothing to commit."
fi

# Cleanup by removing the added remote
git remote remove source_repo
