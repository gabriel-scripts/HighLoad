# Download musics and videos with no ads

![alt text](assets/image.png)

## how to build:

Linux
```bash
pyinstaller --onefile --noconsole --add-data "assets/highload.png:assets" view/main.py
```

Windows
```bash
pyinstaller --onefile --noconsole --add-data "assets/highload.png;assets" view/main.py
```