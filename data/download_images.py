import glob
import requests
import json

from tqdm.cli import tqdm
from concurrent.futures import ThreadPoolExecutor

def download_file(path,):
    with open(path,"r") as file:
        image_urls = file.read().split("\n")
    broken = []
    for line in tqdm(image_urls):
        name,url = line.split("\t")
        with open(f"./images/{name}.jpg","wb") as image:
            with requests.get(url) as response:
                if response.status_code == 200:
                    image.write(response.content)
                else:
                    broken.append([file,url])
    return broken


def main():
    files = glob.glob("./image_url/*.txt")
    with ThreadPoolExecutor(max_workers=6) as executer:
        res = executer.map(download_file,files)
    
    broken = []
    for r in res:
        broken += r

    open("./broken.json","r").write(json.dumps(broken))

if __name__ == "__main__":
    main()