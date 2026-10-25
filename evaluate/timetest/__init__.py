log_file = None


def log(text):
    """Very simple logger. Prints the statement to the console and to a set log file."""
    print(text)
    if log_file is not None:
        log_file.write(text+'\n')