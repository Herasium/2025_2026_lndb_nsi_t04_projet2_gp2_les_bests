Project Usage
=============

Editor
------

Gates
~~~~~

You can add gates to your chip by dragging them from the bottom bar.  
Gates are split into 3 categories:

- 1 Bit (Binary Logic)
- Custom Gates (Based on other chips made by the user)
- 8 Bit  

You can scroll in the bottom bar to display all gates.

Paths
~~~~~

You can join multiple gates by creating a path.  
A path is created when clicking on the inputs/outputs of a gate (keyhole-like holes on the bottom of a gate).  
A path can only be connected to other inputs/outputs of the same bit size (1 bit with 1 bit, 8 bit with 8 bit).  
A path only transmits from Outputs -> Inputs.  
In case of conflicts, the outputs that were wired first are chosen as the final solution.

Deletion
~~~~~~~~

You can use Backspace (Delete key) on any gates or paths in the editor to remove them.  
Deleting a gate will also delete all paths wired to said gate.  
A deletion cannot be undone, please delete with caution.

Save
~~~~

You can save your current chip using the **"S"** key.  
Pressing it will lead you to the save menu, where you can enter a name for your chip (max 17 chars.).  
When saved, the menu will bring you back to the editor.  
All chips are auto-saved every minute to prevent any loss in case of a game crash.

Input Toggle
~~~~~~~~~~~~

You can toggle an input by hovering over the gate and pressing the **"E"** key.  
If the input is 1 bit, it will just switch its value: On -> Off, Off -> On.  
If the input is more than 1 bit, a new screen will appear, similar to the save screen, where you'll be prompted to enter a new value.  
For 8 bit, the value is between 0 and 255.  
Pressing **"OK"** will send you back to the editor.  
Pressing **"Shift"** while pressing **"OK"** will assign a random value, in the authorized range, to the input.

Level
-----

Level List
~~~~~~~~~~

A list of all levels included in the game. They are all numbered from 0 to 35, but the order is just advice; you are free to try any level, even if you didn't finish the previous one.  
Levels are also colored according to their difficulty: Green -> Yellow -> Orange -> Red -> Purple -> Black.

Level Player
~~~~~~~~~~~~

When playing a level, you are provided with 3 things:

- A time limit, set by the level's author. It won't make you fail the level, it just won't let you get 3 stars.
- Gates to use, in the bottom bar. You are limited to those gates only.
- A truth table, showing you the intended solution depending on the inputs, and what your chip will output.

To update the truth table, you can click on **"CHECK"**; it will also trigger the victory animation if necessary.  
Every level has a solution, and the answer can be seen by pressing **"ANSWER"**, which will also validate the level with only 1 star.  
In a level, you cannot delete any inputs/outputs, only move them.

Tutorial
--------

The tutorial provides you with basic insights into the workings of the game, just as the document does, with a reminder of the workings of each basic logic gate and their truth table.

Options
-------

The options let you adjust some settings of the game.  
Video-related settings such as FPS and fullscreen will require a full game relaunch to take effect.  
Settings are saved in the **preferences.json** file, in the root of the project.
