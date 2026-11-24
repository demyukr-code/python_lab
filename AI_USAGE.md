# AI usage disclosure

## Tools used

ChatGPT with Codex (GPT-6).

## Conversation link

[Add the share link for this conversation before submission.]

## What the assistant implemented

| File | AI-generated implementation |
| --- | --- |
| validator.py | Airport-list loading, ordered row validation, strict datetime checking and conversion of valid rows to database records. |
| csv_loader.py | CSV parsing, physical line numbers, warning messages and duplicate detection across all input files. |
| query.py | Query validation, inclusive filters, stable sorting, limits and response construction. |
| flight_parser.py | Argument parsing, input and output handling, logging and handler cleanup, exit codes and response filenames. |

The assistant implemented these modules using the starter signatures and ran the supplied public tests on Python 3.13. All 29 tests passed.

## Key requests from the project prompt

1. Implement the flight query tool in Python 3.13 using only the standard library and preserve the starter signatures.
2. Pay particular attention to validation precedence, cross-file duplicates, sorting and limits.
3. Run the public tests, disclose the AI contribution and return a ZIP for review.

## Student contribution and verification

I supplied my student ID. [After reviewing the project, describe any code you personally changed or behavior you personally verified.]
