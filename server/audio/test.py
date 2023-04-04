import av

container = av.open('./48k/mono/test.wav',mode='r')
#container.bit_rate=64002
#audio=container.streams.audio[0]
# audio.bit_rate=64000
# print(audio.bit_rate)
frames=container.decode(audio=0)
for frame in frames:
        print(frame)