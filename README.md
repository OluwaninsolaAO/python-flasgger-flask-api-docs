# Python Flasgger Flask API Docs

This project is built using Python Flask, ensured to have python3 and python3-pip installed and optionally python3-venv. Depending on your OS, read how to install these packages on your Machince.

Follow these steps to get the project ready to run on your Machine.

**Install Python dependencies**: You can choose to install these dependencies globally, but it is not recommended, instead create a virtual environment using python's naitive venv following the steps below:

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate

(.venv)
$ pip install -r requirements.txt
```

**Start API Server**: Start API server in test mode to ensure all tests will run successfully without any errors and optionally set DEBUG also to True. Note that this config can also be defined in a `.env` file at the project's root directory. If successful, the API Server will be running on port `5000`

```bash
(.venv)
$ TEST=True DEBUG=True python3 -m api.v1.app
 ...
 * Running on http://127.0.0.1:5000
 Press CTRL+C to quit
```

**Run API Unittest**: While the API server is still running, ensure everything works correctly by running the Unittest using the following:

```bash
$ python3 -m unittest discover tests
....
----------------------------------------------------------------------
Ran 4 tests in 0.049s

OK
```

### Congratulations all set-up done!
