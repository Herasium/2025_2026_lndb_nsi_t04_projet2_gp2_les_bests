Project Overview
================

Overview
--------

This project provide the user with a capable logic gates simultation, turing complete.
The project can be divided into three parts:

- **The Sandbox**, where users are free to user every tool to let their creativity run free.
- **The Levels**, where users are though in a progressive and organized manner the basics of binary logic.

The architecture is designed to be extensible, allowing custom gates,
compositions, and multiple abstraction levels (1-bit, 8-bit, mixed).

Architecture
------------

The project is organized into the following main packages:

- ``modules.data``  
  Core domain model: gates, nodes, chips, and level definitions
  Shared classes and textures data for the entire project

- ``modules.engine``  
  Simulation logic and execution pipeline

- ``modules.ui``  
  All user interactions, main menu, editors and levels

- ``modules.logger``  
  Logging and debug utilities


Key Concepts
------------

Gates
~~~~~
Logical operators (AND, OR, NOT, etc.) implemented across different bit widths.

Levels
~~~~~~
Prebuilt by us, they represent a goal where the user is directed.

UI Systems
~~~~~~~~~~
Tools for editing, debugging, and interacting with the simulation.


Getting Started
---------------

Typical workflow:

1. Select a level
2. Find the right solution
3. Learn to create your own projects
4. Build your own chips, free of limitations
5. Enjoy!


API Reference
-------------

See the :doc:`api` section for full technical documentation.