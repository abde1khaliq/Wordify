import requests
import json
import os
from packaging import version

url = 'https://raw.githubusercontent.com/abde1khaliq/Wordify/main/app/config/wordify.json'


def check_for_updates():
    try:
        config_path = os.path.join(os.path.dirname(__file__), "config", "wordify.json")
        with open(config_path, 'r') as file:
            local_config = json.load(file)

        response = requests.get(url)
        remote_config = response.json()

        local_version = version.parse(local_config['version'])
        remote_version = version.parse(remote_config['version'])

        if remote_version > local_version:
            print(f"🔔 Update available: {remote_config['version']}")
            return False
        else:
            print("✅ This application is up to date.")
            return True

    except Exception as error:
        print("❌ An error occurred in the updater module:", error)
        return None