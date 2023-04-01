# FastAPI User Service

## Setup Environment
~~~
python3.9 -m venv venv
~~~
~~~
source venv/bin/activate
~~~
~~~
sh scripts/install_requirements.sh
~~~

## Install new requirement
~~~
pipenv install package_name
~~~

## Important Points
- Do not push .env file
- It should be present at server level
- BaseModel validation does not support variables starting with underscore

## Get 32 characters long secret Key
~~~
openssl rand -hex 32
~~~