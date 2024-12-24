import re
import requests

base_url = 'https://download.eclipse.org/jdtls/milestones/'

def get_latest_version():
    milestones_res = requests.get(base_url, allow_redirects=True)
    if(milestones_res.status_code != 200):
        raise Exception('Failed to get all versions from milestones page')
    version_match_regex = r"<a href='(.*?)'> (\d*.\d*.\d*.)</a>"
    matches = re.findall(version_match_regex, milestones_res.text)
    versions = [match[1] for match in matches]

    sorted_versions = sorted(versions, key=lambda x: list(map(int, x.split('.'))))
    return sorted_versions[-1]
version = get_latest_version()
print(version)
