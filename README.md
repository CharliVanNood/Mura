# Game Development Project HU AI S2


Şeyma Ceren Yildirim 
1878084 \
Author of level 2

Jens Kortink 
1811273 \
Author of level 6

Mathijs de Jong 
1833628 \
Author of level 7

Charli van Nood 
1888360 \
Author of levels 3 & smiley

Myla Berger 
1882404 \
Author of levels 1, 4 & 5

<br/><br/>

dependencies:

pygame==2.6.1
pillow==11.2.1

<br/><br/>
How to install game:

Clone the repository to an IDE running python 3.12 and install the dependencies
<br/><br/>
How to install dependencies:

pip install -r reqirements.txt
<br/><br/>

How to run the game:
run main.py and the game window will open

# controls:


A: move left

D: move right


Space: jump

**X**: respawn / quit

&uarr; : change gravity up

&darr; : change gravity down


# Formatting world files:
## Default
All objects should start with the object id,  
The arguments are split by : and ended with @
## Player
For the player object you have to give up the P at the start to notify the engine it's dealing with a player  
And after that the x and y coordinates which will result in an object like this:  
`P:1:2@`
This will set the player to x=1 and y=2  
## Portal
For the portal object you have to give up the T at the start to notify the engine it's dealing with a player  
And after that the x and y coordinates which will result in an object like this:  
`T:1:2`
This will set the portal to x=1 and y=2, T stands for teleport as P was already used in player  
`T:1:2:10:10@`
This second set of x and y arguments sets the destination
## Ground
For the ground object you have to give up the GroundId at the start to notify the engine it's dealing with a ground object  
We have a few different ground objects, the main ones right now are:  
- G1: ground_1
- GW1: ground_wide_1
And after that the x and y coordinates which will result give an unfinished object like this:
`G1:1:2`
This will set the ground to x=1 and y=2, now we have to set the size modifier like this:
`G1:1:2:1:1`
1 by 1 is the normal size for a ground object, making this 2 will double it's size, and at last we have to set the extenders like this:
`G1:1:2:1:1:ED@`
This will extend the tile down, the tags for this are:  
- ED: Extends Down
- EU: Extends Up
- N: No extenders

# Running the project  
- How do I run the project?  
First cd into the source folder with `cd src`  
use python3 with `python3 main.py`  

# Installation Python
- How do I install python? **(Arch)**  
Install with pacman `sudo pacman -S python`  

- How do I install python? **(Ubuntu)**  
Install with apt `sudo apt install python`  

- How do I install python? **(Windows)**  
Download the installer from `https://www.python.org/downloads/windows/`  
Run the installer.  

# Installation Pygame  
- How do I install pygame?  
use pip with `pip install pygame`  

- How do I install pip? **(Arch)**  
use pacman with `sudo pacman -S python-pip`  

# Required dependencies
- Pillow `pip install pillow`