# Pool Game Simulator

## Description
This program written in C, simulates a game of pool where balls can either roll or remain still on the table. 
It outputs results whenever a collision occurs, a rolling ball has stopped moving, or all rolling balls have rolled to a stop.
This program will continuosly check for collisions/bounce between rolling balls and objects. Also includes python code to display updated table onto webserver with svg files created by python code.

## Features
- Simulates pool game with rolling or stationary balls.
- Outputs results for collisions and ball movements.
- Supports multiple balls on the table.
- Provides customizable parameters for simulation.

## Running the C Code
1. cd pool_game
2. make
3. export LD_LIBRARY_PATH=`pwd`
4. ./a1

## Running the WebServer
1. make
2. export LD_LIBRARY_PATH=`pwd`
3. python3 server.py (local host port number)
4. open "http://localhost:(local host port number)/shoot.html"
