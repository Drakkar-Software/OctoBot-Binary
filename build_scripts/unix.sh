#!/bin/bash
pip install -U pip setuptools wheel
pip install -r requirements.txt
git clone -q $OCTOBOT_GH_REPO -b $OCTOBOT_DEFAULT_BRANCH
pip install --prefer-binary -r $OCTOBOT_REPOSITORY_DIR/dev_requirements.txt -r $OCTOBOT_REPOSITORY_DIR/requirements.txt
python scripts/python_file_lister.py bin/octobot_packages_files.txt $OCTOBOT_REPOSITORY_DIR
python scripts/insert_imports.py $OCTOBOT_REPOSITORY_DIR/octobot/cli.py
cp -R bin $OCTOBOT_REPOSITORY_DIR
cd $OCTOBOT_REPOSITORY_DIR
python ../scripts/fetch_nltk_data.py words $NLTK_DATA
python setup.py build_ext --inplace
python -m PyInstaller bin/start.spec
mv dist/OctoBot ./OctoBot_$BUILD_ARCH && rm -rf dist/
ls -al
