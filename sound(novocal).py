import os
import time
import simpleaudio as sa
import ast

def get_wav_files(directory):
    wav_files = {}
    for file in os.listdir(directory):
        if file.endswith(".wav"):
            note = os.path.splitext(file)[0] 
            wav_files[note.upper()] = os.path.join(directory, file)
    return wav_files

def load_array_from_file():
    with open("chorus.txt", "r") as file:
        data = file.read()
        array = ast.literal_eval(data)  
    return array

def play_notes_with_background(mr_file, wav_files, notes, interval=0.5):
    if os.path.exists(mr_file):
        mr_wave_obj = sa.WaveObject.from_wave_file(mr_file)
        mr_play_obj = mr_wave_obj.play()
    else:
        print("MR file not found.")
        return

    start_time = time.time()
    play_objects = []

    for i, note in enumerate(notes):
        if note in wav_files:
            wave_obj = sa.WaveObject.from_wave_file(wav_files[note])
            play_obj = wave_obj.play()
            play_objects.append(play_obj)
        

        next_time = start_time + (i + 1) * interval
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)


    for play_obj in play_objects:
        play_obj.wait_done()


    mr_play_obj.wait_done()

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base_path, "Music", "Guitar")
    mr_file = os.path.join(base_path, "MR", "MR.wav")
    
    wav_files = get_wav_files(directory)

    chorus_line = load_array_from_file()

    if not wav_files:
        print("No wav files found in the directory.")
    else:
        play_notes_with_background(mr_file, wav_files, chorus_line, interval=0.5)
