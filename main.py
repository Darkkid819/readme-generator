from src.code_parser import parse_codebase
from src.readme_generator import generate_readme
from src.file_writer import write_readme


def main():
    project_path = "."
    output_path = "README.md"

    project_details = parse_codebase(project_path)
    readme_content = generate_readme(project_details)
    write_readme(readme_content, output_path)
    print(f"README.md generated successfully at {output_path}")


if __name__ == "__main__":
    main()
