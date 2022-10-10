# Installation

The latest stable version of _conferences_ is available through _pip_:
```
pip install conferences
```

## Development version

You can install the development version of _conferences_ with _pip_ and _git_:
```
pip install git+https://git@github.com/Avaiga/conferences
```

## Work with the _conferences_ code
```
git clone https://github.com/Avaiga/conferences.git
cd demo-production planning
pip install .
```

If you want to run tests, please install `Pipenv`:
```
pip install pipenv
git clone https://github.com/Avaiga/conferences.git
cd conferences
pipenv install --dev
pipenv run pytest
```
