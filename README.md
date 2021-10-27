

# URL-SAFE

A simple service that can be queried to determine if a given URL is safe to allow access to.

The query can be made using REST calls with the following format:

/urlinfo/1/{hostname_and_port}/{original_path_and_query_string}

It will return "True" if the given input results in a safe URL or false otherwise. The return structure is a JSON dictionary with the following format: <br>

{ "Blocked": <true/false> }

## Deveoper setup

Install Python 3.8.12 environment <br><br>
Note: these are instructions to create a python 3.8+ virtual environment. If you have another preferred method of installing python and python-packages please feel free to use that one.<br>

1. Follow instrunctions here to install pyenv <br>
https://www.liquidweb.com/kb/how-to-install-pyenv-on-ubuntu-18-04/
1. Followin instrunctions here instal install pyenv-virtualenv <br>
https://github.com/pyenv/pyenv-virtualenv
1. Install python 3.8.12
    > pyenv install 3.8.3
1. Install virtual-env for developer work
    > pyenv virtualenv 3.8.3 url_safe
1. Install git.
    > sudo apt-get install git

## Install code
1. Clone the repo
    > git clone https://github.com/briandsouza2/urlsafe.git
2. Activate the url_safe virtual-enviroment
    > source ~/.pyenv/versions/url_safe_new/bin/activate
2. Install python packages
    > pip install -r requirements.txt <br>
    > pip install -r requirements-dev.txt
2. Install urlsafe
    > pip install -e .
2. Set developer mode
    > export FLASK_ENV=development
2. Start up the server
    > urlsafe

## Make sample requests
Note: The "original_path_and_query_string" must be URL encoded. A helper script has been provided to help do this.

1. Test a blocked URL <br>
    > ./helpers/checkurl.sh "testhost_80" "somepath?param1=1&param2=2" <br>
        [output]<br>
        curl http://localhost:5000/urlinfo/1/testhost_80/somepath%3Fparam1%3D1%26param2%3D2<br>
        {
        "Blocked": true
        }
1. Test a 'safe' URL:
    > ./helpers/checkurl.sh "testhost_80" "goodpath?param1=1&param2=2" <br>
        [output]<br>
        curl http://localhost:5000/urlinfo/1/testhost_80/goodpath%3Fparam1%3D1%26param2%3D2<br>
        {
        "Blocked": false
        }


## Docker container
1. Create test data for the container. This will create 4 random hosts with 10000 blocked URIs each. <br>
    > python ./helpers/generate_url.py
1. Build the docker image
    > docker build -t flask/urlsafe .
2. Start the container
    > docker run -d -p 5000:5000 flask/urlsafe

## Testing
1. To run the unittests <br>
    > make test
1. To run performace tests <br>
    > python helpers/perf_test.py

## Cleanup
1. To clean up after docker
    > docker rm -f $(docker ps -a -q)
    > docker image prune