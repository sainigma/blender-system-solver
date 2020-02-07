
## Description

This addon is an animation tool that uses a system equations solver along side simulation cases to move objects in realistic fashion. The addon also provides an UI to Blender's toolshelf to control the simulation.

Currently I've written a simulation for sinking objects, it takes gravity and hydrodynamic drag into account. I'll be adding more once I get to it.

TLDR; The addon is in functional state, but needs documentation and more simulation cases.


## Installation 

Download the repository or clone it with

    git clone https://github.com/sainigma/blender-system-solver.git

Then either copy the addon folder **blender-system-solver** from the root of the repo to your Blender addon folder and enable the addon from Blender's addon preferences, or feed the repository as a zip to Blender's internal addon installer.

## Usage

Simulation controls are visible in object mode, and can be found from the right toolbar when a target object is selected. Select simulation case, set initial parameters and run the script, results are saved as keyframes.

![alt text](./docs/buoyantSystemUI.png "UI for sinking objects")