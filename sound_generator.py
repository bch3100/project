import sys
import os
import time
import simpleaudio as sa

def get_wav_files(directory):
    """지정된 디렉토리에서 .wav 파일 경로를 반환"""
    wav_files = {}
    for file in os.listdir(directory):
        if file.endswith(".wav"):
            note = os.path.splitext(file)[0]  # 파일 이름에서 확장자 제거
            wav_files[note.upper()] = os.path.join(directory, file)
    return wav_files

def play_notes_with_background(mr_audio_file, wav_files, notes, interval=0.5):
    """
    MR 파일과 음계 배열을 동시에 재생
    - mr_audio_file: MR 파일 경로
    - wav_files: 음계 파일 경로 딕셔너리
    - notes: 재생할 음계 리스트
    - interval: 음계 간 재생 간격
    """
    # MR 재생 시작
    wave_obj = sa.WaveObject.from_wave_file(mr_audio_file)
    mr_play_obj = wave_obj.play()

    # 음계 재생
    play_objects = []
    for note in notes:
        if note in wav_files:
            wave_obj = sa.WaveObject.from_wave_file(wav_files[note])
            play_obj = wave_obj.play()
            play_objects.append(play_obj)
            time.sleep(interval)
        else:
            print(f"Note {note} not found in WAV files.")

    # 음계가 모두 끝날 때까지 대기
    for play_obj in play_objects:
        play_obj.wait_done()

    # MR 재생이 끝날 때까지 대기
    mr_play_obj.wait_done()

def main():
    # 두 번째 프로그램의 입력값 처리
    if len(sys.argv) < 3:
        print("Usage: python second_program.py <mr_audio_file> <notes_array>")
        return

    mr_audio_file = sys.argv[1]
    notes_array_string = sys.argv[2]
    notes_array = [item.strip() for item in notes_array_string.split(',')]

    # 음계 파일 디렉토리 설정 (상대 경로)
    wav_directory = os.path.join('.', 'Music', 'Guitar')
    wav_files = get_wav_files(wav_directory)

    if not wav_files:
        print("음계 파일이 존재하지 않습니다. WAV 파일을 확인해주세요.")
        return

    # MR 파일과 음계 배열을 동시에 재생
    play_notes_with_background(mr_audio_file, wav_files, notes_array)

if __name__ == "__main__":
    main()



