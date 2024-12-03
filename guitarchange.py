import numpy as np
import librosa
import soundfile as sf
import random

# 음계 주파수 매핑 (예: C4, D4 등 음계에 해당하는 주파수 정의)
note_frequencies = {
    'C1': 32.70, 'D1': 36.71, 'E1': 41.20, 'F1': 43.65, 'G1': 49.00, 'A1': 55.00, 'B1': 61.74,
    'C2': 65.41, 'D2': 73.42, 'E2': 82.41, 'F2': 87.31, 'G2': 98.00, 'A2': 110.00, 'B2': 123.47,
    # 추가적인 음계 정의 가능
}

# 음계에 맞는 사인파 오디오 생성 함수
def generate_tone(frequency, duration, sr=22050):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    return tone

# 문자열에 맞는 오디오 파일 생성 및 결합
def create_audio_from_string(note_string, output_path="output.wav"):
    sr = 22050  # 샘플링 레이트
    note_duration = 0.5  # 4/4박자 기준 한 음의 길이 (0.5초, 4분음표)
    overlap_duration = 0.2  # 겹치는 부분의 길이 (초)
    combined_audio = np.array([])  # 결합된 오디오 데이터를 저장할 배열

    for note in note_string:
        if note in note_frequencies:
            frequency = note_frequencies[note]
            tone = generate_tone(frequency, duration=note_duration, sr=sr)  # 각 음계에 대해 0.5초짜리 톤 생성
            if len(combined_audio) == 0:
                combined_audio = tone
            else:
                overlap_length = int(sr * overlap_duration)
                combined_audio[-overlap_length:] += tone[:overlap_length]  # 겹치는 부분 결합
                combined_audio = np.concatenate((combined_audio, tone[overlap_length:]))  # 나머지 부분 결합
        else:
            print(f"음계 {note}를 찾을 수 없습니다. 스킵합니다.")

    # 결합된 오디오를 파일로 저장
    sf.write(output_path, combined_audio, sr)
    print(f"오디오 파일이 다음 위치에 저장되었습니다: {output_path}")

# 랜덤하게 20마디 생성
notes = list(note_frequencies.keys())
note_string = [random.choice(notes) for _ in range(4 * 20)]  # 각 마디에 4개의 음계, 총 20마디

# 오디오 파일 생성
create_audio_from_string(note_string, output_path="note_sequence_20_measures.wav")

