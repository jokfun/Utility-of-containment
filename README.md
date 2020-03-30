# Utility of containment

Simulation of the effectiveness of a containment on a population

![Demo](clip.gif)

## How to use it

First you have to add the package tqdm : pip install tqdm

Then, edit the bottom of the files __simulation.py__ :
```python
	"""
		CUSTOM THE HYPERPARAMETERS HERE
	"""
	size_population = 150
	borderX = 20
	borderY = 20
	episodes = 3000
	chance_to_move = 0.01
	length_move = 0.2
```
__Warning__ : The larger the population size, the longer it will take. In addition, the population size and the size of the map must be consistent.

Finally you can run the command:
```
	python simulation.py
```

## Author 

Raphael Teitgen (raphael.teitgen@gmail.com)