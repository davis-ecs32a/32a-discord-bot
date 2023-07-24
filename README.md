# 32a-utils
A collection of useful scripts for managing the UC Davis ECS32A class.

# Discord Bot (bot.py) Documentation
## Overview
The bot is designed to facilitate interaction between students and tutors in a learning community hosted on a Discord server. The bot manages channels for asking questions, answering them, and registering for tutoring sessions. It ensures the proper flow of interaction, keeping the server organized and efficient.

## Initialization
The bot is initialized with a token, which is not provided in the code for security reasons.

```python
bot = interactions.Client(token='<token>')
```

The waiting_list is a global list that will hold the queue of students waiting for a tutor.

```python
global waiting_list
waiting_list = []
```
Two button objects are defined for user interaction: `public_button` and `private_button`.

## Utility Functions
There are several utility functions that help in retrieving information about categories and roles in the Discord server:

1. `get_categories(ctx)`: This function returns the IDs of the channels "ASK HERE", "ACTIVE QUESTIONS", "TUTORING", and "ANSWERED QUESTIONS".

2. `tutor_check(ctx)`: This function checks if a user has the role of "Tutor" and returns a boolean value.

3. `get_relevant_roles(ctx)`: This function returns the IDs of the roles "Tutor", "@everyone", "Student", and "Active Tutor".

## Commands
Commands in the bot are defined using the `@bot.command` decorator. Here are the commands defined in the bot:

1. `resolve`: This command is used to close a channel. It checks if the channel is open and if the user executing the command has the necessary permissions. If the channel is private, it deletes the message history.

2. `register`: This command allows a user to get in line for a tutor. It adds the user to the waiting_list and notifies them of their position.

3. `next`: This command allows a tutor to notify the next student in line that they are ready. It checks if the user executing the command is a tutor and if there is a student in line.

4. `signin`: This command allows a tutor to sign into their tutoring shift. It checks if the user executing the command is a tutor and if they are not already signed in.

5. `signout`: This command allows a tutor to sign out of their tutoring shift. It checks if the user executing the command is a tutor and if they are not already signed out.

6. `forceresolve`: This is a debug command reserved for use by admins to force any channel to become a new Ask Here channel. If a channel ever fails to resolve into a proper state, an admin can use this command to fix it.

## Button Responses
There are two button responses defined in the bot, `public_button_response` and `private_button_response`. These responses are triggered when a user clicks on the respective button. They handle the process of opening a question in a public or private channel.

## Running the Bot
The bot is started with the `bot.start()` command at the end of the script.

## Note
Please remember to replace `<token>` with the actual bot token in the `interactions.Client(token='<token>')` line before running the bot.


# Homework Submission Consolidation Script (hwStyle.py) Documentation

## Overview
This script consolidates student homework submissions that are exported from Gradescope. The script reads student data from a CSV file, consolidates their submissions which are in separate files, and outputs a single file for each student in the `result` directory. Each output file is named after the student.

## Import Dependencies
The script uses the following libraries:

- `os`: For interacting with the OS, especially for file and directory operations.
- `shutil`: For file operations such as copying.
```python
import os 
from shutil import copyfile
```

## Main Functionality
The main functionality of the script is to read student data from a CSV file, consolidate their submissions, and output the consolidated submission. This is done in the `main` function of the script.

The script reads student data from a CSV file. For each student, if their assignment status is not "missing", the script reads their submission files from the `submissions` directory, concatenates the contents, and writes the `result` into a new file in the result directory. The new file is named after the student.

## Functions
1. **Initialization**: The script starts by initializing an empty dictionary, `cluster_dict`, which will hold unique code submissions as keys and their corresponding `SameCode` objects as values. The `SameCode` class is a Python dataclass that represents a group of students who have submitted the same code. It contains the shared code, the filename of the submission, a list of students who have submitted the same code, and the number of such submissions.

2. **Reading Metadata**: The script reads a CSV file of student data, which includes student names and their submission status. It creates a dictionary mapping the submission ID to the student's name.

3. **Processing Submissions**: The script iterates over all student submissions in the `submissions` directory. For each student, the script reads their Python (.py) files. It strips comments and whitespace from the top of each file and uses this stripped code as a key in the `cluster_dict` dictionary.

4. **Cluster Creation**: If the stripped code is not already in the `cluster_dict`, a new `SameCode` object is created with the stripped code, the filename, and the student's name. If the stripped code is already in the `cluster_dict`, the script retrieves the corresponding `SameCode` object and updates it with the new student's name and increments the copies attribute. This process effectively clusters together all submissions that have the same stripped code.

5. **Filtering and Formatting**: After all submissions have been processed, the script filters out `SameCode` objects that have fewer than `CLUSTER_THRESH` copies. This threshold determines the minimum number of similar submissions needed to be considered potential plagiarism. The remaining `SameCode` objects are formatted into strings and written to a CSV file. Each line of the CSV file includes the problem name (filename), and the names of the students who have submitted similar code.

## Usage
Before running the script, you need to do the following:

1. Export the submissions from Gradescope.
2. Unzip the exported directory and rename it to submissions.
3. Export the grades from Gradescope.
4. Save the grades file as 'HW4.csv' or equivalent.
5. Update the variables in the script (CSV file name, homework Python files).
6. Run the script.
The script creates a `result` directory if it doesn't exist and writes the consolidated submission files into this directory.





