#!/usr/bin/env bash

DIST="dist"
ARTIFACT="bundle.zip"

# ----------------------------------------------------------------------------
printf "\n----- CREATING VIRTUALENV...\n"
virtualenv env
. ./env/bin/activate

# ----------------------------------------------------------------------------
printf "\n----- INSTALLING DEPENDENCIES...\n"
pip install -r requirements.txt

# ----------------------------------------------------------------------------
printf "\n----- BUNDLING...\n"
mkdir $DIST
cp -rf env/lib/python3.*/site-packages/* $DIST
cp -r stalker $DIST

cd $DIST
rm -rf pandas numpy pip setuptools wheel
curl \
    "https://files.pythonhosted.org/packages/c2/76/73df80caf7affbe4b4f4a3b69a9a8f10b3b2acbb8179ad5bb578daaee56c/numpy-1.19.1-cp38-cp38-manylinux1_x86_64.whl" \
    --output numpy.whl

curl \
    "https://files.pythonhosted.org/packages/5d/9f/f4c2a0f6f03d3ba95043c616e477926776ed3de7963a80edede7599630de/pandas-1.1.0-cp38-cp38-manylinux1_x86_64.whl" \
    --output pandas.whl

unzip -o numpy.whl
unzip -o pandas.whl

rm -r *.dist-info __pycache__ *.whl *.virtualenv
zip -q -r $ARTIFACT .

cd ..
mv $DIST/$ARTIFACT .
rm -rf $DIST
