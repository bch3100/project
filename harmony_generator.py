import librosa as lb
import numpy as np

#MRStructure 의 bar는 코드 정보를 포함하는 2차원 배열
#VocalStructure 의 line은 멜로디 정보를 포함하는 1차원 배열

#모든 출력값들은 행은 마디, 열은 일단 한 박자 단위로 출력한다.

class MRStructure:
    def __init__(self, MR_file = None, time_sig = None, key_sig = None, bpm = None, MR_slice = 4, bars = None):
        self.y, self.sr = lb.load(MR_file) if MR_file is not None else (None, None)
        self.time_signature = self.set_time_signature(time_sig)
        self.key_signature = self.set_key_signature(key_sig)
        self.tempo = self.set_tempo(bpm)
        self.MRslice = MR_slice
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

    def set_bar(self, bars):
        if bars is not None:
            self.bar = bars
            return self.bar
        else:
            beat_duration = 60.0 / self.tempo
            beat_count, beat_value = map(int, self.time_signature.split('/'))
            bar_duration = (beat_count / beat_value * 4) * beat_duration
            sample_per_bar = int(bar_duration * self.sr)
            sample_per_slice = int(sample_per_bar / (beat_count / beat_value * self.MRslice))

            bar_count = (len(self.y) // sample_per_bar) + 2
            bar_slices= int(float(beat_count / beat_value) * self.MRslice)
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
                # chroma = lb.feature.chroma_cqt(y=self.y[start_sample:], sr=self.sr)
                # chroma_sum = np.sum(np.nan_to_num(chroma), axis=1)
                # bars[i][j] = chord_detector(chroma_sum)
                bars[i][j] = None

            self.bar = bars
            return self.bar
        
    def MR_transpose(self, key):
        index = None
        for i in range(len(pitch_table)):
            if self.key_signature == pitch_table[i]:
                index = i
                break
        self.key_signature = pitch_table[(index+key) % len(pitch_table)]

        for i in range(len(self.bar)):
            for j in range(len(self.bar[i])):
                chord = self.bar[i][j]
                if chord is None:
                    continue
                else:
                    for k in range(len(chord_list)):
                        if chord == chord_list[k]:
                            self.bar[i][j] = chord_list[(k + key * 5) % len(chord_list)]

    def moreslice(self, slices):
        if slices <= 1:
            return
        
        bar_count = len(self.bar)
        new_bar = []

        for i in range(bar_count):
            new_slices = []
            for j in range(len(self.bar[i])):
                new_slices.extend([self.bar[i][j]] * slices)
            new_bar.append(new_slices)
        
        return new_bar
    

def MR_sampling(bar, start, count, slices):
    sample = []
    i = start[0]
    j = start[1]
    while len(sample) < count:
        sample.append(bar[i][j])
        i += (j + 1) // slices
        j = (j + 1) % slices
    return sample

def chord_detector(chroma_sum):
    best_chord = None
    best_similarity = 0

    for chord, pitch_class in chroma_chord_table.items():

        similarity = np.dot(chroma_sum, pitch_class)


        if similarity > best_similarity:
            best_similarity = similarity
            best_chord = chord
    
    return best_chord


#====================================================================#


class VocalStructure:
    def __init__(self, Vocal_file = None, time_sig = None, key_sig = None, bpm = None, Vocal_slice = 4, line = None):
        self.y, self.sr = lb.load(Vocal_file) if Vocal_file is not None else (None, None)
        self.time_signature = self.set_time_signature(time_sig)
        self.key_signature = self.set_key_signature(key_sig)
        self.tempo = self.set_tempo(bpm)
        self.Vocalslice = Vocal_slice
        self.line = self.set_line(line)
        
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

    def set_line(self, line):
        if line is not None:
            self.line = line
            return self.line
        
        beat_duration = 60.0 / self.tempo
        sample_per_slice = int(beat_duration * self.sr / self.Vocalslice)

        slices_count = (len(self.y) // sample_per_slice + 1)
        notes = [None] * slices_count

        trimmed_audio, index = lb.effects.trim(self.y, top_db=20)
        start_sample = index[0]
        i = 0
        
        while start_sample + sample_per_slice <= len(self.y): 
            end_sample = start_sample + sample_per_slice
            chroma = lb.feature.chroma_cqt(y=self.y[start_sample:end_sample], sr=self.sr)
            chroma_sum = np.sum(np.nan_to_num(chroma), axis=1)
            notes[i] = pitch_detector(chroma_sum, self.y[start_sample:end_sample], sr=self.sr)
            start_sample = end_sample
            i += 1

        if start_sample < len(self.y):
            # chroma = lb.feature.chroma_cqt(y=y[start_sample:], sr=self.sr)
            # chroma_sum = np.sum(np.nan_to_num(chroma), axis=1)
            # notes[i] = pitch_detector(chroma_sum, self.y[start_sample:], sr=self.sr)
            notes[i] = None

        return notes

    def pitch_transpose(self, key):
        index = None
        for i in range(len(pitch_table)):
            if self.key_signature == pitch_table[i]:
                index = i
                break
        self.key_signature = pitch_table[(index+key) % len(pitch_table)]

        if key == 0:
            return self.line
        
        for i in range(len(self.line)):
            if self.line[i] is None: 
                    continue
            else:
                note = self.line[i]
                pitch = note[:-1]
                octave= int(note[-1])
                for j in range(len(pitch_table)):
                    if pitch == pitch_table[j]:
                        new_pitch = pitch_table[(j + key) % len(pitch_table)]
                        new_octave = octave + (j + key) // len(pitch_table)
                        break
                self.line[i] = f"{new_pitch}{new_octave}"

        return self.line     

    def octave_transpose(self, key):
        if key == 0:
            return self.line
        
        for i in range(len(self.line)):
            if self.line[i] is None: 
                    continue
            else:
                note = self.line[i]
                pitch = note[:-1]
                octave = int(note[-1]) + key
                self.line[i] = f"{pitch}{octave}"

        return self.line


    def chorus_generator(self, sampled_MR):
        n = len(self.line)
        chorus = [None] * n

        for i in range(n):
            if sampled_MR[i] == None or self.line[i] == None:
                continue
            
            else:
                chord = sampled_MR[i]
                m = len(chord_scale_table[chord])

                note = self.line[i]
                pitch = note[:-1]
                octave= int(note[-1])
                
                index = 0
                new_pitch = chord_scale_table[chord][index]
                new_octave = octave

                for j in range(m):
                    if  -2 < pitch_table.index(pitch) - pitch_table.index(new_pitch) < 2:
                        new_pitch = chord_scale_table[chord][index + j]

                if pitch_table.index(pitch) < pitch_table.index(new_pitch) :
                    new_octave -= 1

            chorus[i] = f"{new_pitch}{new_octave}"
        return chorus

def pitch_detector(chroma_sum, y, sr):
    index = np.argmax(chroma_sum)
    pitch = pitch_table[index]

    spectral_centroids = lb.feature.spectral_centroid(y=y, sr=sr)
    
    if spectral_centroids.size > 0 and np.isfinite(spectral_centroids).all():
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


#====================================================================#


def transpose(MR, Vocal, key):
    MR.MR_transpose(key)
    Vocal.Vocal_transpose(key)


def Synchronize(MR, Vocal, start):
    bars = MR.moreslice(int(Vocal.Vocalslice * 4 / MR.MRslice))
    sampled_bar = MR_sampling(bars, start, len(Vocal.line), Vocal.Vocalslice * 4)

    return sampled_bar
    

#====================================================================#


pitch_table = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

chord_list = ['C', 'Cm', 'Caug', 'Cdim', 'Csus4'
              'C#', 'C#m', 'C#aug', 'C#dim', 'C#sus4',
              'D', 'Dm', 'Daug', 'Ddim', 'Dsus4', 
              'D#', 'D#m', 'D#aug', 'D#dim', 'D#sus4', 
              'E', 'Em', 'Eaug', 'Edim', 'Esus4', 
              'F', 'Fm', 'Faug', 'Fdim', 'Fsus4', 
              'F#', 'F#m', 'F#aug', 'F#dim', 'F#sus4', 
              'G', 'Gm', 'Gaug', 'Gdim', 'Gsus4', 
              'G#', 'G#m', 'G#aug', 'G#dim', 'G#sus4', 
              'A', 'Am', 'Aaug', 'Adim', 'Asus4', 
              'A#', 'A#m', 'A#aug', 'A#dim', 'A#sus4', 
              'B', 'Bm', 'Baug', 'Bdim', 'Bsus4']
    
chord_scale_table = {
    'C':     ['C', 'E', 'G'], 
    'Cm':    ['C', 'D#', 'G'],
    'Caug':  ['C', 'E', 'G#'],
    'Cdim':  ['C', 'D#', 'F#'],
    'Csus4': ['C', 'F', 'G'],
    #
    'C#':    ['C#', 'F', 'G#'],
    'C#m':   ['C#', 'E', 'G#'],
    'C#aug': ['C#', 'F', 'A'],
    'C#dim': ['C#', 'E', 'G'],
    'C#sus4':['C#', 'F#', 'G#'],
    #
    'D':     ['D', 'F#', 'A'],
    'Dm':    ['D', 'F', 'A'],
    'Daug':  ['D', 'F#', 'A#'],
    'Ddim':  ['D', 'F', 'G#'],
    'Dsus4': ['D', 'G', 'A'],
    #
    'D#':    ['D#', 'G', 'A#'],
    'D#m':   ['D#', 'F#', 'A#'],
    'D#aug': ['D#', 'G', 'B'],
    'D#dim': ['D#', 'F#', 'A'],
    'D#sus4':['D#', 'G#', 'A#'],
    #
    'E':     ['E', 'G#', 'B'],
    'Em':    ['E', 'G', 'B'],
    'Eaug':  ['E', 'G#', 'C'],
    'Edim':  ['E', 'G', 'A#'],
    'Esus4': ['E', 'A', 'B'],
    #
    'F':     ['F', 'A', 'C'],
    'Fm':    ['F', 'G#', 'C'],
    'Faug':  ['F', 'A', 'C#'],
    'Fdim':  ['F', 'G#', 'B'],
    'Fsus4': ['F', 'A#', 'C'],
    #
    'F#':    ['F#', 'A#', 'C#'],
    'F#m':   ['F#', 'A', 'C#'],
    'F#aug': ['F#', 'A#', 'D'],
    'F#dim': ['F#', 'A', 'C'],
    'F#sus4':['F#', 'B', 'C#'],
    #
    'G':     ['G', 'B', 'D'],
    'Gm':    ['G', 'A#', 'D'],
    'Gaug':  ['G', 'B', 'D#'],
    'Gdim':  ['G', 'A#', 'C'],
    'Gsus4': ['G', 'C', 'D'],
    #
    'G#':    ['G#', 'C', 'D#'],
    'G#m':   ['G#', 'B', 'D#'],
    'G#aug': ['G#', 'E', 'G#'],
    'G#dim': ['G#', 'B', 'D'],
    'G#sus4':['G#', 'C#', 'D#'],
    #
    'A':     ['A', 'C#', 'E'],
    'Am':    ['A', 'C', 'E'],
    'Aaug':  ['A', 'C#', 'E#'],
    'Adim':  ['A', 'C', 'E'],
    'Asus4': ['A', 'D', 'E'],
    #
    'A#':    ['A#', 'D', 'F'],
    'A#m':   ['A#', 'C#', 'F'],
    'A#aug': ['A#', 'D', 'F#'],
    'A#dim': ['A#', 'C#', 'E'],
    'A#sus4':['A#', 'D#', 'F'],
    #
    'B':     ['B', 'D#', 'F#'],
    'Bm':    ['B', 'D', 'F#'],
    'Baug':  ['B', 'D#', 'G'],
    'Bdim':  ['B', 'D', 'F'],
    'Bsus4': ['B', 'E', 'F#'],
}

chroma_chord_table = {
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


#====================================================================#


#예시) 임의로 설정할 수도 있다

# time_signature = '4/4'
# key_signature = 'C'
#tempo = 120 #BPM

#MRStructure bar : 첫 행과 마지막 행은 비워둠. 파일로 생성해도 마지막 행을 제외하고 비슷한 형식으로 만들어짐
# MR_bars = [[None, None, None, None],
#         ['C', 'D', 'E', 'F'],
#         ['G', 'A', 'B', 'C'],
#         [None, None, None, None]]

# test_MR = MRStructure(time_sig=time_signature, key_sig=key_signature, bpm=tempo, MR_slice=2, bars=MR_bars)

#VocalStructure bar : 1차원 배열
# Vocal_line = ['C1', 'D1', 'E1', 'F1', 'G1', 'A1', 'B1', 'C2']

# test_Vocal = VocalStructure(time_sig=time_signature, key_sig=key_signature, bpm=tempo, Vocal_slice=2, line=Vocal_line)

#파일로부터 생성하는 법

#MR_path = 'MR_path.mp3'
#test = MRStructure(MR_path, time_sig=time_signature, key_sig=key_signature) 최소한 time_signature과 key_signature는 직접 입력

# Vocal_path = 'Vocal_path.mp3'
# test_Vocal = VocalStructure(Vocal_file=Vocal_path, time_sig=time_signature, key_sig=key_signature) #최소한 time_signature과 key_signature는 직접 입력
