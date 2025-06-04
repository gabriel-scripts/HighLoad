import pytubefix
import os
import requests

from pytubefix.cli import on_progress
from pytubefix import YouTube

def download(links: list, destination: str, option: str):
    if not links:
        return print("Lista de links vazia.")
    
    if not os.path.exists(destination):
        print("Pasta não existe, criando uma.")
        os.makedirs(destination)
    
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    for link in links:
        try:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                video = pytubefix.YouTube(link)
                if option == "audio":
                    stream = video.streams.filter(only_audio=True).first()
                elif option == "video":
                    stream = video.streams.get_highest_resolution()
                if stream:
                    stream.download(output_path=destination)
                    status = f"Download de áudio concluído: {link} -> {os.path.join(destination, stream.default_filename)}"
                else:
                    status = f"Não foi possível encontrar um stream de áudio para o vídeo: {link}"
            else:
                status = f"Erro ao acessar o vídeo {link}: {response.status_code}"
        except Exception as e:
            status = f"Erro ao baixar o áudio do vídeo {link}: {str(e)}"
    return status

