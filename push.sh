#!/usr/bin/env bash
# One-shot setup + push helper.
# Usage:
#   ./push.sh <github-username> <repo-name> ["Your Name"] [you@email.com]
# Example:
#   ./push.sh sukoji awesome-self-evolving-agents "Suko Jim" sukoji@users.noreply.github.com
#
# Prereqs: create an EMPTY repo on GitHub first (no README/license), and have
# git authentication set up (gh auth login, or a credential helper / PAT).
set -euo pipefail

OWNER="${1:?usage: ./push.sh <owner> <repo> [\"Your Name\"] [email]}"
REPO="${2:?usage: ./push.sh <owner> <repo> [\"Your Name\"] [email]}"
NAME="${3:-}"
EMAIL="${4:-}"

echo ">> filling in repository links (OWNER/REPO -> ${OWNER}/${REPO})"
grep -rl 'OWNER/REPO' . --exclude-dir=.git | while read -r f; do
  sed -i.bak "s|OWNER/REPO|${OWNER}/${REPO}|g" "$f" && rm -f "${f}.bak"
done

if [ -n "$NAME" ]; then
  first="${NAME%% *}"; last="${NAME##* }"
  sed -i.bak "s|YOUR_FIRST_NAME|${first}|; s|YOUR_LAST_NAME|${last}|" CITATION.cff && rm -f CITATION.cff.bak
  git config user.name "$NAME"
fi
[ -n "$EMAIL" ] && git config user.email "$EMAIL"

echo ">> committing substitutions"
git add -A
git commit -q -m "Configure repository links for ${OWNER}/${REPO}" || echo "   (nothing to commit)"

if [ -n "$NAME" ] && [ -n "$EMAIL" ]; then
  echo ">> rewriting commit authorship to ${NAME} <${EMAIL}>"
  git rebase -r --root --exec 'git commit --amend --reset-author --no-edit' >/dev/null 2>&1 || \
    echo "   (skipped author rewrite; you can amend manually)"
fi

echo ">> connecting remote and pushing"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${OWNER}/${REPO}.git"
git branch -M main
git push -u origin main

echo ""
echo "Done -> https://github.com/${OWNER}/${REPO}"
