#!/bin/sh

# Installs git-conventional-commits https://github.com/qoomon/git-conventional-commits
npm install --global git-conventional-commits

# Sets the hooks path to .git-hooks/ folder, which contain client side validation rules for git commits
git config core.hooksPath .git-hooks
