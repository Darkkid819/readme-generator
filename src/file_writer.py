def write_readme(content, output_path):
    with open(output_path, "w") as f:
        f.write(content['message']['content'])