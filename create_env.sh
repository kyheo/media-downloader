#!/bin/bash

REQ_FILE='doc/requirements.txt'

ENV=$1

if [[ -z $ENV ]]
then
    ENV="dev_env"
fi

if [[ -d $ENV ]]
then
    echo "- Deleting old $ENV environment directory."
    rm -Rf $ENV
fi

echo "- Creating new $ENV environment."
virtualenv $ENV
source $ENV/bin/activate
echo "- Installing BeautifulSoup required to install Periscope (yes)."
pip install BeautifulSoup
echo "- Installing required packages from requirements file ($REQ_FILE)."
pip install -r $REQ_FILE
deactivate

echo "- Adding $ENV environment directory to .gitignore."
echo $ENV >> .gitignore

echo "- Creating $ENV start_env.sh file."
echo "-- To start the environment $ . ./start_env.sh"
echo "-- To stop the environment ($ENV)$ deactivate"
echo "source $ENV/bin/activate" > start_env.sh
chmod u+x start_env.sh
