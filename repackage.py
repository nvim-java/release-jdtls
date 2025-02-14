import re
import requests
from urllib.parse import urljoin
import tarfile
import os
import tempfile
from shutil import copyfile 

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

def get_jdtls_download_url(version):
    url = urljoin(base_url, f'{version}/latest.txt')
    pkg_name_res = requests.get(url)
    file_name = pkg_name_res.text.strip()
    return urljoin(base_url, f'{version}/{file_name}')

def get_equinox_launcher_name(version):
    plugins_res = requests.get(f"https://download.eclipse.org/jdtls/milestones/{version}/repository/plugins/")
    pattern = r"<a .*?>(org.eclipse.equinox.launcher_.*?.jar)</a>"
    matches = re.findall(pattern, plugins_res.text)

    if len(matches) < 1:
        raise Exception('Could not find the equinox launcher plugin')

    if len(matches) > 1:
        raise Exception('Found more than one equinox launcher plugin')

    return matches[0]

def download_file(url):
    with tempfile.TemporaryDirectory() as tmp:
        res = requests.get(url)
        file_path = urljoin(tmp, 'jdtls.tar.gz')
        with open(file_path, 'wb') as file:
            file.write(res.content)
        return file_path

def extract_tar_gz(tar_gz_path, equinox_plugin_path):
    with tarfile.open(tar_gz_path, "r:gz") as tar:
        with tempfile.TemporaryDirectory() as tmp:
            ex_dir = f'{tmp}/jdtls'
            tar.extractall(path=ex_dir)
            # creating a hard link instead of moving the file
            # https://github.com/nvim-java/release-jdtls/issues/1
            os.link(f'{ex_dir}/plugins/{equinox_plugin_path}', f'{ex_dir}/plugins/org.eclipse.equinox.launcher.jar')
            # move(f'{ex_dir}/plugins/{equinox_plugin_path}', f'{ex_dir}/plugins/org.eclipse.equinox.launcher.jar')
            with tempfile.TemporaryDirectory() as tmpout:
                out_path = f'{tmpout}/jdtls.tar.gz'
                with tarfile.open(out_path, "w:gz") as tarout:
                    for file in os.listdir(ex_dir):
                        tarout.add(f'{ex_dir}/{file}',arcname=file, recursive=True)
                copyfile(f'{tmpout}/jdtls.tar.gz', './jdtls.tar.gz')



if os.environ.get('jdtls_version'):
    is_custom_version = True
    version = os.environ.get('jdtls_version')
else:
    is_custom_version = False
    version = get_latest_version()

print(f"re-packaging version {version}")

download_url = get_jdtls_download_url(version)
equinox_plugin_path = get_equinox_launcher_name(version)
downloaded_path = download_file(download_url)
extract_tar_gz(downloaded_path, equinox_plugin_path)
