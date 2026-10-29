#
# Helper function for mise bash tasks 
#

function info() {
	echo -e "\e[34m$1\e[0m"
}

function check_for_error() {
	if [ ${2:-0} -ne 0 ]; then
		echo -e "\e[31m$1\e[0m";
		exit 1
	else
		echo -e "\e[32mSuccess\e[0m"
	fi
}

# The reference the changes are computed against (same as the CI and utils/ tools)
BASE_REF="origin/develop"

function check_base_ref() {
	if ! git rev-parse --verify -q "$BASE_REF" >/dev/null; then
		echo -e "\e[31m$BASE_REF not found. Please run 'git fetch origin develop:refs/remotes/origin/develop'\e[0m";
		exit 1
	fi
}

# Untracked files are invisible to `git diff`, so the formats they belong to would be skipped
function check_untracked_files() {
	local untracked
	untracked=$(git ls-files --others --exclude-standard | grep -vE '^(doc/|utils/|\.)' | grep -E '^[^/]+/[^/]+/')
	if [ -n "$untracked" ]; then
		echo -e "\e[31mUntracked files are ignored by the checks. Please run 'git add -N <file>' on:\e[0m";
		echo "$untracked"
		exit 1
	fi
}

# NUL-separated list of the files changed against $BASE_REF, deleted files excluded
function changed_files() {
	git diff --name-only -z --diff-filter=d "$BASE_REF"
}

# Newline-separated list of the paths changed against $BASE_REF, deleted files included,
# as selected by the `--changes` option of the utils/ tools
function changed_paths() {
	git diff --name-only "$BASE_REF"
}
