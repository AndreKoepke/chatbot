import os
import requests
import sys
from tqdm import tqdm

# Run this script to download the bigger model
# pip install tensorflow
# Run the command below with the right paths
# python "C:\Users\Ibera\Anaconda3\Lib\site-packages\pytorch_pretrained_bert\convert_gpt2_checkpoint_to_pytorch.py" --gpt2_checkpoint_path "C:\Users\Ibera\IdeaProjects\hitmaschine\chat\data\models\345M" --gpt2_config_file "C:\Users\Ibera\IdeaProjects\hitmaschine\chat\data\config_file" --pytorch_dump_folder_path "C:\Users\Ibera\IdeaProjects\hitmaschine\chat\data\gpt2_345M_pytorch_model"
from data.conver_checkpoint import convert_gpt2_checkpoint_to_pytorch

model = "345M"

subdir = os.path.join('models', model)

if not os.path.exists(subdir):
    os.makedirs(subdir)

subdir = subdir.replace('\\', '/')  # needed for Windows

for filename in ['checkpoint', 'encoder.json', 'hparams.json', 'model.ckpt.data-00000-of-00001', 'model.ckpt.index',
                 'model.ckpt.meta', 'vocab.bpe']:
    # https://storage.googleapis.com/gpt-2/checkpoint/
    r = requests.get("https://storage.googleapis.com/gpt-2/" + subdir + "/" + filename, stream=True)

    with open(os.path.join(subdir, filename), 'wb') as f:

        file_size = int(r.headers["content-length"])

        chunk_size = 1000

        with tqdm(ncols=100, desc="Fetching " + filename, total=file_size, unit_scale=True) as pbar:
            # 1k for chunk_size, since Ethernet packet size is around 1500 bytes

            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)

                pbar.update(chunk_size)
