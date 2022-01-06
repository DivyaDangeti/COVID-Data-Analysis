SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd "$SCRIPTPATH"
cd ..
source venv/bin/activate
python covid_analysis/main.py

