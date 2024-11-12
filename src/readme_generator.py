from ollama import Client


def generate_readme(project_details):
    client = Client()
    prompt = f"""
    You are a README generator. Based on the following project details, generate a professional README.md:

    Project Name: {project_details['project_name']}
    Key Files: {', '.join(project_details['files'][:5])}
    Key Functions: 
    {''.join(f"- {func}\n" for func in project_details['key_functions'])}

    Include sections for Installation, Usage, and License.
    """

    response = client.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    print(response)  # Add this to inspect the response structure
    return response
