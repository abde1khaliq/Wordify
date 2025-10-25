import requests
import json
import os
from packaging import version
from res_path import resource_path

url = 'https://raw.githubusercontent.com/abde1khaliq/Wordify/refs/heads/master/wordify.json'

def check_for_updates():
    try:
        with open(resource_path("wordify.json"), 'r') as file:
            local_config = json.load(file)

        response = requests.get(url)
        remote_config = response.json()

        local_version = version.parse(str(local_config['version']))
        print(local_version)
        remote_version = version.parse(str(remote_config['version']))
        print(remote_config)

        if remote_version == local_version:
            return True
        elif remote_version > local_version:
            return False

    except Exception as error:
        print("❌ An error occurred in the updater module:", error)
        return None