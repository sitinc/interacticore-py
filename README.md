# interacticore-py
Python module for common patterns and classes for interactgen-py, interactovery-py, and interactilogue-py modules.  The 
module abstracts invocations against large language models (LLMs), and aims to remove as much boiler plate as possible, 
and inter-working differences between model behaviours for module-user-consistency.

## Installation

This project requires Python >=3.11 to <3.13. Below are the instructions to set up the environment for this project.

### Installing interacticore module

You can install the interactigen module from PyPI with **pip** or **poetry**:

**pip**:
```bash
pip install interacticore
```

**poetry**:
```bash
poetry add interacticore
```

## Usage

The best place to explore usage is [the interactigen-py GitHub project](https://github.com/sitinc/interactigen-py/).  
The [Jupyter notebook](https://github.com/sitinc/interactigen-py/blob/main/notes/interactigen-getting-started.ipynb) 
contains examples of using the Interactigen client, which wraps around the interacticore module.


## Updates and Breaking Changes

This module is something I am putting together to allow everyone to have easy-to-use tools to generate interactional 
data.  This project is not polished production code, but something I am building publicly as part of a blog series that 
will improve slowly over time.  Sometimes, those changes are going to be breaking.  I'll start considering commitments 
to backwards compatibility once the project reaches v1.0.0.  ;)
