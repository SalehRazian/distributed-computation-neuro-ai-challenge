###
# Distributed Computing
###

Using the files in this prototype, you can do distributed computing using multiple
machines.
This project was made for Neuro Challenge:
https://github.com/neuro-ai-dev/distribute-challenge

###
# Server Side
###

First, run "scheduler.py" at a machine and make sure it is at the host and port
desire. If not, abort and modify the code where appropriate. This is the scheduler
and it is responsible for the management of the tasks and their execution.

Second, run "worker.py" at the machines that you desire. If the workers need to 
connect to a specific host and port, modify the code where appropriate. This is 
a worker that will do the computations as instructed by the scheduler.

Third, run "flask_client.py" at the machine that you desire. Make sure that the
client variable is connected to the scheduler and the host and port of the flask
app is as required by you. This will act as a client to the scheduler where tasks 
will be submitted and it will act as a submission point for any user to submit 
their function for computation.

Make sure that you have a directory called save in the same directory that 
contains the "flask_client.py" file ("/save").

###
# User/Client Side
###

Make sure the "dist_computation.py" and your code are in the same directory.
from dist_computation import compute_this
Decorate the function that will be send for computation by: @compute_this
Run the function as: func.compute(x)
Make sure that the dist_computation base variable connects to the flask server.

"main_demo.py" is a demo file that is used for testing purposes.
"main_easy.py" is a demo file that is used to test easy problems.
"main_hard.py" is a demo file that is used to test hard problems.

###
# Requirements
###

Use Python3

For the "scheduler.py" and the "worker.py":
asyncio
"dask[complete]"

For the "flask_client.py":
flask
flask_restful
dill
os
werkzeug
werkzeug.util
"dask[complete]"

For "dist_computation.py":
requests
random
string
dill
os

###
# Notes
###

Python and Java:
I have used Python programming language to make this setup since on the Neuro 
Challenge page, the function provided was a python function.

Dask and Jug:
The choice of using Dask for this project was mainly to provide a working project.
This is because Dask handles the scheduler, worker and client setup.
Jug would breakdown the tasks using TaskGenerator() which gives us more freedom to 
send tasks between machines for computation. 

Flask API:
I have some experience in working with Flask and for that I used it in this 
project.

Pickle and Dill:
Serializing the function using Dill is not safe according to some sources, 
however, it was used in this project for demonstration purposes.

Potential Problems:
During the testing phase of the project, it is important to note that tasks were
sometimes allocated to one worker. This could be a problem that needs to be
investigated.

Some Improvements:
Using Jug would be an improvement as it gives us more control over the tasks. Saving the tasks and their results at the user's local machine could be beneficial
in case the server goes down during a long computation. Making the flask_client 
a scheduler and a worker could be beneficial to maximize efficient usage of 
resources.
