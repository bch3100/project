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
    # 음계 파일 디렉토리와 MR 파일 경로
    directory = r"C:\\Users\\USER\\Desktop\\opensource\\project\\Music\\Guitar"
    mr_file = r"C:\\Users\\USER\\Desktop\\opensource\\project\\MR\\MR.wav"
    
    # 음계 파일 불러오기
    wav_files = get_wav_files(directory)

    if not wav_files:
        print("No wav files found in the directory.")
    else:
        # MR과 음계를 동시에 재생
        play_notes_with_background(mr_file, wav_files, twinkle_star_notes, interval=0.5)
