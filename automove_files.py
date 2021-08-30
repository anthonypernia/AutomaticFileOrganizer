from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,FileSystemEvent
import os
import json 
import re
import time
from datetime import datetime


class FileHandler(FileSystemEventHandler):

    def set_config(self, config_file_name: str):
        with open(config_file_name, 'r') as file:
            config = json.load(file)
        self.folder_to_track = config['folder_to_track']
        self.regex_text = config['text']['regex']
        self.regex_code = config['code']['regex']
        self.regex_documents = config['document']['regex']
        self.regex_images = config['image']['regex']
        self.regex_videos = config['video']['regex']
        self.regex_zip = config['zip']['regex']
        self.regex_audio = config['audio']['regex']
        self.folder_text = config['text']['folder']
        self.folder_code = config['code']['folder']
        self.folder_documents = config['document']['folder']
        self.folder_images = config['image']['folder']
        self.folder_videos = config['video']['folder']
        self.folder_zipp = config['zip']['folder']
        self.folder_audio = config['audio']['folder']
        return self.folder_to_track
    #This method mode file acording to de scr - dst
    def move_file(self, src: str, dst: str):
        if os.path.exists(dst):
            #print("File already exists: %s" % dst)
            pass
        else:
            time.sleep(3)
            try:
                os.rename(src, dst)
                print("File moved: %s" % dst)
            except Exception as e:
                try:
                    file = dst.split('/')[-1]
                    os.makedirs(dst.replace(file, '')) ##is the folder is not created , create it, and init method againg (recursive)
                    self.move_file(src, dst)
                except Exception as e:
                    print("Error moving file: %s" % e)


    #this method is pending to the event file , and filter the file to move later
    def on_modified(self, event: FileSystemEvent):
        print(event)
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
                new_name = filename.replace(text.group(), "_" + date_today + text.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/"+self.folder_text+"/"+ new_name
                self.move_file(src, dst)
            elif code:
                new_name = filename.replace(code.group(), "_" + date_today + code.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/"+self.folder_code+"/"+ new_name
                self.move_file(src, dst)
            elif documents:
                new_name = filename.replace(documents.group(), "_" + date_today + documents.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/"+self.folder_documents+"/"+ new_name
                self.move_file(src, dst)
            elif images:
                new_name = filename.replace(images.group(), "_" + date_today + images.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/"+self.folder_images+"/"+ new_name
                self.move_file(src, dst)
            elif videos:
                new_name = filename.replace(videos.group(), "_" + date_today + videos.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/"+self.folder_videos+"/"+ new_name
                self.move_file(src, dst)

            elif zipp:
                new_name = filename.replace(zipp.group(), "_" + date_today + zipp.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/"+self.folder_zipp+"/"+ new_name
                self.move_file(src, dst)
            elif audio:
                new_name = filename.replace(audio.group(), "_" + date_today + audio.group())
                src = self.folder_to_track +"/"+ filename
                dst = self.folder_to_track +"/"+self.folder_audio+"/"+ new_name
                self.move_file(src, dst)
            else:
                pass



def main():
    event_handler = FileHandler()
    folder_to_track = event_handler.set_config('config.json')
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()
  

if __name__ == "__main__":
    main()
