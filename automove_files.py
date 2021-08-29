from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json 
import re
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

class FileHandler(FileSystemEventHandler):

    def set_config(self, config_file_name: str):
        with open(config_file_name, 'r') as file:
            config = json.load(file)
        self.folder_to_track = config['folder_to_track']
        self.regex_text = config['regex_text']
        self.regex_code = config['regex_code']
        self.regex_documents = config['regex_documents']
        self.regex_images = config['regex_images']
        self.regex_videos = config['regex_videos']
        self.regex_zip = config['regex_zip']
        self.regex_audio = config['regex_audio']
        return self.folder_to_track

    def move_file(self, src: str, dst: str):
        if os.path.exists(dst):
            print("File already exists: %s" % dst)
        else:
            try:
                os.rename(src, dst)
                print("File moved: %s" % dst)
            except Exception as e:
                try:
                    file = dst.split('/')[-1]
                    os.makedirs(dst.replace(file, ''))
                    self.move_file(src, dst)
                except Exception as e:
                    print("Error moving file: %s" % e)

    def on_modified(self, event: FileSystemEvent):
        for filename in os.listdir(self.folder_to_track):
        
            date_today = datetime.now().strftime("%Y_%m_%d_")
            r_text = re.compile( self.regex_text, re.IGNORECASE )
            r_code = re.compile( self.regex_code, re.IGNORECASE )
            r_documents = re.compile( self.regex_documents, re.IGNORECASE )
            r_images = re.compile( self.regex_images, re.IGNORECASE )
            r_videos = re.compile( self.regex_videos, re.IGNORECASE )
            r_zip = re.compile( self.regex_zip, re.IGNORECASE )
            r_audio = re.compile( self.regex_audio, re.IGNORECASE )
            text = r_text.search(filename)
            code = r_code.search(filename)
            documents = r_documents.search(filename)
            images = r_images.search(filename)
            videos = r_videos.search(filename)
            zipp = r_zip.search(filename)
            audio = r_audio.search(filename)
            if text:
                new_name = filename.replace(text.group(), date_today + "_" + text.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/Text/"+ new_name
                self.move_file(src, dst)
            elif code:
                new_name = "_" + filename.replace(code.group(), date_today + code.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/Code/"+ new_name
                self.move_file(src, dst)
            elif documents:
                new_name = filename.replace(documents.group(), date_today + documents.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/Documents/"+ new_name
                self.move_file(src, dst)
            elif images:
                new_name = filename.replace(images.group(), date_today + images.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/Images/"+ new_name
                self.move_file(src, dst)
            elif videos:
                new_name = filename.replace(videos.group(), date_today + videos.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/Videos/"+ new_name
                self.move_file(src, dst)

            elif zipp:
                new_name = filename.replace(zipp.group(), date_today + zipp.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/Zipp/"+ new_name
                self.move_file(src, dst)
            elif audio:
                new_name = filename.replace(audio.group(), date_today + audio.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/Audio/"+ new_name
                self.move_file(src, dst)
            else:
                pass



def main():
    event_handler = FileHandler()
    folder_to_track = event_handler.set_config('config.json')
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduler.start, 'interval', seconds=3)
    observer.join()
  

if __name__ == "__main__":
    main()
