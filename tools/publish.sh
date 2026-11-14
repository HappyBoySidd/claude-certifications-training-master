#!/usr/bin/env bash
# Build, gate and stage the site. Pipeline P7 in the project's CREW-WORKFLOW.md.
# It never pushes by itself: push after gate G10 passes (standing approval from the site owner).
#
#   CERT_SRC="<study workspace path>" tools/publish.sh
set -euo pipefail
cd "$(dirname "$0")/.."
: "${CERT_SRC:?Set CERT_SRC to the study workspace path}"

echo "== 1/6 blocklist (hashes of private names)"
python3 tools/make_blocklist.py --src "$CERT_SRC"

echo "== 2/6 build docs/ and export the page sources to content/"
python3 site/build.py --src "$CERT_SRC" --export content
python3 tools/build_practice.py --src "$CERT_SRC"

echo "== 3/6 gate G9 (NFR-01 to NFR-10)"
python3 tools/gate.py

echo "== 3a/6 CCAR-F objective coverage and presentation check (B63-FX-7, regression guard under FX-14)"
python3 tools/objective_check.py --src "$CERT_SRC"

echo "== 3b/6 hanging-reference check (fails the build on any hit)"
cr="$CERT_SRC/10-Learning-Site/private/ccar-f-study-site"
saved=/tmp/check_refs_dump.pw.json
if [ -f "$cr/check_refs.py" ]; then
  # Same rule as gate.py: a Playwright render saved by pw_jobs.py counts only if neither page changed since.
  if [ -f "$saved" ] && [ -f "$cr/site/index.html" ] && [ -f "$cr/../index.html" ] \
     && [ ! "$cr/site/index.html" -nt "$saved" ] && [ ! "$cr/../index.html" -nt "$saved" ]; then
    python3 "$cr/check_refs.py" --dump "$saved"
  else
    python3 "$cr/check_refs.py"
  fi
else
  echo "check_refs.py not found under CERT_SRC; refusing to continue"; exit 1
fi

echo "== 4/6 the repo alone rebuilds the same site (handover check)"
tmp="$(mktemp -d)"
python3 site/build.py --src content --out "$tmp/docs" >/dev/null
diff -rq docs "$tmp/docs" || { echo "content/ does not rebuild docs/ exactly; fix before committing"; exit 1; }
echo "identical"

echo "== 5/6 stage by explicit path"
chmod +x .githooks/pre-commit tools/publish.sh  # copies from Drive lose the executable bit; git skips a non-executable hook
git add README.md CHANGELOG.md CONTRIBUTING.md HANDOVER.md MAINTAINING.md .gitignore .githooks site tools docs content practice assessment .github
git status --short

echo "== 6/6 ready-to-push checks (backlog, seats, plans)"
ready=1
python3 tools/backlog_check.py --src content --manifest "$CERT_SRC/.project.md" --changelog "$CERT_SRC/CHANGELOG.md" ${BACKLOG_ALLOW:+--allow "$BACKLOG_ALLOW"} || ready=0
python3 "$CERT_SRC/.claude/agents/check_seats.py" || ready=0
if [ -f "$CERT_SRC/13-Plans/plan_check.py" ]; then
  python3 "$CERT_SRC/13-Plans/plan_check.py" || ready=0
else
  echo "plan_check.py not found under CERT_SRC; not ready to push"; ready=0
fi

cat <<'EOF'

Next:
  preview:  python3 -m http.server -d docs 8000   then open http://localhost:8000
  review:   the changed pages (gates G7 and G8), then write the CHANGELOG entry
  commit:   git commit -m "vX.Y: <what changed>"   (the pre-commit hook reruns the gate)
  tag:      git tag -a vX.Y -m "vX.Y: <title from CHANGELOG>"
  push:     once G10 passes:  git push --follow-tags origin master
  live:     https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/
EOF

if [ "$ready" -eq 0 ]; then
  echo
  echo "NOT READY TO PUSH: a ready-to-push check failed (backlog, seats or plans; see above). Preview and review are fine."
  echo "Approved backlog exception only: BACKLOG_ALLOW=\"B-12\" CERT_SRC=... tools/publish.sh"
  exit 1
fi
