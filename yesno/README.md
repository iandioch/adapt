# What is this?

Irish has no words for "yes" or "no". When asked `Are you X?`, you would reply `(I) am` or `(I) am not`. In this directory is a tool that, when given a question, creates a report as to the verb form that should be used when responding.

# Setup

## Dependencies

The following tools must be set up before this module can be used:

- [Elaine Uí Dhonnchadha's part of speech tagger for Irish](https://github.com/uidhonne).
- [Maltparser](http://www.maltparser.org/), and trained with [the Irish treebank](https://github.com/tlynn747/IrishDependencyTreebank/blob/master/1020-gold_master_IrishTreebank.conll).

## Config

You must set the paths to the above resources in the variables at the top of the `process.py` file.

# Usage

Run `python3 process.py`. The program will wait for questions to be fed by `stdin`, and will output its report to `stdout`.
