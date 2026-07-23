#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_root="${repo_root}/skills/find-china-cdc-health-report"
dist_dir="${repo_root}/dist"
stage_dir="$(mktemp -d)"

cleanup() {
  rm -rf "${stage_dir}"
}
trap cleanup EXIT

python3 "${repo_root}/scripts/validate_skill.py"
python3 -m unittest discover -s "${repo_root}/tests" -v

mkdir -p "${dist_dir}"
rm -f "${dist_dir}/skill.zip" "${dist_dir}/SHA256SUMS"

cp "${skill_root}/SKILL.md" "${stage_dir}/SKILL.md"
cp -R "${skill_root}/agents" "${stage_dir}/agents"
cp -R "${skill_root}/references" "${stage_dir}/references"
cp -R "${skill_root}/scripts" "${stage_dir}/scripts"

find "${stage_dir}" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "${stage_dir}" -type f \( -name "*.pyc" -o -name ".DS_Store" \) -delete

(
  cd "${stage_dir}"
  zip -q -r "${dist_dir}/skill.zip" SKILL.md agents references scripts
)

first_entry="$(unzip -Z1 "${dist_dir}/skill.zip" | head -n 1)"
if [[ "${first_entry}" != "SKILL.md" ]]; then
  echo "skill.zip must contain SKILL.md at its root" >&2
  exit 1
fi

if unzip -Z1 "${dist_dir}/skill.zip" | grep -Eq '(^|/)(artifacts|tests|docs|__pycache__)(/|$)|\.pyc$|\.DS_Store$'; then
  echo "skill.zip contains excluded development or runtime files" >&2
  exit 1
fi

(
  cd "${dist_dir}"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum skill.zip > SHA256SUMS
  else
    shasum -a 256 skill.zip > SHA256SUMS
  fi
)

echo "Created ${dist_dir}/skill.zip"
echo "Created ${dist_dir}/SHA256SUMS"
