# GFM Code Submission

You are designing a command-line implementation of a new recurring donation
feature for GoFundMe. We want donors to be able to specify a monthly recurring
donation limit and make recurring donations of specified amounts to individual
campaigns. To support this our command-line interface will need to accept input
from STDIN or from a file passed as an argument to the command-line tool. For
example:

``` shell
cat input.txt | recurring

recurring input.txt
```

should produce the same output.

The command-line tool will need to accept 3 different commands, one to add a
campaign, one to add a donor, and one to set up a recurring donation for a given
donor to a given campaign. The following commands will set up a recurring monthly
donation of \$100 from a donor named Greg with a limit of \$1000 to a campaign
named SaveTheDogs:

``` text
Add Donor Greg $1000
Add Campaign SaveTheDogs
Donate Greg SaveTheDogs $100
```

Any `Donate` command that would cause the monthly total donation to go over the
limit specified in the `Add Donor` command should be ignored. After the entire
input is consumed by the tool, it should print a summary and exit with a
successful exit code. The summary should consist of each Donor's total donations
for a month, each Donor's average donation size, and each Campaign's total
received donations for a month. There should be separate sections for Donors and
Campaigns, and the Donors and Campaigns should be printed in alphabetical order.
The following input

``` text
Add Donor Greg $1000
Add Donor Janine $100
Add Campaign SaveTheDogs
Add Campaign HelpTheKids
Donate Greg SaveTheDogs $100
Donate Greg HelpTheKids $200
Donate Janine SaveTheDogs $50
```

Should result in exactly the following output:

``` text
Donors:
Greg: Total: $300 Average: $150
Janine: Total: $50 Average: $50

Campaigns:
HelpTheKids: Total: $200
SaveTheDogs: Total: $150
```

# Requirements

This problem is designed to be possible to do with the standard libraries of
most languages; please do not use external libraries or tools. Exceptions to
these guidelines are test libraries and build tools. Our goal is to
understand how you would solve this problem, not if you know the correct
libraries and tools to find to solve the problem.

Your submission should include:
- The full source for the implementation of your solution to the above problem.
- Tests that verify that your solution works correctly
- An informative README that
  1. explains the steps necessary to build and run your solution.

     You may assume that evaluators have the ability to install the necessary
     tools to build your solution, but you should not assume they have any tools
     installed beyond a terminal and a shell.

  2. describes how your solution should be tested
  3. describes the process and rationale behind the solution you have submitted
- After an evaluator follows your instructions, there should be a single
  executable file named `recurring` in the submission directory. This file
  can be an executable or a shell script. The evaluator will test that your
  submissions works by invoking the following commands and comparing the output
  to the specified correct output:

  ```shell
  cat input.txt | ./recurring
  ./recurring input.txt
  ```

Please submit your take-home as a zipped file via the linked provided and do not share it on any public pages. 
  
# Evaluation Criteria

We will evaluate your submission in the following areas:

1. Correctness
   Does your solution produce the intended output given the sample input?
2. Domain Modeling
   Is your code structured in a way that related data and/or behavior is
   organized together? Note: this does not necessarily mean that your submission
   must be implemented in an object-oriented style.
3. Best practices 
   Does your submission adhere to the practices and idioms of
   your chosen language? Are variables, functions, etc well named to clarify
   intent? Is your submission free of obvious errors, clean of commented-out or
   unreachable code, simple?
4. Documentation 
   Does your submission's README include adequate instructions for
   the evaluator to compile your submission? Does your submission include
   adequate instructions for the evaluator to run any tests you include in your
   submission? Is your submission mostly self-documenting with text
   documentation added to clarify sections that might otherwise be unobvious? Does your README describe the process and rationale behind the solution you have submitted?