import feedparser
import requests
import argparse
import os
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.description='please enter the path to save LoudMurmurs audios...'
parser.add_argument("-p", "--path", help="path to save", type=str, default=os.path.split(os.path.realpath(__file__))[0])

args = parser.parse_args()
save_dir = os.path.join(args.path, "LoudMurmurs")
os.makedirs(save_dir, exist_ok=True)

url = 'https://loudmurmursfm.com/feed/audio.xml'
data=feedparser.parse(url) 


def download(url: str, fname: str):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', -1))
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1023,
    ) as bar:
        for data in resp.iter_content(chunk_size=1023):
            size = file.write(data)
            bar.update(size)


for idx, one in enumerate(data.entries):
    print('Total download procress: ' + str(idx+1) + ' / ' + str(len(data.entries)))

    title = one.title.replace('"', '')
    url = one.links[0].href

    save_name = title + ".mps"
    save_path = os.path.join(save_dir, save_name)

    download(url, save_path)



