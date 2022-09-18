# River Health Assessor

## Description

This is a web based application that is built on the Flask framework. Data processing/manipulation is handled using pandas and front end styling achieved with the aid of bootstrap. The purpose of the application is to assess the impact of sewer overflow events from combined sewer overflows (CSO's). Input data is produced from modelling of urban and river catchments integrated with, storm/sewer networks. The application analyses pollutant levels in the river 'spill' events and produces both a SOAF impact score and the WFD class of river, as well as corresponding graphs/data.

## Getting Started

### Initial Setup
1. First clone the application to a local repository

2. Once you have the project download locally navigate to `river-health` and set up a virtual environment. This can be done by running `python -m venv env`. You will now have a local virtual environment called `env` that will appear as a folder (please stick to this naming convention as it has been added to the `.gitignore` file).

3. Now that you have a virtual envrionment run `source env/Scripts/activate` on Windows (or `source env/bin/activate` if on Mac/Linux) in order to avctivate the virtual environment.

4. Finally run `pip install -r requirements.txt` to install all of the dependencies for the project.

5. Run the command `deactivate` to deactivate the virtual enviornment when you are no longer working on the project.

NOTE: ~~If you install any packages please run `pip freeze > requirements.txt` when in the root directory in order to update the requirements with the new packages. Be aware that this will overwrite the `requirements.txt` file so ensure that you have run `pip install -r requirements.txt` (you can run this as many times as you like as it will just skip over any packages already installed)~~
pipreqs has now been implemented in the pipeline to automatically update the requirements.txt file. So there is no longer any need to use `pip freeze > requirements.txt`. To get the dependencies locally:

1. Install pipreqs using `pip install pipreqs`
2. Run `pipreqs --force` to replace the requirements.txt file when in the root of the project
3. Run `pip install -r requirements.txt`

Please see the pipreqs [documentation](https://github.com/bndr/pipreqs) for more information on how to use pipreqs.

### Running the server

The application is run by a Flask server in order to run the application locally ensure you have followed the steps above and you have your virtual environment activated. 

The app should be run using the command `python main.py` as the flask application is now instantiated in `main.py`.

The server should then be available at http://localhost:5000/

Please see the [Flask docs](https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/) if there is any confusion

### Docker

The application can be run using docker - please ensure that you have docker installed (use the command `which docker` to check if docker is installed).

To build the Docker image using the Dockerfile run the following command whilst in the root directory of the project (repalce <image name> with the name you want for the image e.g. river-health. Also don't miss the full stop at the end of the command):

`docker build --tag <image name> .`

Once the image has been built you can run the image using the following command:

`docker run -d -p 5000:5000 <image name>`

This will run the container in detached mode so that you can still use your terminal. If you want to run the container and see the outputs in your terminal remove the `-d` flag. 

On starting the container will automatically run the flask application and it will be available at http://localhost:5000/.

If you want to ssh into the container whilst it is running you can use the following command whilst in detached mode:

`docker exec -it <image name> /bin/bash`

## Testing

Testing is done using the pytest framework. Testing is simple and can be done by simply running the command `pytest` whilst in the projects root directory.

Tests must follow the naming convention of `test_*.py` for the filename and `test_*` for the function name. This is because pytest searches through all directories for files and functions following this convention and executes them.

All tests can be found in the `/tests` directory.

Note: any file paths that are implemented in the tests assume that the context is the root directory, therefore some tests may fail if `pytest` is run from any other location.

Please see the [documentation](https://docs.pytest.org/en/7.1.x/how-to/assert.html#assert) for details on how to write tests

## Deployment

The application is deployed through a docker container run on an OpenStack server, the ip address of the server is `http://10.72.100.224:5000/` 


As the application is deployed through a docker container the server does not need to be torn down and rebuilt each time the applicaiton is deployed, but rather the container image is destroyed and rebuilt - ensuring a fixed ip address for teh server.