# Homework Submission Illegal Imports Checker (illegal_code.py) Documentation

## Overview
This script checks student homework submissions that are exported from Gradescope for illegal imports and functions. The script reads student data from a CSV file, parses their submissions, and creates a CSV file listing any illegal imports or functions used.

## Import Dependencies
The script uses the following libraries:

- `os`: For interacting with the OS, especially for file and directory operations.
- `re`: For using regular expressions to find imports in the code.
- `collections`: For using the `defaultdict` data structure.
- `dataclasses`: For using Python dataclasses.

```python
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
```

## Data Structures
The script uses the CodeSubmission dataclass to represent a student's submission. It includes the student's name, the file name, a list of imports found in the file, and a boolean indicating whether the file contains a `__name__ == "__main__"` check.

## Main Functionality
The main functionality of the script is to read student data from a CSV file, parse their submissions, check for illegal imports or functions, and output the results into a CSV file. This is done in the `main` function of the script.

The script reads student data from a CSV file. For each student, if their assignment status is not "missing", the script reads their submission files from the `submissions` directory, checks for illegal imports and functions, and writes the results into a new file. The new file lists all students who have used illegal imports or functions.

## Usage
Before running the script, you need to do the following:

1. Export the submissions from Gradescope.
2. Unzip the exported directory and rename it to submissions.
3. Export the grades from Gradescope.
4. Delete all the columns in the grades CSV except for first name, last name, and submission_id.
5. Save the file as 'HW3_ID.csv', eg.
6. Run the script.
The script creates a CSV file listing all students who have used illegal imports or functions.


# Homework Submission Plagiarism Checker (plag.py) Documentation

## Overview
This script checks student homework submissions that are exported from Gradescope for similarities. The script reads student data from a CSV file, parses their submissions, and creates a CSV file listing submissions that are too similar.

## Import Dependencies
The script uses the following libraries:

- `os`: For interacting with the OS, especially for file and directory operations.
- `collections`: For using the `defaultdict` data structure.
- `dataclasses`: For using Python dataclasses.
```python
import os
from collections import defaultdict
from dataclasses import dataclass, field
```

## Data Structures
The script uses the `SameCode` dataclass to represent a cluster of similar submissions. It includes the common code, the file name, a list of students who submitted the same code, and the number of students who submitted the same code.

## Main Functionality
The main functionality of the script is to read student data from a CSV file, parse their submissions, check for similarities, and output the results into a CSV file. This is done in the `main` function of the script.

The script reads student data from a CSV file. For each student, the script reads their submission files from the `submissions` directory, checks for similarities with other submissions, and if a submission is too similar to others (based on the `CLUSTER_THRESH` variable), it is written into a new file. The new file lists all students who have submitted similar code.

## Usage
Before running the script, you need to do the following:

1. Export the submissions from Gradescope.
2. Unzip the exported directory and rename it to submissions.
3. Export the grades from Gradescope.
4. Save the file as 'HW3.csv', eg.
5. Run the script.

The script creates a CSV file listing all students who have submitted similar code.




# Gradescope API Client (api_client.py) Documentation
## Overview
This script is designed to interact with the Gradescope API for the purpose of uploading student assignments. The script logs into Gradescope using provided credentials, reads student data from a CSV file, and uploads assignments from a specified directory.

## Import Dependencies
The script uses the following libraries:

- `requests`: For making HTTP requests to the Gradescope API.
- `getpass`: For securely handling password input.
- `os`: For interacting with the OS, especially for file and directory operations.
- `shutil`: For file operations such as copying.
```python
import requests
import getpass
import os 
from shutil import copyfile
```

## APIClient Class
The main functionality of the script is encapsulated within the APIClient class. This class has methods for logging into Gradescope and uploading assignments.

### `__init__` Method
The constructor initializes a requests.Session object which is used for making the HTTP requests.

### `post` Method
A simple wrapper around requests.Session.post for making POST requests.

### `log_in` Method
This method logs into Gradescope using the provided email and password. It saves the access token for future API calls.

### `upload_pdf_submission` Method
This method uploads a PDF submission for a student. It requires the course ID, assignment ID, student's email, and the filename of the PDF.

### `replace_pdf_submission` Method
This method replaces a student's PDF submission. It requires the course ID, assignment ID, student's email, and the filename of the PDF.

### `upload_programming_submission` Method
This method uploads a programming submission for a student. It requires the course ID, assignment ID, student's email, and the filenames of the submission files.

## Main Functionality
The main functionality of the script is to read student data from a CSV file and upload their assignments. This is done in the `if __name__ == '__main__'`: section of the script.

The script logs into Gradescope using hardcoded credentials, then reads student data from a CSV file. For each student, if their assignment status is not "missing", the script uploads their assignment from the ./result directory.

## Usage
Before running the script, you need to update the CSV file name and the course ID and assignment ID variables. Then, run the script in the directory where the CSV file and ./result directory are located.

Please note that the APIClient class can be imported into other Python scripts for interacting with the Gradescope API. The methods provided in the class can be used to log into Gradescope, upload assignments, and replace assignments.
