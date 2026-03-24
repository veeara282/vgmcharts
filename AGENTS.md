- Python code should conform to the Black formatter's style guide. Some of the most
  important style rules are:
  - String literals are generally delimited by "double quotes". Strings that contain
    quotation marks may be formatted using single quotes, e.g. 'quoted "text"'.
  - Lines should generally be at most 88 characters long, although comments can go
    slightly over.
  Generated code need not perfectly adhere to the Black style rules. It may be helpful
  to run Black (`uv run black .` from the `pipelines` directory) after generating code.
- Comments should concisely summarize the parts of the code that follow them and should
  not over-explain implementation details.
