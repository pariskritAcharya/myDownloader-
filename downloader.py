import yt_dlp
from file_manager import get_settings,update_title
import os 

class ytDownloader:
    def __init__(self):
        settings = get_settings()    
             
        self.output_dir = settings.get("downloadFolder", "./downloads")
        self.quality = settings.get("audioQuality", "best")
        self.audioFormat = settings.get("audioFormat", "mp3")
        self.videoFormat = settings.get("videoFormat", "mp4")
        self.last_percent = 0
        os.makedirs(f"{self.output_dir}/audio", exist_ok=True)
        os.makedirs(f"{self.output_dir}/video", exist_ok=True)
 
        

    def download_audio(self,job_details) -> None:
        ydl_opts = { 
            'format': 'bestaudio/best', #quality only audio
            'outtmpl': self.output_dir +'/audio/'+ '%(title)s.%(ext)s', #output template / path
            'playlistend': int(job_details["downloadNumber"]), 
            'progress_hooks': [self._get_progress_hook(job_details,self.last_percent)],
            # 'no_warnings': True,
            'noprogress': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec' : self.audioFormat,
                'preferredquality': self.quality
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([job_details["url"]])

    def download_video(self, job_details) ->None:
       
        ydl_opts ={
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': self.output_dir +'/video/'+ '%(title)s.%(ext)s',
            'playlistend': int(job_details["downloadNumber"]), 
            'progress_hooks': [self._get_progress_hook(job_details,self.last_percent)],
            # 'no_warnings': True,
            'noprogress': True,
            'merge_output_format': 'mp4'

        }
        # Execute the download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([job_details["url"]])

    def _get_progress_hook(self, job_details, last_percent):
        def hook(d):
            if d["status"] == "downloading":
               
                #1. capture title
                real_title = d.get("info_dict", {}).get("title", "Unknown")
                
                # Prevent spamming the update on every single download chunk
                if job_details.get("title") != real_title:
                    job_details["title"] = real_title
                    print(f"\n[MY DOWNLOADER]Captured title mid-flight: {real_title}")
                    update_title(job_details=job_details)

                #2. capture download progress
                percentage_status = d.get('_percent_str', '0%').strip()

                if percentage_status != last_percent:
                    self.last_percent = percentage_status
                    print(f"[MY DOWNLODER] Download progress:{percentage_status}")
                 

        return hook