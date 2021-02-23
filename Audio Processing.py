## Mocking Bot - Task 2 : Instrument Classification
#  Instructions
#  ------------
#
#  This file contains Main function and Instrument_identify function. Main Function helps you to check your output
#  for practice audio files provided. Do not make any changes in the Main Function.
#  You have to complete only the Instrument_identify function. You can add helper functions but make sure
#  that these functions are called from Instrument_identify function. The final output should be returned
#  from the Instrument_identify function.
#
#  Note: While evaluation we will use only the onset_detect function. Hence the format of input, output
#  or returned arguments should be as per the given format.
#  
#  Recommended Python version is 2.7.
#  The submitted Python file must be 2.7 compatible as the evaluation will be done on Python 2.7.
#  
#  Warning: The error due to compatibility will not be entertained.
#  -------------


## Library initialisation

# Import Modules
# DO NOT import any library/module
# related to Audio Processing here
import numpy as np
import math
import wave
import os
import struct
import librosa as lb

# Teams can add helper functions
# Add all helper functions here

############################### Your Code Here #############################################
'''
* Team Id : 2403
* Author List : S MITRABINDA, AMRIT RAJ

* Filename: Task_2
* Theme: Mocking Bot -eYRC
* Functions: Instrument_identify
* Global Variables: None
'''

def Instrument_identify(audio_file):
        #   Instructions
        #   ------------
        #   Input       :       audio_file -- a single test audio_file as input argument
        #   Output      :       1. Instruments -- List of string corresponding to the Instrument
        #                       2. Detected_Notes -- List of string corresponding to the Detected Notes
        #                       3. Onsets -- List of Float numbers corresponding
        #                               to the Note Onsets (up to Two decimal places)
        #   Example     :       For Audio_1.wav file,
        #                               Instruments = ["Piano","Violin","Piano","Trumpet"]
        #                               Detected_Notes = ["C3","B5","A6","C5"]
        #                               Onsets = [0.00, 0.99, 1.32, 2.04]
        
        # Add your code here
        Instruments = []
        Detected_Notes = []
        Onsets = []
############################## Initialize ##################################


# Some Useful Variables
        window_size = 2205    # Size of window to be used for detecting silence
        sampling_freq = 44100   # Sampling frequency of audio signal
        threshold = 2
        array = [16.35,17.32,18.35,19.45,20.6,21.83,23.12,24.5,25.96,27.5,29.14,                                        
                 30.87,32.7,34.65,36.71,38.89,41.2,43.65,46.25,49,51.91,
                 55,58.27,61.74,65.41,69.3,73.42,77.78,82.41,87.31,92.5,98,103.83,110,116.54,123.47,
                 130.81,138.59,146.83,155.56,164.81,174.61,185,196,207.65,220,233.08,246.94,261.63,277.18,
                 293.66,311.13,329.63,349.23,369.99,392,415.3,440,466.16,493.88,
                 523.25,554.37,587.33,622.25,659.25,698.46,739.99,783.99,830.61,880,932.33,987.77,1046.5,1108.73,
                 1174.66,1244.51,1318.51,1396.91,1479.98,1567.98,1661.22,1760,1864.66,1975.53,2093,2217.46,
                 2349.32,2489.02,2637.02,2793.83,2959.96,3135.96,3322.44,3520,3729.31,3951.07,4186.01,4434.92,
                 4698.63,4978.03,5274.04,5587.65,5919.91,6271.93,6644.88,7040,7458.62,7902.13]

        notes = ['C0','C#0','D0','D#0','E0','F0','F#0','G0','G#0','A0','A#0',
                 'B0','C1','C#1','D1','D#1','E1','F1','F#1','G1','G#1','A1',
                 'A#1','B1','C2','C#2','D2','D#2','E2','F2','F#2','G2',
                 'G#2','A2','A#2','B2','C3','C#3','D3','D#3','E3','F3','F#3',
                 'G3','G#3','A3','A#3','B3','C4','C#4','D4','D#4','E4','F4',
                 'F#4','G4','G#4','A4','A#4','B4',
                 'C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5',
                 'A5','A#5','B5','C6','C#6','D6','D#6','E6',
                 'F6','F#6','G6','G#6','A6','A#6','B6','C7','C#7',
                 'D7','D#7','E7','F7','F#7','G7','G#7',
                 'A7','A#7','B7','C8','C#8','D8','D#8',
                 'E8','F8','F#8','G8','G#8','A8','A#8','B8']

