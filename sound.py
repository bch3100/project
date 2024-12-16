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

def load_array_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = file.read()
            return ast.literal_eval(data)  
    else:
        print(f"Array file not found: {file_path}")
        return []

def play_notes_with_background(mr_file, wav_files, notes, additional_wav_files, additional_notes, interval=0.5):
    if os.path.exists(mr_file):
        try:
            mr_wave_obj = sa.WaveObject.from_wave_file(mr_file)
            mr_play_obj = mr_wave_obj.play()
        except Exception as e:
            print(f"Error playing MR file: {e}")
            return
    else:
        print("MR file not found.")
        return

    start_time = time.time()
    play_objects = []

    max_length = max(len(notes), len(additional_notes))  

    for i in range(max_length):
        if i < len(notes) and notes[i] in wav_files:
            try:
                wave_obj = sa.WaveObject.from_wave_file(wav_files[notes[i]])
                play_obj = wave_obj.play()
                play_objects.append(play_obj)
            except Exception as e:
                print(f"Error playing note {notes[i]}: {e}")

        if i < len(additional_notes) and additional_notes[i] in additional_wav_files:
            try:
                wave_obj = sa.WaveObject.from_wave_file(additional_wav_files[additional_notes[i]])
                play_obj = wave_obj.play()
                play_objects.append(play_obj)
            except Exception as e:
                print(f"Error playing additional note {additional_notes[i]}: {e}")
        elif i < len(additional_notes):
            print(f"Additional note {additional_notes[i]} not found in additional wav files.")

        next_time = start_time + (i + 1) * interval
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            print(f"Skipping sleep as sleep_time={sleep_time:.3f}")

    for play_obj in play_objects:
        try:
            play_obj.wait_done()
        except Exception as e:
            print(f"Error waiting for play object: {e}")

    try:
        mr_play_obj.wait_done()
    except Exception as e:
        print(f"Error waiting for MR play object: {e}")

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    main_directory = os.path.join(base_path, "Music", "Guitar")
    additional_directory = os.path.join(base_path, "VocalGuitar")  
    mr_file = os.path.join(base_path, "MR", "MR.wav")
    
    
    chorus_line = load_array_from_file("chorus.txt")
    additional_notes = load_array_from_file(os.path.join(additional_directory, "vocal_line.txt"))


    wav_files = get_wav_files(main_directory)

    
    additional_wav_files = get_wav_files(additional_directory)

    if not wav_files:
        print("No wav files found in the main directory.")
    elif not additional_wav_files:
        print("No wav files found in the additional directory.")
    else:
        play_notes_with_background(mr_file, wav_files, chorus_line, additional_wav_files, additional_notes, interval=0.5)
