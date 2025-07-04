import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from index import add_to_index, save_index
from embeddings import generate_embeddings
from config import DIRECTORY_TO_USE_RAG, IGNORE_PATHS

def should_ignore_path(path):
    for ignore_path in IGNORE_PATHS:
        if path.startswith(ignore_path):
            return True
    return False

class CodeChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory or should_ignore_path(event.src_path):
            return

        if event.src_path.endswith(".py"):
            print(f"changes in file: {event.src_path}")
            with open(event.src_path, 'r', encoding='utf-8') as f:
                full_content = f.read()
            embeddings = generate_embeddings(full_content)
            if embeddings is not None and len(embeddings) > 0:
                filename = os.path.basename(event.src_path)
                add_to_index(embeddings, full_content, filename, event.src_path)
                save_index()
                print(f"Updated FAISS index for file: {event.src_path}")

def start_monitoring():
    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=DIRECTORY_TO_USE_RAG, recursive=True)
    observer.start()
    print(f"Started monitoring {DIRECTORY_TO_USE_RAG}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
