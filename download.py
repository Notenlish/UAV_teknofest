import os
import requests
import zipfile


def download_and_extract_zip(url, extract_to):
    zip_path = 'temp.zip'
    extract_dir = os.path.join("datasets", extract_to)

    response = requests.get(url, stream=True)
    with open(zip_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    os.remove(zip_path)

if __name__ == '__main__':
    our_datasets = {  # 7.9k images
        "actualdataset":"https://app.roboflow.com/ds/8TE4Iz67oq?key=5XERbvKokU"
    }

    for folder_name, link in our_datasets.items():
        download_and_extract_zip(link, folder_name)