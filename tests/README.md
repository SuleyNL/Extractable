#Manual testing
Unfortunately there have been unresolved issues with running tests in this repo. Most importantly with the commandline 
pytest not finding the appropriate files when performing actions such as ``pdm run pytest -v -k unittests`` or 
``pytest tests/*``. Especially between Windows and Linux-based OS systems there seems to be a stark difference. 
This created the importance of this manual testing manual. 

##Windows

If you want to run tests on Windows you can only do this in the following way. in terminal:

for the unittests:
 
```commandline 
pdm run pytest -v -k tests/Test_Extractable_Unittests/
```

and for the e2e tests:
```commandline 

pdm run pytest -v -k tests/Test_e2e_blackbox/
```

##MacOS/Ubuntu
On MacOS it is a bit different. First you must create and activate a python virtual environment, then you should install
the packages, after which you can run the tests using pytest and NOT pdm.

###Create venv:

````commandline
sudo apt install python3.10-venv        ##!ONLY in case Python3.10 is not installed!##
````

````commandline
python3.10 -m venv myenv
````

````commandline
source myenv/bin/activate
````

###Run tests:

Unittests:
````commandline
pytest tests/Test_Extractable_Unittests/*
````

and for the e2e tests:
````commandline
pytest tests/Test_e2e_blackbox/*
````