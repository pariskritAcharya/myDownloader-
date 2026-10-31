import queue

import threading
from downloader import ytDownloader
from file_manager import  add_to_queue ,dequeue_from_queue

download_queue = queue.Queue()
ram_lock = threading.Lock()
active_job = None

def enqueue(url:str,format:str,downloadNumber:int):
    job_details = {}
    job_details["url"] = url        # url of the video / audio
    job_details["format"] = format  # video or audio?
    job_details["downloadNumber"] = downloadNumber #total number of video/ audio to download in a sequence
    #add downloadID to the downloads that marks history of download
   
    ytdl = ytDownloader()
    # job_details["title"],job_details["duration"] = ytdl.get_info(job_details["url"])
    job_details["title" ] = "fetching..."
    print(f"[MY DOWNLOADER] Current title = {job_details["title"]}")
    
    #locking while inserting 
    with ram_lock:
        download_queue.put(job_details)

    #append to .json file
    add_to_queue(job_details=job_details)


def dequeue(job_details):
    
    #remove the json data which matched the given url
    dequeue_from_queue(job_details=job_details)

def get_live_snapshot():
    """CustomTkinter will call this every 2 seconds to draw the screen."""
    with ram_lock:
        # .queue accesses the hidden internal list of waiting jobs
        snapshot = list(download_queue.queue)
        
        # If a video is currently downloading, add it to the top of the UI list
        if active_job:
            snapshot.insert(0, active_job)
            
        return snapshot 

def background_download_worker():
    global active_job
    while True:
        job_details = download_queue.get()
        print(f"[MY DOWNLOADER] starting downloading {job_details["title"]} ....")
        with ram_lock:
            active_job = job_details
        ytdl = ytDownloader()
        
        if(job_details["format"] == "audio"):
            ytdl.download_audio(job_details=job_details)
        else:
            ytdl.download_video(job_details=job_details)
        
        download_queue.task_done()
        dequeue(job_details)
        
        with ram_lock:
            active_job = None  # Clear it when finished

        print("[MY DOWNLOADER] download completed.....")

def run_background_worker():
    worker = threading.Thread(target=background_download_worker,daemon=True)
    worker.start()
    print("[MY DOWNLOADER] background work thread started")


