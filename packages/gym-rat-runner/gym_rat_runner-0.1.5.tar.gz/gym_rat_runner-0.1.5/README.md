# Gym-Rat-Runner

## Introduction

**Gym Rat Runner** is an open-source environment implemented over [OpenAI Gym](https://gym.openai.com/).It is a 2-D discrete environment intended for Reinforcement learning applications with collision treatments. For now, the package has two distinct environments; the open and the maze environments.

### Agent <img src="/images/rat.png" alt="Rat Agent" width="40" height="40" style="display:inline;">

The agent is represented by a friendly rat with the objective of catching the cheese. Which will have eight move action options.


### Target <img src="/images/cheese.png" alt="Rat Agent" width="40" height="40" style="display:inline;">

The cheese won't move and will always be visible to the Agent.

### Hunter <img src="/images/cat.png" alt="Rat Agent" width="40" height="40" style="display:inline;">

The Hunter is represented by a cat and will move differently depending on the environment.

## Installation

### Requirements

<pre><code>
pandas >= 1.4.1
numpy >= 1.20.3
gym >= 0.23.0
pygame >= 2.1.2
opencv-python
</code></pre>

### pip
To install the package into your machine you can use the code bellow

<pre><code>  
pip install gym-rat-runner  
</code></pre>

## Environments


### Open Environment

<br/>
<br/>

<img src="/images/Open_Environment.png" alt="Open Environment" width="360" height="360" style="display:block; margin-left: auto; margin-right: auto;">
<br/>


The open environment has 10 by 10 spaces and the cat is sleeping and won't move independently what the rat does.

### Maze Environment

<br/>
<br/>
<img src="/images/Maze_Environment.png" alt="Maze Environment" width="850" height="450" style="display:block; margin-left: auto; margin-right: auto;">
<br/>

The maze environment has 16 by 32 spaces based on the [Bank Heist](http://www.virtualatari.org/soft.php?soft=Bank_Heist) from Atari. Like the police in Bank Heist, the hunter won't be able to move back but it will have two options of movement:

1. The Agent is outside the field vision of the  hunter
  * The cat will move randomly by the maze.
2. The agent is inside the field vision of the hunter.
  * The cat will start to run after the rat and will move twice the movement of the agent.
