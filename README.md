# Recurring donations

![image](https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png)

This script is a command-line implementation of a new recurring donation
feature. We want donors to be able to specify a monthly recurring
donation limit and make recurring donations of specified amounts to individual
campaigns. This command-line interface accepts input
from STDIN or from a file passed as an argument to the command-line tool

The 3 main entities that we are using in place here are:
- Donor
- Campaign
- Donation

The processing of the file we receive relies on trying to create commands to execute the creation of donors, campaigns or donations. Each one with the following basic rules:
- General
  - The prefix for each command will be processed case insensitive wise.
- Donor
  - This command string format is `Add Donor <name> <funds>`.
  - name has to be unique. If we receive two donors with the same name (case insensitive), only the first command is executed.
  - funds for a donor can have a `$` prefix, but as long is parseable to number and greater than 0 it can be executed.
- Campaign
  - This command string format is `Add Campaign <name>`.
  - name has to be unique. If we receive two campaigns with the same name (case insensitive), only the first command is executed
- Donation
  - This command string format is `Donate <donor_name> <campaign_name> <amount>`.
  - donor_name has to be already in the model
  - campaign_name has to be already in the model
  - amount for a donor can have a `$` prefix, but as long is parseable to number and greater than 0 and it is lesser or equal than the funds of the donor, it can be executed

Any error on the format of all these commands, like having less arguments or non parceable arguments, it will cause the system to ignore that command

Example of well formed commands:
``` text
Add Donor Greg $1000
Add Campaign SaveTheDogs
Donate Greg SaveTheDogs $100
```

After the entire input is consumed by the tool, it prints a summary and exit with a
successful exit code. The summary consists of:
- Each Donor's total donations for a month
- Each Donor's average donation size
- Each Campaign's total received donations for a month.

There are separate sections for Donors and Campaigns, and the Donors and Campaigns are printed in alphabetical order.

That way, the following input:

``` text
Add Donor Greg $1000
Add Donor Janine $100
Add Campaign SaveTheDogs
Add Campaign HelpTheKids
Donate Greg SaveTheDogs $100
Donate Greg HelpTheKids $200
Donate Janine SaveTheDogs $50
```

Results in exactly the following output:

``` text
Donors:
Greg: Total: $300 Average: $150
Janine: Total: $50 Average: $50

Campaigns:
HelpTheKids: Total: $200
SaveTheDogs: Total: $150
```

If the input does not creates data to build this report, the script does not print anything on the output.


# Solution overview

For building this solution I've created several entities that colaborate among them for the solution.
- Consolidator: 
  - The main class I've created. I'm making paces with the naming desition. The whole purpose of the class is to be the coordinator and consolidator of the model of the application, holding data properly created and being the "source of truth" for the final report. It colaborates with the EntriesReport regarding how to store each one of the command's execution results.
- EntriesReporter:
  - Stores the ReportEntry instances that indicate the status of each operation. These normally have subclasses of Commands as target, but it can also store string input errors from parsing errors from stdin.
  
  - My background as ETL software developer also led me to think on a way to log each operation (succesful or not) for future analysis, statistics reporting and troubleshooting
- Models:
  - They just represent the actual valid data in our system
- Commands:
  - They represent an executable command that can create donors, campaigns, or donations. Each one of it subclasses has to implement how to generate a new instance of itself from a string representation. I expect that they run some validation in that stage, but even if they don't run the validation method they have, on the implementation of the ingestion of that command by the Consolidator, we validate the commands.

# Takes on cons of the implementation

- we still don't have a way to link a log entry with the line being processed
- we can't define a real unique key for each donor, or project, but the name hopefully we can get that in the command and acomodate the model to this new feature

# Table of contents

- [Installation](#installation)
- [Running Python script](#running-python-script)
- [Usage](#usage)
  - [Flags](#flags)
- [Building a standalone executable](#building-a-standalone-executable)
- [Running standalone executable](#running-standalone-executable)
- [Unit testing](#unit-testing)

# Installation

[(Back to top)](#table-of-contents)

Install Python (preferably, version >= 3.11). For that purpose please check [Python Donwload page](https://www.python.org/downloads/). Bear in mind that, it is a good practice to create and activate virtual environment for working on different python projects, [check the documentation](https://docs.python.org/3/library/venv.html).

Once you have an interpreter and having deciding if you will use or not an env, you can run the app

## Running Python script

[(Back to top)](#table-of-contents)

You can run the python scripts using the following syntax in bash just by setting the right filepath you want to run:
  ```bash
  cat <filepath> | python recurring.py
  ```
  or
  ```bash
  python recurring.py <filepath>
  ```
  *Note: In the root folder of the project we have a file named `input.txt` that has examples of commands we used for testing, you can run the app with them executing the following bash script:*

   ```bash
  python recurring.py input.txt
   ```

# Usage

[(Back to top)](#table-of-contents)

Usage explanation pages have been set in place. Checkout:
 ```bash
  python recurring.py
```

### Flags

- With `-v` (or) `--verbose` : Log to stdout processing logs for each command line

## Building a standalone executable

1. For building a standalone executable, you have to [install PyInstaller](https://pyinstaller.org/en/stable/installation.html). 

   *Note: The easiest way to install it is just to run:*
   ```bash
   pip install pyinstaller
   ```

2. Once this package is installed, run:
    ```bash
    pyinstaller --onefile recurring.py
    ```
    The execution of this command will create a new folder called `dist` in which  you will find an executable file generated for your actual environment

## Running standalone executable

[(Back to top)](#table-of-contents)

From the previous step you will get a file that has a name, or maybe a given extension that's specific to your filesystem (in this specific example, I've ran the script in Windows, so I got `recurring.exe`)
You can run the executable built in `dist` folder you can run:
  ```bash
  cat <filepath> | ./dist/<executable>
  ```
  or
  ```bash
  ./dist/<executable> <filepath>
  ```
  *Note: In the root folder of the project we have a file named `input.txt` that has examples of commands we used for testing, you can run the app with them executing the following bash script:*
  
  ```bash
  ./dist/<executable> input.txt
  ```

  Windows example:
  ```bash
  ./dist/recurring.exe input.txt
  ```

## Unit testing

[(Back to top)](#table-of-contents)

### Unit testing libraries installation

1. After the general setup you have to run the following script for adding test coverage support:

   ```bash
   pip install pytest
   pip install pytest-cov
   ```

2. Once those packages are installed, run:
  - For only running tests:
    ```bash
      pytest tests
    ```
  - For running coverage report in stdout:
    ```bash
    pytest tests --cov=internal
    ```
  - For running coverage report and store it as html:
    ```bash
    pytest tests --cov=internal --cov-report=html
    ```
    The execution of this command will create a new folder called `htmlcov` in which  you will find a static page structured with and `index.html` file that you can open to traverse the report


You can run the executable built in `dist` folder you can run:
  ```bash
  cat <filepath> | ./dist/recurring.exe
  ```
  or
  ```bash
  ./dist/recurring.exe <filepath>
  ```
  *Note: In the root folder of the project we have a file named `input.txt` that has examples of commands we used for testing, you can run the app with them executing the following bash script:*
  
  ```bash
  ./dist/recurring.exe input.txt
  ```