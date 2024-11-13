import argparse
from src.code_parser import parse_codebase
from src.readme_generator import generate_readme
from src.file_writer import write_readme
from tqdm import tqdm  # For progress bar


def main():
    parser = argparse.ArgumentParser(description="Generate a README.md file for your project.")
    parser.add_argument("--path", "-p", type=str, default=".", help="Path to the project directory.")
    parser.add_argument("--output", "-o", type=str, default="README.md", help="Path to save the generated README.md.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose mode for detailed output.")
    args = parser.parse_args()

    print(f"Parsing codebase at {args.path}...")
    with tqdm(total=3, desc="Generating README") as progress_bar:
        project_details = parse_codebase(args.path)
        progress_bar.update(1)
        readme_content = generate_readme(project_details)
        progress_bar.update(1)
        write_readme(readme_content, args.output)
        progress_bar.update(1)

    print(f"README.md generated successfully at {args.output}")


if __name__ == "__main__":
    main()
