import re

def parse_log_line(line):
    log_pattern = r'^(?P<timestamp>[^,]+),(?P<level>[^,]+),(?P<service>[^,]+),(?P<message>.+)$'
    match = re.match(log_pattern, line)
    if match:
        return match.groupdict()
    return None
    
    # groupdict() -> convert raw data into structure data (dictionary)
    # r'' -> raw Data
    # ?P<timestamp> -> named group
    # #s+ -> for spaces one or more
    # ^ -> start of line
    # $ -> end of line
    # \S -> non space character