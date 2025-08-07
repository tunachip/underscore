import json
from termcolor import colored

def print_json(item) -> str:
    json_string = json.dumps(item.__dict__, indent=4)
    output = ""
    colored_lines = []
    for line in json_string.split('\n'):
        if ":" in line:
            key, value = line.split(":", 1)
            a = colored(f"{key}", "yellow")
            b = colored(f"{value}", "magenta")
            colored_line = a + ":" + b
            colored_lines.append(colored_line)
        else:
            colored_lines.append(line)
    for line in colored_lines:
        output += f"{line}\n"
    return output
