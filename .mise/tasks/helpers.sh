#
# Helper function for mise bash tasks 
#

function info() {
	echo -e "\e[34m$1\e[0m"
}

function check_for_error() {
	if [ $2 != 0 ]; then
		echo -e "\e[31m$1\e[0m";
		exit 1
	else
		echo -e "\e[32mSuccess\e[0m"
	fi
}
