#!/usr/bin/env bash

set -ex

mkdir "$DIST"
cp -rf .venv/lib/python3.*/site-packages/* "$DIST"
cp -r stalker "$DIST"

cd "$DIST"
rm -rf pandas numpy pip setuptools wheel
curl \
    "https://files.pythonhosted.org/packages/41/6e/919522a6e1d067ddb5959c5716a659a05719e2f27487695d2a539b51d66e/numpy-1.19.2-cp38-cp38-manylinux1_x86_64.whl" \
    --output numpy.whl

curl \
    "https://files.pythonhosted.org/packages/64/0e/97fa348981b2ccebd39569200c91d587703329ea21508c30bb35110e404c/pandas-1.1.3-cp38-cp38-manylinux1_x86_64.whl" \
    --output pandas.whl

unzip -o numpy.whl
unzip -o pandas.whl

rm -r ./*.dist-info ./*.whl ./*.virtualenv __pycache__
zip -q -r "$ARTIFACT" .

cd ..
mv "${DIST}/${ARTIFACT}" .
rm -rf "$DIST"