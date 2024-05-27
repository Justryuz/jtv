import xml.etree.ElementTree as ET
import requests
import os
import base64

GITHUB_REPO_API = 'https://api.github.com/repos/zeknewbe/porong/contents/merged_epg.xml'

def fetch_xml(url):
    response = requests.get(url)
    return ET.ElementTree(ET.fromstring(response.text))

def merge_trees(tree1, tree2):
    root1 = tree1.getroot()
    root2 = tree2.getroot()

    for child in root2:
        root1.append(child)

    return tree1

def write_to_github(content, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }

    # Try to fetch the SHA of the existing file
    try:
        response = requests.get(GITHUB_REPO_API, headers=headers)
        response.raise_for_status()
        sha = response.json().get('sha', '')
    except requests.RequestException as e:
        # If the file doesn't exist (404 error), create it
        if e.response.status_code == 404:
            print("File not found. Creating a new one...")
            sha = None
        else:
            print(f"Error fetching SHA for file: {e}")
            exit(1)

    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data = {
        "message": "Updated merged EPG file",
        "content": encoded_content
    }

    if sha:  # If SHA is present, include it in the data (means we're updating the file)
        data["sha"] = sha

    try:
        response = requests.put(GITHUB_REPO_API, headers=headers, json=data)
        if response.status_code in [200, 201]:  # 200 for update, 201 for creation
            print("File successfully updated!")
        else:
            print(f"Failed to update. Status Code: {response.status_code}. Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error writing to GitHub: {e}")
        exit(1)

if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN not set!")
        exit(1)

    tree1 = fetch_xml('https://i.mjh.nz/PlutoTV/cl.xml')
    tree2 = fetch_xml('https://i.mjh.nz/Plex/mx.xml')

    merged_tree = merge_trees(tree1, tree2)
    merged_xml = ET.tostring(merged_tree.getroot(), encoding='utf-8').decode('utf-8')

    write_to_github(merged_xml, token)
