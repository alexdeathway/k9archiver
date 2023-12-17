# step to run, generate coverage report and update badge.json

Step 1: run test
```
coverage run manage.py test
```
Step 2: generate coverage report in json format
```
coverage json --pretty-print -o coverage/coverage.json 
```
Step 3: update badge.json
```
python coverage/coverage.py
```

