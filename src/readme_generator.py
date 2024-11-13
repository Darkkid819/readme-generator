from pathlib import Path
import os
from datetime import datetime, timedelta
from ollama import Client
import ast


def detect_license(files):
    license_files = [file for file in files if "license" in file.lower()]
    if not license_files:
        return None

    license_path = license_files[0]
    with open(license_path, 'r') as f:
        license_content = f.read().lower()
        if "mit license" in license_content:
            return "MIT"
        elif "gnu general public license" in license_content:
            return "GPL"
        elif "apache license" in license_content:
            return "Apache"
        else:
            return "Custom/Other"


def check_project_inactivity(files):
    now = datetime.now()
    last_modified_dates = [datetime.fromtimestamp(os.path.getmtime(file)) for file in files]
    most_recent = max(last_modified_dates)

    if most_recent < now - timedelta(days=180):
        return True
    return False


def find_entry_point(files):
    for file in files:
        if file.endswith('.py'):
            with open(file, 'r') as f:
                content = f.read()
                if '__main__' in content:
                    return file
    return None


def extract_usage_from_script(script_path):
    usage_info = []
    script_name = Path(script_path).name

    with open(script_path, 'r') as f:
        tree = ast.parse(f.read(), filename=script_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and hasattr(node.func, 'attr') and node.func.attr == 'add_argument':
                args = [ast.literal_eval(arg) for arg in node.args]
                if len(args) >= 2:
                    option, description = args[0], args[1]
                    usage_info.append({
                        'option': option,
                        'description': description
                    })
    return script_name, usage_info


def generate_readme(project_details):
    client = Client()

    project_name = Path(project_details['project_name']).name

    has_tests = any("test" in file.lower() for file in project_details['files'])
    has_ci = any("ci" in file.lower() or "github/workflows" in file.lower() for file in project_details['files'])
    has_setup = any("setup.py" in file.lower() or "requirements.txt" in file.lower() for file in project_details['files'])
    has_docs = any("readme" in file.lower() or "docs" in file.lower() for file in project_details['files'])
    has_visuals = any(file.lower().endswith(('.png', '.jpg', '.gif', '.mp4', '.mov')) for file in project_details['files'])

    license_type = detect_license(project_details['files'])
    is_inactive = check_project_inactivity(project_details['files'])

    entry_point = find_entry_point(project_details['files'])
    if entry_point:
        script_name, usage_examples = extract_usage_from_script(entry_point)
    else:
        script_name, usage_examples = "main.py", []

    prompt = f"""
    You are a README generator. Based on the following project details, generate a professional README.md using these exact headers.

    **Do not include placeholders, extra notes, or 'Replace' messages.**

    # {project_name}

    ## Description
    Provide a clear and engaging description of the project, including its purpose and key features.

    {'' if not (has_ci or has_tests) else '## Badges\nInclude relevant badges, such as build status or test coverage.'}

    {'' if not has_visuals else '## Visuals\nInclude screenshots, GIFs, or videos demonstrating project functionality.'}

    {'' if not has_setup else '## Installation\nProvide detailed installation instructions, including dependencies.'}

    ## Usage
    Provide usage examples based on the following options extracted from the entry point script (`{script_name}`):
    """

    for usage in usage_examples:
        prompt += f"\n- **{usage['option']}**: {usage['description']}\n"

    prompt += f"""
    {'' if not is_inactive else '## Project Status\nThis project appears to be inactive. Suggest updating users about its status and seeking maintainers.'}

    {'' if not license_type else f'## License\nThis project is licensed under the {license_type} license.'}

    {'' if not has_tests else '## Contributing\nProvide guidelines for contributors, including how to run tests.'}

    {'' if not has_docs else '## Support\nMention where users can get help, such as issue trackers or forums.'}

    ## Authors and Acknowledgment
    Credit the authors and contributors.
    """

    response = client.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': prompt.strip(),
        },
    ])

    return response['message']['content'].strip()
