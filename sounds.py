import matplotlib.pyplot as plt
from scipy.io import wavfile
import glob
import os
import math

# 1. Get files sorted by name (sample_01, sample_02...)
files = sorted(glob.glob("Voices_in_my_Head/*.wav"))

if not files:
    print("Error: No .wav files found in Voices_in_my_Head/ folder.")
    exit()

print(f"Found {len(files)} audio files.")

# 2. Setup Plot - Let's look at the first 9 files to see if letters appear
# We create a 3x3 grid
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

for i, file in enumerate(files[60:64]):
    rate, data = wavfile.read(file)
    
    # If stereo, take one channel
    if len(data.shape) > 1:
        data = data[:, 0]
        
    axes[i].specgram(data, Fs=rate, NFFT=1024, noverlap=512)
    axes[i].set_title(os.path.basename(file))
    axes[i].axis('off') # Hide axes for cleaner look

plt.tight_layout()
plt.show()
