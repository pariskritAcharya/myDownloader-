import os
import threading
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVES_DIR = os.path.join(BASE_DIR, 'saves')
QUEUE_FILE = os.path.join(SAVES_DIR, 'queue.json')
HISTORY_FILE = os.path.join(SAVES_DIR, 'history.json')
SETTINGS_FILE = os.path.join(SAVES_DIR, 'settings.json')
os.makedirs(SAVES_DIR, exist_ok=True)

queue_lock = threading.Lock()
history_lock = threading.Lock()
settings_lock = threading.Lock()

def get_address():
    return {
        "base": BASE_DIR,
        "saves": SAVES_DIR,
        "queue": QUEUE_FILE,
        "history": HISTORY_FILE,
        "settings": SETTINGS_FILE
    }

def get_settings():
    with settings_lock:
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
                settings = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            settings = {} # Fall back to empty if error 
    return settings


def get_queue():
    with queue_lock:
        try:
            with open(QUEUE_FILE, 'r', encoding='utf-8') as file:
                data_list = json.load(file)
            
        except (FileNotFoundError , json.JSONDecodeError):
            data_list = [] # see if {} or []
            
            with open(QUEUE_FILE, 'w', encoding='utf-8') as file:
                    json.dump(data_list, file, indent=4)
    return data_list


def add_to_queue(job_details):
    with queue_lock:
        with open(QUEUE_FILE, 'r', encoding='utf-8') as file:
                read_data = json.load(file)
        
        read_data.append(job_details)
        with open(QUEUE_FILE, 'w', encoding='utf-8') as file:
            json.dump(read_data,file,indent=4)
    
def dequeue_from_queue(job_details):
    with queue_lock:
        with open(QUEUE_FILE, 'r', encoding='utf-8') as file:
                    read_data = json.load(file)
        updated_data = [item for item in read_data if item.get("url") != job_details["url"] ]
    
        with open(QUEUE_FILE,'w', encoding='utf-8') as file:
            json.dump(updated_data,file,indent=4)

    
    




def update_title(job_details):
    # Update for queue file
    with queue_lock:
        try:
            with open(QUEUE_FILE, 'r', encoding='utf-8') as file:
                queue_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            queue_data = []

        for data in queue_data:
            if data["url"] == job_details["url"]:
                data["title"] = job_details["title"] 
                break

        with open(QUEUE_FILE, 'w', encoding='utf-8') as file:
            json.dump(queue_data, file, indent=4)   

    # Insert in history with an id
    with history_lock:
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
                history_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            history_data = []
        
        max_index = 0
        for data in history_data:
            if data.get("index", 0) > max_index:
                max_index = data["index"]

        # Increment by 1 to create a unique ID
        job_details["index"] = max_index + 1
        history_data.append(job_details)

        with open(HISTORY_FILE, 'w', encoding='utf-8') as file:
            json.dump(history_data, file, indent=4)



