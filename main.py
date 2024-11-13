import argparse
import sys
import time
from itertools import cycle
from pathlib import Path
from threading import Thread
from src.code_parser import parse_codebase
from src.readme_generator import generate_readme
from src.file_writer import write_readme


def spinning_cursor():
    for cursor in cycle(['\\', '|', '/', '-']):
        yield cursor


def display_with_spinner(message, func, *args, **kwargs):
    spinner = spinning_cursor()
    sys.stdout.write(f"{message} ")
    sys.stdout.flush()

    result = None
    spinner_running = True

    def spinner_loop():
        while spinner_running:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

    spinner_thread = Thread(target=spinner_loop)
    spinner_thread.start()

    try:
        result = func(*args, **kwargs)
    finally:
        spinner_running = False
        spinner_thread.join()
        sys.stdout.write("Done!\n")

    return result


def main():
    parser = argparse.ArgumentParser(description="Generate a README.md file for your project.")
    parser.add_argument("--path", "-p", type=str, default=".", help="Path to the project directory.")
    parser.add_argument("--output", "-o", type=str, default="README.md", help="Path to save the generated README.md.")
    args = parser.parse_args()

    project_path = Path(args.path).resolve()
    output_path = Path(args.output).resolve()

    project_details = display_with_spinner(f"Parsing codebase at {project_path}", parse_codebase, str(project_path))
    readme_content = display_with_spinner("Generating README", generate_readme, project_details)
    display_with_spinner(f"Writing to {output_path}", write_readme, readme_content, str(output_path))

    print(f"README.md generated successfully at {output_path}")


if __name__ == "__main__":
    main()
