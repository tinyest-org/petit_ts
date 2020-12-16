./test.sh
if [ $? -eq 0 ]; then
    echo "Test passed, proceeding, with build and upload"
    echo "Uploading code coverage results"
    bash <(curl -s https://codecov.io/bash)
    python3 setup.py sdist bdist_wheel
    python3 -m twine upload dist/*
    rm -rf build dist petit_ts.egg-info
else
    echo "Test failed, upgrade canceled"
fi
