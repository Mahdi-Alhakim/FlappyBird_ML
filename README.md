# Flappy Bird Copy with ML - Reinforced Learning

This is a flappy bird game copy created with python and tkinter. Additionally, a self-learning bot is implemented that learns to play the game across generations of multiple bird bots following a genetic algorithm and reinforced learning.

**_Note:\
It may take a few rounds until birds begin to pass the pipes._**

## Requirements:
- #### python 3.x
- #### Tkinter 8.6
- #### Pillow 10.10.0
- #### Thread6 0.2.0
- #### Personal Neural Network Library:
    _`git+https://github.com/Mahdi-Alhakim/NeuralNetworkLibrary.git`_


## Setup:

1. Create a virtual environment using the latest release of virtualenv:

``` bash
> pip install virtualenv --upgrade
> virtualenv venv
```

_If there are problems with installing tkinter:_
- Install tkinter package. Ex: Homebrew:
``` bash
> brew install python-tk
```
- Then create the virtual environment as follows:
```
> virtualenv venv --system-site-packages
```

2. Access the virtual environment `./venv`
``` bash
> source ./venv/bin/activate
```

3. Install the requirements:
```bash
> pip install -r requirements.txt
```

## Execution:

#### To run the self-playing version of the game, execute the following command:

``` bash
> python3 Flappy_Bird_AI.py
```

#### To play the game yourself, execute the following command:

``` bash
> python3 Flappy_Bird.py
```

## How to Play:

* Click / Space / Up-Arrow to jump
* Don't Hit the pipes!
