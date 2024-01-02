import os
import sys
from bs4 import BeautifulSoup


def get_element_data(soup, tag, file_name):
    # Find all tags of the specified type
    tags = soup.find_all(tag)

    results = []
    # Extract and print attributes for each tag
    for element in tags:
        attributes = element.attrs
        _src = attributes.get("src", "null")
        _href = attributes.get("href", "null")
        _rel = attributes.get("rel", "null")
        _type = attributes.get("type", "null")
        _is_external = _src.startswith("http") or _href.startswith("http")
        results.append(
            (
                file_name,
                tag,
                _src,
                _href,
                _type,
                "+".join(_rel) if isinstance(_rel, list) else _rel,
                "TRUE" if _is_external else "FALSE",
            )
        )

    return results


def get_elements_data_for_file(file_path):
    # Open and read the HTML file
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    results = []
    tags = ("link", "script", "a", "iframe", "img")

    for tag in tags:
        results.extend(get_element_data(soup, tag, file_path))

    return results


def iterate_over_files(directory_path):
    print("iterate_over_files: ", directory_path)
    # Iterate over files in the directory
    results = []
    for filename in os.listdir(directory_path):
        print(filename, end="=>")

        if filename.endswith(".html"):
            print("is html file")
            file_path = os.path.join(directory_path, filename)
            elements = get_elements_data_for_file(file_path)
            results.extend(elements)

        elif os.path.isdir(os.path.join(directory_path, filename)):
            print("is dir")
            # print("Directory found: ", filename)
            subdirectory_path = os.path.join(directory_path, filename)
            elements = iterate_over_files(subdirectory_path)
            results.extend(elements)

        else:
            print("is not html file")

    return results


if __name__ == "__main__":
    try:
        directory_path = sys.argv[1]
    except IndexError:
        print("Please provide a directory path")
        sys.exit(1)

    results = iterate_over_files(directory_path)

    with open("results.csv", "a", encoding="utf-8") as file:
        file.write("file_name,tag,src,href,type,rel,is_external\n")
        for result in results:
            row = f"""{",".join(list(result))}\n"""
            file.write(row)
