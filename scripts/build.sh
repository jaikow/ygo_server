parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

cd "$parent_path"

source ../.venv/bin/activate
pip3 intall -f ../requirements.txt