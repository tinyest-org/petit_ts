python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
rm -rf build dist petit_ts.egg-info