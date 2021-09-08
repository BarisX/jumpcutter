from moviepy.editor import VideoFileClip
import sys
import os 
from shutil import rmtree
from collections import deque

TEMP_FOLDER = "TEMP"

divide_number = int(sys.argv[1])

def extending_string(string: str, number: int) -> str:
    s_deque = deque(string)
    counter = 0
    while len(s_deque) != number and len(s_deque) < number+1:
        if counter == 0:
            s_deque.extend(" ")
            counter = counter + 1
        elif counter == 1:
            s_deque.extendleft(" ")
            counter = counter + 1
        else:
            if len(s_deque) % 2 == 0:
                s_deque.extend("#")
            s_deque.extendleft("#")
    return_string  = "".join(s_deque)
    return return_string+"#" if len(return_string) < number+1 else return_string

def clean_log(string:str, number: int) -> str:
    if len(string) > number:
        string_as_list = string.split(" ")
        return_string = ""
        for batch_string in string_as_list:
            return_string = return_string + extending_string(batch_string, number)
            return_string = return_string + "\n"
        return return_string
    else:
        return extending_string(string, number)

def log_print(log_string:str) -> None:
    print("<^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^>")
    print("###################################################")
    print("################## PRETTY LOGGER ##################")
    print(clean_log(log_string, 50))
    print("###################################################")
    print("###################################################")
    print("<_________________________________________________>")

def div(file, original_video, duration, batch_size, i):
    temp_batch = duration - batch_size
    batch = duration - temp_batch
    duration = duration if (duration - batch) > 0 else 0
    if batch*(i+1) > duration:
        clip = original_video.subclip(batch*i, original_video.duration)
    else:
        clip = original_video.subclip(batch*i, batch*(i+1))
    output_filename = file[:-4]+str(i+1)+".mp4"
    clip.to_videofile(output_filename, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
    log_print("The "+output_filename+" created.")
    if not "ALTERED" in file:
        os.system("python jumpcutter.py --input_file "+output_filename+" --output_file "+output_filename+"_ALTERED"+" --silent_speed 999999 --frame_rate 60 --frame_quality 1 --silent_threshold 0.008")
        log_print("The "+output_filename+" jumcutted in loop.")


def get_all_mp4():        
        lt = []
        for l in os.listdir():
            if 'mp4' in l:    
                lt.append(l)  
        return lt

def deletePath(s): # Dangerous! Watch out!
    try:  
        rmtree(s, ignore_errors=False)
    except OSError:  
        print ("Deletion of the directory %s failed" % s)
        print(OSError)

if os.path.isdir(TEMP_FOLDER):
    deletePath(TEMP_FOLDER)
    log_str = "The folder "+TEMP_FOLDER+" deleted."
    log_print(log_str)
else:
    log_str = "The folder "+TEMP_FOLDER+" was not here."
    log_print(log_str)
for file in get_all_mp4():
    if os.path.isfile(file[:-4]+"_ALTERED.mp4"):
        continue
    with VideoFileClip(file) as original_video:
        duration = original_video.duration
        if duration > 300:
            while duration/divide_number > 300:
                divide_number = divide_number + 1
            batch_size = duration/divide_number
            
            for i in range(0, divide_number):
                div(file, original_video, duration, batch_size, i)
                
        elif duration < 300:
            if not "ALTERED" in file:
                os.system("python jumpcutter.py --input_file "+file+" --silent_speed 999999 --frame_quality 1 --frame_rate 60 --silent_threshold 0.008")
                log_print("The "+file+" jumpcutted.")