############################## Read Audio File #############################
        '''
* Function Name: wave.open
* Input: path of the file along with task that we want to do
* Output: read the file and store it in a variable
* Logic: This function is used to open the audio file from the path.It is
         also useful in reading the file.
* Example Call: sound_file=wave.open(file_name,'r')
                we can call the function by its name and the path must be defined inside the bracket
                along with the task to be performed.Here,we have used 'r' to read the file only.
                The open function from wave module takes the path to audio file and the
                mode as parameters. We are using mode = ‘r’, i.e. reading mode. In this case wave.open returns a
                Wave_read object.
'''
        sound_file = wave.open(file_name, 'r')
        '''
* Function Name: Wave_read.getnframes()
* Input: sound file that had been read
* Output:rerturns the no. of frames
* Logic: It returns the number of audio frames contained in the file. Loosely
        speaking an audio frame is equivalent to one sample of our discrete audio signal.
* Example Call: file_length = sound_file.getnframes()
'''
        file_length = sound_file.getnframes()
        '''
* Function Name: np.zeros(file_length)
* Input: length of items 
* Output: returns the number of zeros same as the length of input as an array 
* Logic: to create array in order to store the read audio files
* Example Call: sound = np.zeros(10)
        
'''

        sound = np.zeros(file_length)
        mean_square = []
        sound_square = np.zeros(file_length)
        for i in range(file_length):

                data = sound_file.readframes(1)      
                data = struct.unpack("<h", data)
                sound[i] = int(data[0])
    
        sound = np.divide(sound, float(2**15))   # Normalize data in range -1 to 1


######################### DETECTING SCILENCE ##################################
        '''
* Function Name: np.square()
* Input: takes any floating value
* Output: floating value
* Logic: this will square the data
* Example Call: ound = np.square(sound, float(2**15))
'''
    
  

        sound_square = np.square(sound)
        frequency = []
        discrete_fourier_tranform=[]                                                                                                                                                                                                    
        i = 0
        j = 0
        k = 0    
# traversing sound_square array with a fixed window_size
        while(i<=len(sound_square)-window_size):
                s = 0.0
                j = 0
                while(j<=window_size):
                        s = s + sound_square[i+j]
                        j = j + 1       
# detecting the silence waves
                if s < threshold:
                        if(i-k>window_size*4):
  
                                discrete_fourier_tranform = np.array(discrete_fourier_tranform) # applying fourier transform function
                                discrete_fourier_tranform = np.fft.fft(sound[k:i])
                                '''
* Function Name: np.argsort()
* input:data in fourier tranformed form
* Output: Returns the indices that would sort an array.
* Logic: this will be helpful in sorting the array
* Example Call: discrete_fourier_tranform = np.argsort(discrete_fourier_tranform) 
'''
                                discrete_fourier_tranform=np.argsort(discrete_fourier_tranform)

                                if(discrete_fourier_tranform[0]>discrete_fourier_tranform[-1] and discrete_fourier_tranform[1]>discrete_fourier_tranform[-1]):
                                        i_max = discrete_fourier_tranform[-1]
                                elif(discrete_fourier_tranform[1]>discrete_fourier_tranform[0] and discrete_fourier_tranform[-1]>discrete_fourier_tranform[0]):
                                        i_max = discrete_fourier_tranform[0]
                                else :  
                                        i_max = discrete_fourier_tranform[1]
# claculating frequency                         
                                frequency.append((i_max*sampling_freq)/(i-k))
                                discrete_fourier_tranform = []
                                k = i+1
                i = i + window_size 

        for i in frequency :
                idx = (np.abs(array-i)).argmin()
                Detected_Notes.append(notes[idx])
# onset detection

        y,sr=lb.load(file_name,offset=-0.01)                           #using librosa library to load the file
        onset_frames=lb.onset.onset_detect(y,sr=22050)                  #onset detection in frames
        onset_times = lb.frames_to_time(onset_frames)                   #onset conversion in time
        interval=lb.effects.split(y,top_db=17)                          #finding start and end point of respective notes
        onsets_detect=lb.samples_to_time(interval,sr=22050)
        for i in range(0,len(onsets_detect)): 
            new='%0.2f' % onsets_detect[i][0]                           #finding onset upto 2 decimal places
            Onsets.append(new)
        return Instruments, Detected_Notes, Onsets


############################### Main Function #############################################

if __name__ == "__main__":

        #   Instructions
        #   ------------
        #   Do not edit this function.

        # code for checking output for single audio file
        path = os.getcwd()
        
        file_name = path + "/Task_2_Audio_files/Audio_1.wav"
        audio_file = wave.open(file_name)
        
        Instruments, Detected_Notes, Onsets = Instrument_identify(audio_file)

        print("\n\tInstruments = "  + str(Instruments))
        print("\n\tDetected Notes = " + str(Detected_Notes))
        print("\n\tOnsets = " + str(Onsets))
        # code for checking output for all audio files
        
        x  =  raw_input("\n\tWant to check output for all Audio Files - Y/N: ")
                
        if x  ==  'Y':

                Instruments_list = []
                Detected_Notes_list = []
                Onsets_list = []
                
                file_count = len(os.listdir(path + "/Task_2_Audio_files"))

                for file_number in range(1, file_count-1):

                        file_name = path + "/Task_2_Audio_files/Audio_"+str(file_number)+".wav"
                        audio_file = wave.open(file_name)
                        
                        Instruments, Detected_Notes,Onsets = Instrument_identify(audio_file)
                        
                        Instruments_list.append(Instruments)
                        Detected_Notes_list.append(Detected_Notes)
                        Onsets_list.append(Onsets)
                print("\n\tInstruments = " + str(Instruments_list))
                print("\n\tDetected Notes = " + str(Detected_Notes_list))
                print("\n\tOnsets = " + str(Onsets_list))

