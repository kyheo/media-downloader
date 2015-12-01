# If you use virtualenvwrapper, this script would help you create a new
# environment, configure it and install everything needed for
# development.

# To get this file running and the environment created run:
# $ . ./env_creator.sh <env_name>

PYTHON_EXEC=`which python2.7`
OLD_DIR=`pwd`

if [[ ! -f $PYTHON_EXEC ]];
then
    echo "Missing python2.7 binary required"
    exit 1
fi

ENV_NAME=$1

if [[ -z "$ENV_NAME" ]];
then
    ENV_NAME='kyheo-mediaDownloader'
fi

cd ..
mkvirtualenv $ENV_NAME -p $PYTHON_EXEC
pip install --upgrade pip
pip install BeautifulSoup
pip install -r doc/requirements.txt
# add2virtualenv src
setvirtualenvproject $VIRTUAL_ENV $(pwd)
cd $OLD_DIR
deactivate

echo ""
echo "Virtualenvironment created, helpful commands: "
echo " - workon $ENV_NAME : will start the virtual environment and take you to the project dir."
echo " - cdproject : will take you to the main repo directory while inside the virtual environment "
echo " - cdsitepackages : will take you to the library directory "
echo " - deactivate : will get you out the virtual environment."
echo ""
