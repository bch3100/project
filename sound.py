import os
import time
import simpleaudio as sa
import ast

def get_wav_files(directory):
    """지정된 디렉토리에서 .wav 파일 경로를 반환"""
    wav_files = {}
    for file in os.listdir(directory):
        if file.endswith(".wav"):
            note = os.path.splitext(file)[0]  # 파일 이름에서 확장자 제거
            wav_files[note.upper()] = os.path.join(directory, file)
    return wav_files

def load_array_from_file():
    # 텍스트 파일에서 배열 읽기
    with open("chorus.txt", "r") as file:
        data = file.read()
        array = ast.literal_eval(data)  
    return array

def play_notes_with_background(mr_file, wav_files, notes, interval=0.465):
    """MR 파일과 음계 리스트를 동시에 재생"""
    # MR 파일 재생 시작
    if os.path.exists(mr_file):
        mr_wave_obj = sa.WaveObject.from_wave_file(mr_file)
        mr_play_obj = mr_wave_obj.play()
    else:
        print("MR file not found.")
        return

    # 음계 재생
    start_time = time.time()
    play_objects = []

    for i, note in enumerate(notes):
        if note in wav_files:
            wave_obj = sa.WaveObject.from_wave_file(wav_files[note])
            play_obj = wave_obj.play()
            play_objects.append(play_obj)
        else:
            print(f"Note {note} not found in wav files.")
        
        # 다음 음표 재생 간격 유지
        next_time = start_time + (i + 1) * interval
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

    # 모든 음계가 재생 종료될 때까지 대기
    for play_obj in play_objects:
        play_obj.wait_done()

    # MR 재생이 끝날 때까지 대기
    mr_play_obj.wait_done()

if __name__ == "__main__":
    # 현재 스크립트 경로 기준으로 디렉토리 설정
    base_path = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base_path, "Music", "Guitar")
    mr_file = os.path.join(base_path, "MR", "MR.wav")
    
    # 음계 파일 불러오기
    wav_files = get_wav_files(directory)

    chorus_line = load_array_from_file()

    if not wav_files:
        print("No wav files found in the directory.")
    else:
        # MR과 음계를 동시에 재생
        play_notes_with_background(mr_file, wav_files, chorus_line, interval=0.5)
