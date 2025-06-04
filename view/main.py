from tkinter import *
from tkinter import filedialog, messagebox

import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from index import download

CONFIG_FILE = os.path.expanduser("~/.highload_config.json")

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_last_folder():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_folder")
    return ""

def save_last_folder(folder):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"last_folder": folder}, f)

def start_download(destination, root, links, option):
    if not links:
        messagebox.showinfo("Cancelado", "Nenhum link adicionado.")
        return
    download(links, destination[0], option)
    messagebox.showinfo("Concluído", "Downloads finalizados.")

def add_link(entry_link, links, listbox_links):
    link = entry_link.get().strip()
    if link:
        links.append(link)
        listbox_links.insert(END, link)
        entry_link.delete(0, END)

def remove_selected(links, listbox_links):
    selected = listbox_links.curselection()
    for i in reversed(selected):
        links.pop(i)
        listbox_links.delete(i)

def choose_folder(destination, label_folder):
    folder = filedialog.askdirectory(title="Selecione a pasta de download")
    if folder:
        destination[0] = folder
        save_last_folder(folder)
        label_folder.config(text=f"Pasta: {folder}")


def add_hover_effect(button):
    def on_enter(e):
        button['bg'] = "#666694"
    def on_leave(e):
        button['bg'] = "#2b2b52"
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def main():

    # COLORS:
    background = "#00021A"

    frame_background = "#00021A"
    frame_light_background = "#2b2b52"

    button_background = "#2b2b52"
    label_background = "#2b2b52"
    list_box_background = "#2b2b52"
    text_color = "#fff"

    # window
    root = Tk()
    root.title("highload")
    root.geometry("720x420")
    root.configure(bg = background)

    icon = PhotoImage(file=resource_path("assets/highload.png"))
    root.iconphoto(True, icon)

    last_folder = load_last_folder()
    destination = [last_folder] if last_folder else [""]

    links = []

    frame_folder = Frame(root, bg = frame_light_background)
    frame_folder.pack(pady=5)
    label_folder = Label(frame_folder, text=f"Pasta: {destination[0] or 'Nenhuma selecionada'}", bg=label_background, fg = text_color, bd=0, padx=20, pady=10)
    label_folder.pack(side=LEFT, padx=5)
    Button(
        frame_folder, text="Selecionar pasta",
        bg = button_background, fg= text_color, bd=0, padx=20, pady=10, highlightthickness=0,
        command=lambda: choose_folder(destination, label_folder)
    ).pack(side=LEFT)

    link_entry_button_frame = Frame(root, bg = frame_light_background)
    link_entry_button_frame.pack(pady=20)
    entry_link = Entry(link_entry_button_frame, width=50, bg="#666694", fg = text_color,  borderwidth=0, highlightthickness=0)
    entry_link.pack(side=LEFT)

    placeholder_text = " Cole o link aqui..."
    entry_link.insert(0, placeholder_text)
    entry_link.config(fg="#c5c5c5") 

    def on_entry_focus_in(event):
        if entry_link.get() == placeholder_text:
            entry_link.delete(0, END)
            entry_link.config(fg=text_color)

    def on_entry_focus_out(event):
        if not entry_link.get():
            entry_link.insert(0, placeholder_text)
            entry_link.config(fg="#c5c5c5")

    entry_link.bind("<FocusIn>", on_entry_focus_in)
    entry_link.bind("<FocusOut>", on_entry_focus_out)

    Button(
        link_entry_button_frame, text="Adicionar link",
        bg = button_background, fg = text_color, bd=0, padx=25, pady=10, borderwidth=0, highlightthickness=0,
        command=lambda: add_link(entry_link, links, listbox_links)
    ).pack(side=LEFT, padx=5)

    option = StringVar(value="audio") 

    option_frame = Frame(root, bg=frame_background)
    option_frame.pack(pady=5)

    label_option = Label(option_frame, text="Escolha o formato:", bg=frame_background, fg=text_color)
    label_option.pack(side=LEFT, padx=5)

    radio_audio = Radiobutton(
        option_frame, text="Áudio", variable=option, value="audio",
        bg=frame_background, fg=text_color, selectcolor=frame_light_background, activebackground=frame_background, activeforeground=text_color, highlightthickness=0
    )
    radio_audio.pack(side=LEFT, padx=5)

    radio_video = Radiobutton(
        option_frame, text="Vídeo", variable=option, value="video",
        bg=frame_background, fg=text_color, selectcolor=frame_light_background, activebackground=frame_background, activeforeground=text_color, highlightthickness=0
    )
    radio_video.pack(side=LEFT, padx=5)

    listbox_links = Listbox(root, width=70, height=10, bg=list_box_background, fg= text_color, borderwidth=0, highlightthickness=0)
    listbox_links.pack(pady=5)

    action_buttons_frame = Frame(root, bg = frame_background)
    action_buttons_frame.pack(pady=5)

    button_remove_link = Button(
        action_buttons_frame, text="Remover selecionado",
        command=lambda: remove_selected(links, listbox_links),
        bg = button_background, fg = text_color, bd=0, padx=20, pady=10, borderwidth=0, highlightthickness=0
    )

    button_remove_link.pack(side=LEFT, padx=5)
    add_hover_effect(button_remove_link)

    button_start_download = Button(
        action_buttons_frame, text="Iniciar download",
        command=lambda: start_download(destination, root, links, option.get()),
        bg = button_background, fg = text_color, bd=0, padx=20, pady=10, borderwidth=0, highlightthickness=0
    )

    button_start_download.pack(side=LEFT, padx=5)
    add_hover_effect(button_start_download)
    
    button_quit = Button(
        action_buttons_frame, text="Sair", command=root.destroy,
        bg = button_background, fg = text_color, bd=0, padx=20, pady=10, borderwidth=0, highlightthickness=0
    )
    button_quit.pack(side=LEFT, padx=5)
    add_hover_effect(button_quit)

    if last_folder:
        label_folder.config(text=f"Pasta: {last_folder}")

    root.mainloop()

if __name__ == "__main__":
    main()