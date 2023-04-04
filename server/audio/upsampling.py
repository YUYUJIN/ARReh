import numpy as np
import scipy.io.wavfile
import scipy.signal

required_num_samples = 1065601
required_sample_rate = 96000

# read 48k wav file
fname = './audio/test8.wav'
#print 'Loading file {}...'.format(fname)
rate, data = scipy.io.wavfile.read(fname)
print ('Rate = {}, samples = {}'.format(rate, len(data)))
assert rate == 48000, 'sample rate must be 48000'

# resample using FFT and convert back to int16
resampling_factor = 2
samples = len(data) * resampling_factor
rate_new = rate * resampling_factor
print ('Resample (FFT) to rate = {}, and samples = {}...'.format(rate_new, samples))
_ = scipy.signal.resample(data, samples).astype(np.int16)

# append data to ndarray - add the last sample
n = len(_)
print ('Num of samples = {}'.format(n))
assert n == samples, 'Num of samples is wrong'
#print 'Adding sample(s)...'
value = _[-1]
__ = np.append(_, value)
n = len(__)
print ('Num of samples = {}'.format(n))

# write wav file
#assert n == required_num_samples, 'Wrong number of samples'
fname_new = fname + '.new'
scipy.io.wavfile.write(fname_new, rate_new, __)
#print 'New file: {}'.format(fname_new)
#print 'Finished.'