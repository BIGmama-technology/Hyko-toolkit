set -x 
set -e

rm -rf dist

python -m build
python -m twine upload ./dist/*