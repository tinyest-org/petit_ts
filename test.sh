flake8 . --count --select=E9,F63,F7,F82 --show-source --statistic
 
output=$(coverage run test.py)    
coverage html
echo "Building HTML results"

exit $?