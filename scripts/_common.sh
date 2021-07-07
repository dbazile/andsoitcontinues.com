cd "$(dirname $(dirname $0))"

if [[ ! -d venv ]]; then
	python3 -m venv venv

	echo -e "\033[30;43m create virtual environment \033[0m"
	source venv/bin/activate
	pip install -r requirements.txt
fi

source venv/bin/activate
