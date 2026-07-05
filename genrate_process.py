# this file looks for new folder inside user uploads and convert them to reel if they are not already converted
import os 
from text_to_audio import text_to_speech_file
import time
import subprocess

def text_to_audio(folder):
    print("TTA - " , folder)
    with open(f"user_upload/{folder}/desc.txt") as f :
        text = f.read()
    print( text, folder)    
    text_to_speech_file(text,folder)


def create_reel(folder):
    print ("inside create_reel")
    comand = f'''ffmpeg -y -f concat -safe 0 -i user_upload/{folder}/input.txt -i user_upload/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
     
    print(comand)
    result = subprocess.run(comand, shell=True, capture_output=True, text=True)
    print ("return code:", result.returncode)
    print("STDERR:", result.stderr)
    print("STDOUT:", result.stdout)
    print ("CR -", folder)


if __name__ == "__main__":
    while True:
        print("processing queue.....")
        with open("done.txt","r") as f :
            done_folders = f.readlines()

        done_folders = [f.strip() for f in done_folders]
        folders = os.listdir("user_upload")
        for folder in folders :
            if (folder not in done_folders):
                print("starting text_to_audio...")
                text_to_audio(folder)#genrate the audio.mp3 from desc.txt
                print("starting create_reel...")
                create_reel(folder) #contvert the images and audio.mp3 inside the folder to a reel    
                with open("done.txt","a") as f :
                    f.write(folder + "\n") 

        time.sleep(20*60)                    