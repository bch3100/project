import librosa as lb
import numpy as np

#MRStructure 의 bar는 코드 정보를 포함하는 2차원 배열
#single_tnoe_detector 의 리턴값은 멜로디 정보를 포함하는 2차원 배열
#pronunciation_insert 의 리턴값은 멜로디와 발음 정보를 포함하는 3차원 배열

#모든 출력값들은 행은 마디, 열은 일단 한 박자 단위로 출력한다.

class MRStructure:
    def __init__(self, MR_file = None, time_sig = None, key_sig = None, bpm = None, length = None, bars = None):
        self.y, self.sr = lb.load(MR_file)
        self.time_signature = self.set_time_signature(time_sig)
        self.key_signature = self.set_key_signature(key_sig)
        self.tempo = self.set_tempo(bpm)
        self.duration = self.set_duration(length)
        self.bar = self.set_bar(bars)
        
    def set_time_signature(self, Ts = None):
        if Ts is not None:
            self.time_signature = Ts
            return self.time_signature
        else: 
            self.time_signature = '4/4'
            return self.time_signature
    
    def set_key_signature(self, Ks=None):
        if Ks is not None:
            self.key_signature = Ks
            return self.key_signature
        else: 
            self.key_signature = 'C'
            return self.key_signature
    
    def set_tempo(self, Tp = None):
        if Tp is not None:
            self.tempo = Tp
            return self.tempo
        else:
            extracted_tempo, _ = lb.beat.beat_track(y=self.y, sr=self.sr)
            self.tempo = round(float(extracted_tempo[0]))
            return self.tempo

    def set_duration(self, length = None):
        if length is not None:
            self.duration = length
            return self.duration
        else:
            self.duration = lb.get_duration(y=self.y, sr=self.sr)
            return self.duration

    def set_bar(self, bars = None, slices=4):
        if bars is not None:
            self.bar = bars
            return self.bar
        else:
            beat_duration = 60.0 / self.tempo
            beat_count, beat_value = map(int, self.time_signature.split('/'))
            bar_duration = (beat_count / beat_value * 4) * beat_duration
            sample_per_bar = int(bar_duration * self.sr)
            sample_per_slice = int(sample_per_bar / (beat_count / beat_value * slices))

            bar_count = (len(self.y) // sample_per_bar) + 2
            bar_slices= int(float(beat_count / beat_value) * slices)
            bars = np.full((bar_count, bar_slices), None)

            trimmed_audio, index = lb.effects.trim(self.y, top_db=20)
            start_sample = index[0]
            i = 1

            while start_sample + sample_per_bar <= len(self.y): 
                for j in range(bar_slices):
                    end_sample = start_sample + sample_per_slice
                    chroma = lb.feature.chroma_cqt(y=self.y[start_sample:end_sample], sr=self.sr)
                    chroma_sum = np.sum(np.nan_to_num(chroma), axis=1)
                    bars[i][j] = chord_detector(chroma_sum)
                    start_sample = end_sample
                i += 1
            
            remain_sample = len(self.y) - start_sample
            remain_slice = remain_sample // sample_per_slice
            j = 0

            for j in range(remain_slice):
                end_sample = start_sample + sample_per_slice
                chroma = lb.feature.chroma_cqt(y=self.y[start_sample:end_sample], sr=self.sr)
                chroma_sum = np.sum(np.nan_to_num(chroma), axis=1)
                bars[i][j] = chord_detector(chroma_sum)
                start_sample = end_sample

            if start_sample < len(self.y):
                chroma = lb.feature.chroma_cqt(y=self.y[start_sample:], sr=self.sr)
                chroma_sum = np.sum(np.nan_to_num(chroma), axis=1)
                bars[i][j] = chord_detector(chroma_sum)
                #bars[i][j] = None

            self.bar = bars
            return self.bar

def chord_detector(chroma_sum):
    best_chord = None
    best_similarity = 0

    for chord, pitch_class in chord_table.items():

        similarity = np.dot(chroma_sum, pitch_class)


        if similarity > best_similarity:
            best_similarity = similarity
            best_chord = chord
    
    return best_chord



def single_tone_detector(file_path, time_signature, key_signature, tempo):
    y, sr = lb.load(file_path)
    slices = 4

    beat_duration = 60.0 / tempo
    beat_count, beat_value = map(int, time_signature.split('/'))
    bar_duration = (beat_count / beat_value * 4) * beat_duration
    sample_per_bar = int(bar_duration * sr)
    sample_per_slice = int(sample_per_bar / (beat_count / beat_value * slices))

    bar_count = (len(y) // sample_per_bar) + 1
    bar_slices= int(float(beat_count / beat_value) * slices)
    bars = np.full((bar_count, bar_slices), None)

    trimmed_audio, index = lb.effects.trim(y, top_db=20)
    start_sample = index[0]
    i = 0

    while start_sample + sample_per_bar <= len(y): 
        for j in range(bar_slices):
                end_sample = start_sample + sample_per_slice
                chroma = lb.feature.chroma_cqt(y=y[start_sample:end_sample], sr=sr)
                chroma_sum = np.sum(np.nan_to_num(chroma), axis=1)
                bars[i][j] = pitch_detector(chroma_sum, y[start_sample:end_sample], sr=sr)
                start_sample = end_sample
        i += 1
            
        remain_sample = len(y) - start_sample
        remain_slice = remain_sample // sample_per_slice
        j = 0

        for j in range(remain_slice):
            end_sample = start_sample + sample_per_slice
            chroma = lb.feature.chroma_cqt(y=y[start_sample:end_sample], sr=sr)
            chroma_sum = np.sum(np.nan_to_num(chroma), axis=1)
            bars[i][j] = pitch_detector(chroma_sum, y[start_sample:end_sample], sr=sr)
            start_sample = end_sample

        if start_sample < len(y):
            chroma = lb.feature.chroma_cqt(y=y[start_sample:], sr=sr)
            chroma_sum = np.sum(np.nan_to_num(chroma), axis=1)
            bars[i][j] = pitch_detector(chroma_sum, y[start_sample:end_sample], sr=sr)
            #bars[i][j] = None

    return  bars

def pitch_detector(chroma_sum, y, sr):
    index = np.argmax(chroma_sum)
    pitch = pitch_table[index]

    spectral_centroids = lb.feature.spectral_centroid(y=y, sr=sr)
    
    if spectral_centroids.size > 0 and np.isfinite(spectral_centroids).all():  # Centroid 값 확인
        f0 = np.mean(spectral_centroids)
    else:
        f0 = None

    if f0 and f0 > 0:
        try:
            octave = int(np.log2(f0 / 440.0))
        except (ValueError, OverflowError):
            octave = "Unknown"
    else:
        octave = "Unknown"
    return f"{pitch}{octave}"

def pronunciation_insert(vocal_line):
    bars = []

    for bar in vocal_line:
        notes = []
        for note in bar:
            if note is not None:
                notes.append([note, '아'])
            else :
                notes.append([None, None])
        bars.append(notes)

    return bars

chord_table = {
    'n.c'   : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #
    'C'     : [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    'Cm'    : [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    'Caug'  : [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'Cdim'  : [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    'Csus4' : [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    #
    'C#'    : [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    'C#m'   : [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'C#aug' : [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    'C#dim' : [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    'C#sus4': [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    #
    'D'     : [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    'Dm'    : [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    'Daug'  : [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    'Ddim'  : [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    'Dsus4' : [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    #
    'D#'    : [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    'D#m'   : [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    'D#aug' : [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    'D#dim' : [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    'D#sus4': [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    #
    'E'     : [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    'Em'    : [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'Eaug'  : [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'Edim'  : [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'Esus4' : [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    #
    'F'     : [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    'Fm'    : [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    'Faug'  : [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    'Fdim'  : [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    'Fsus4' : [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    #
    'F#'    : [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    'F#m'   : [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    'F#aug' : [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    'F#dim' : [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    'F#sus4': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    #
    'G'     : [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    'Gm'    : [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    'Gaug'  : [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    'Gdim'  : [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    'Gsus4' : [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #
    'G#'    : [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    'G#m'   : [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    'G#aug' : [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'G#dim' : [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    'G#sus4': [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    #
    'A'     : [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    'Am'    : [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    'Aaug'  : [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    'Adim'  : [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    'Asus4' : [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    #
    'A#'    : [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    'A#m'   : [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    'A#aug' : [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    'A#dim' : [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    'A#sus4': [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    #
    'B'     : [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    'Bm'    : [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    'Baug'  : [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    'Bdim'  : [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    'Bsus4' : [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
}

pitch_table = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']




#예시) 임의로 설정할 수도 있다

time_signature = '4/4'
key_signature = 'C'
tempo = 120 #BPM
length = 60 #초단위

#MR_structure bar. 첫 행과 마지막 행은 비워둠. 파일로 생성해도 마지막 행을 제외하고 비슷한 형식으로 만들어짐
MR_bars = [[None, None, None, None],
        ['C', 'D', 'E', 'F'],
        ['G', 'A', 'B', 'C'],
        [None, None, None, None]]

#위의 다차원 배열과 정보들로 인스턴스 생성
test_MR = MRStructure(time_sig=time_signature, key_sig=key_signature, bpm=tempo, length=length, bars=MR_bars)

#single_tnoe_detector. MR_structure과 다르게 첫 행은 비워두지 않음
Vocal_line = [['C1', 'D1', 'E1', 'F1'],
              ['G1', 'A1', 'B1', 'C2'], 
              [None, None, None, None]]

#pronunciation_insert. single_tone_detector에 발음만 추가
Vocal_with_pronounce = [[['C1', '아'], ['D1', '아'], ['E1', '아'], ['F1', '아']],
                        [['G1', '아'], ['A1', '아'], ['B1', '아'], ['C2', '아']],
                        [[None, None], [None, None], [None, None], [None, None]]]


#파일로부터 생성하는 법

#MR_path = 'MR_path.mp3'
#test = MRStructure(MR_path, time_sig=time_signature, key_sig=key_signature) 단, 최소한 time_signature과 key_signature는 직접 입력


#Vocal_path = 'Vocal_path.mp3'
#test_Vocal = single_tone_detector(Vocal_path, test.time_signature, test.key_signature, test.tempo) 파일과 MR 정보로 생성


#test_Vocal_with_pronounce = pronunciation_insert(test_Vocal)