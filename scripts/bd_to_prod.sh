#!/usr/bin/env bash
set -Eeo pipefail

setup_git() {
    git config --global user.email "no-reply@build.com"
    git config --global user.name "CircleCI"
    git checkout master
    # Avoid version failure
    git stash
}

push_tags() {
    git push origin master --tags
}

echo ".____                  .__                  .__        ";
echo "|    |    __ __  _____ |__| ____   ____     |__| ____  ";
echo "|    |   |  |  \/     \|  |/ ___\ /  _ \    |  |/  _ \ ";
echo "|    |___|  |  /  Y Y  \  / /_/  >  <_> )   |  (  <_> )";
echo "|_______ \____/|__|_|  /__\___  / \____/ /\ |__|\____/ ";
echo "        \/           \/  /_____/         \/            ";
echo
echo "Deploy lumigo-log-shipper to pypi server"

setup_git

pip install wheel

echo "Create package"
python setup.py bdist_wheel

echo "Getting latest changes from git"
latest_tag="$(git describe --tags --abbrev=0)"
changes=$(git log "${latest_tag}..HEAD" --oneline)

bumpversion patch --message "{current_version} → {new_version}. Changes: ${changes}"

echo "Uploading to PyPi"
pip install twine
twine upload dist/*

push_tags
echo "Done"