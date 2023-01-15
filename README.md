# pandpk Notes Organizer Tool

## Setup
1.  To setup the environment, first create a virtual environment.

    ```sh
    python -m venv .rename-env
    ```

2.  Next, install Python dependencies.

    ```sh
    ./rename-venv/Scripts/python -m pip install -r requirements.txt
    ```

3. Create a bin folder with a batch file to run the script.

    ```sh
    mkdir bin
    code bin/pandpk.bat
    ```

4.  Replace the contents of the batch file with the following.

    ```bat
    @echo off
    path-to-python path-to-rename-script %*
    ```

5.  Add the location of the batch file to environment variables.
6.  Restart your terminal.

## Run
Just open a terminal in the correct folder and run the command.
```pwsh
PS> pandpk
```