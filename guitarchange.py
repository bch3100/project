import os
import numpy as np
import librosa
import soundfile as sf

def apply_fade(audio, fade_in_samples, fade_out_samples):
    """
    Apply fade-in and fade-out effects to the given audio.

    Parameters:
        audio (numpy.ndarray): The audio data.
        fade_in_samples (int): Number of samples for fade-in.
        fade_out_samples (int): Number of samples for fade-out.

    Returns:
        numpy.ndarray: Audio with fade-in and fade-out applied.
    """
    fade_in = np.linspace(0, 1, fade_in_samples)
    fade_out = np.linspace(1, 0, fade_out_samples)

    audio[:fade_in_samples] *= fade_in
    audio[-fade_out_samples:] *= fade_out

    return audio

def create_audio_from_notes(note_array, audio_dir, output_path=None, overlap_duration=0.15):
    """
    주어진 노트 배열을 사용해 지정된 디렉토리의 .wav 파일을 결합하여 음성이 겹치도록 생성.

    Parameters:
        note_array (list of str): 사용할 음계 이름 배열
        audio_dir (str): .wav 파일이 저장된 디렉토리 경로
        output_path (str): 생성할 오디오 파일 경로
        overlap_duration (float): 다음 음이 시작되는 지연 시간 (초)
    """
    if output_path is None:
        output_path = os.path.join(r"C:\Users\USER\Desktop\opensource\project\Music", "overlapped_audio.wav")

    sr = 22050  # 기본 샘플링 레이트 설정
    combined_audio = np.zeros(0)  # 초기화된 오디오 배열

    for note in note_array:
        file_path = os.path.join(audio_dir, f"{note}.wav")

        if os.path.exists(file_path):
            # 오디오 파일 읽기
            audio, file_sr = librosa.load(file_path, sr=sr)

            # Adjust the length of the audio to account for overlap
            target_length = int(sr * (1.0 - overlap_duration))
            if len(audio) > target_length:
                audio = audio[:target_length]
        else:
            print(f"Warning: 파일 {file_path}를 찾을 수 없습니다. 무음으로 대체합니다.")
            audio = np.zeros(int(sr * (1.0 - overlap_duration)))  # 누락된 경우 조정된 무음 생성

        # Calculate overlap length
        overlap_samples = int(sr * overlap_duration)

        if len(combined_audio) < overlap_samples:
            combined_audio = np.concatenate((combined_audio, audio))
        else:
            # Mix overlapping part
            combined_audio[-overlap_samples:] += audio[:overlap_samples]
            # Append the remaining part of the new audio
            combined_audio = np.concatenate((combined_audio, audio[overlap_samples:]))

    # 오디오 데이터를 파일로 저장
    sf.write(output_path, combined_audio, sr)
    print(f"오디오 파일이 다음 위치에 저장되었습니다: {output_path}")

# 음계 배열 입력
note_array = [
    'G#0', 'G#0', 'C#1', 'C#1', 'C1', 'C#1', 'D#1', 'D#1', 'C#1', 'D#1','F1', 'F1', 'F#1', 'F1', 'A#0', 'A#0', 'D#1', 'D#1', 'C#1', 'C#1', 'C#1', 'C#1', 'C1', 'C1', 'A#0', 'C1', 'C#1', 'C#1', 'C#1', 'C#1', 'C#1', 'C#1', 'C#1', 'F1', 'G#1', 'G#1', 'F1', 'D#1', 'C#1', 'C#1', 'C1', 'C#1', 'D#1', 'C#1', 'C1', 'A#0', 'G#0', 'G#0','C#1', 'F1', 'G#1', 'G#1', 'F1', 'D#1', 'C#1', 'C#1', 'C1', 'C#1', 'D#1', 'D#1', 'D#1', 'D#1', 'D#1', 'D#1','G#0', 'G#0', 'C#1', 'C#1', 'C#1', 'C#1', 'D#1', 'D#1', 'D#1', 'D#1', 'F1', 'F1', 'F#1', 'F1', 'A#0', 'A#0', 'D#1', 'D#1', 'C#1', 'C#1', 'C#1', 'C#1', 'C1', 'C1', 'A#0', 'C1', 'C#1', 'C#1', 'C#1', 'C#1', 'C#1', 'C#1'
]
audio_dir = r"C:\Users\USER\Desktop\opensource\project\Music\Guitar(TEMPO 60)"

# 오디오 파일 생성
create_audio_from_notes(note_array, audio_dir, overlap_duration=0.15)
