import threading
import queue
from downloader import ytDownloader


# 1. Create the RAM queue
dl_queue = queue.Queue()

# 2. Define the background worker function
def download_worker():
    while True:
        # .get() pauses the loop here until a new URL is added to the queue
        job = dl_queue.get() 
        
        print(f"Background: Downloading {job['url']}...")
        ytdl = ytDownloader()
        ytdl.download_audio
        print("Background: Download complete!")
        
        # Tells the queue the job is finished
        dl_queue.task_done() 

# 3. Start the thread before running your main loop
# daemon=True ensures the thread is killed automatically when you close the main app window
worker = threading.Thread(target=download_worker, daemon=True)
worker.start()

# 4. Simulate the UI adding a job
dl_queue.put({"url": "https://youtube.com/test_video"})