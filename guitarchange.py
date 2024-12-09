import os
import time
import simpleaudio as sa

# 음계 리스트
twinkle_star_notes = [
    'G#0', 'G#0', 'C#1', 'C#1', 'C1', 'C#1', 'D#1', 'D#1', 'C#1', 'D#1',
    'F1', 'F1', 'F#1', 'F1', 'A#0', 'A#0', 'D#1', 'D#1', 'C#1', 'C#1', 'C#1',
    'C#1', 'C1', 'C1', 'A#0', 'C1', 'C#1', 'C#1', 'C#1', 'C#1', 'C#1', 'C#1',
    'C#1', 'F1', 'G#1', 'G#1', 'F1', 'D#1', 'C#1', 'C#1', 'C1', 'C#1', 'D#1',
    'C#1', 'C1', 'A#0', 'G#0', 'G#0', 'C#1', 'F1', 'G#1', 'G#1', 'F1', 'D#1',
    'C#1', 'C#1', 'C1', 'C#1', 'D#1', 'D#1', 'D#1', 'D#1', 'D#1', 'D#1',
    'G#0', 'G#0', 'C#1', 'C#1', 'C#1', 'C#1', 'D#1', 'D#1', 'D#1', 'D#1',
    'F1', 'F1', 'F#1', 'F1', 'A#0', 'A#0', 'D#1', 'D#1', 'C#1', 'C#1', 'C#1',
    'C#1', 'C1', 'C1', 'A#0', 'C1', 'C#1', 'C#1', 'C#1', 'C#1', 'C#1', 'C#1'
]

def get_wav_files(directory):
    """지정된 디렉토리에서 .wav 파일 경로를 반환"""
    wav_files = {}
    for file in os.listdir(directory):
        if file.endswith(".wav"):
            note = os.path.splitext(file)[0]  # 파일 이름에서 확장자 제거
            wav_files[note.upper()] = os.path.join(directory, file)
    return wav_files

def play_notes(wav_files, notes, interval=0.5):
    """지정된 음계 리스트를 간격(interval)으로 재생"""
    play_objects = []

    for note in notes:
        if note in wav_files:
            wave_obj = sa.WaveObject.from_wave_file(wav_files[note])
            play_obj = wave_obj.play()  # 음 재생 시작
            play_objects.append(play_obj)
            time.sleep(interval)  # 간격 설정
        else:
            print(f"Note {note} not found in wav files.")

    # 모든 음이 재생 종료될 때까지 대기
    for play_obj in play_objects:
        play_obj.wait_done()

if __name__ == "__main__":
    directory = r"C:\\Users\\USER\\Desktop\\opensource\\project\\Music\\Guitar"
    wav_files = get_wav_files(directory)

    if not wav_files:
        print("No wav files found in the directory.")
    else:
        play_notes(wav_files, twinkle_star_notes, interval=0.5)
