# Manavi: Automatic Poem Generation
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/pasmod/masnavi/blob/master/License.md)

Masnavi is a tool to automatically generate poems in Farsi. It uses a character based language model trained using a recurrent neural network on lots of Farsi poems. The tool produces poems in the Manavi style. For more information on Masnavi click [here](https://en.wikipedia.org/wiki/Masnavi).

## How to Train
For training you need probably a GPU. To train the network use the following command:
``` bash
THEANO_FLAGS=device=gpu,floatX=float32 python masnavi/train.py
```
You might need to use ``` gpu0```  or ``` gpu1``` instead of ``` gpu```.

##### Why is the training processs not dockerized?
For training the network I used the HPC system of the university of Düseldorf ([HILBERT](https://www.zim.hhu.de/high-performance-computing.html)). Unfortunately, docker could not be installed on the cluster (due to some crezy technical reasons!). Keep in mind that for training you need to install the dependencies listed in  ``` requirements.txt ```.

## How to Start the App
The project has also a very simplistic web application to ease the use. Use the following commands to start the application locally:
``` bash
make build
make start
```
Now the web application runs as daemon in background. Simply point your browser to ``` http://localhost:5000/ ``` to use the app. Notice that processing a poem generation request may take up to 30 seconds. Be patient!


# ToDos
- Processing poem generation requests takes up to 30 seconds. Show the user a message that we are processing the request and the app is not crashed!
        
