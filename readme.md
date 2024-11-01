# Installation and Setup
## Getting Started

To get started, follow these steps:

## Clon the repository
* You can clone the repo from GitHub using the following command:
  
    ```bash
     git clone https://github.com/Slawoodman/Vimmi.git
    ```
## Create a Virtual Environment
* It's recommended to create a virtual environment to manage  project dependencies. If you don't have virtualenv installed, you can install it using pip:
    ```bash
    pip install virtualenv
    ```
* Then, create a new virtual environment and activate it:

    ```bash
    virtualenv envname
    ```

    ```bash
    envname\scripts\activate
    ```

## Install Required Dependencies

* Navigate to the project directory:

    ```bash
    cd Vimmi
    ```
* Install the required dependencies listed in the requirements.txt file:
    ```
    pip install -r requirements.txt
    ```
   
## Run the test

Now let's run the tests:
  ```
  pytest
  ```