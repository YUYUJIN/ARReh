import pyttsx3 as tts

text="오른쪽 다리를 그대로 쭉 뒤로 뻗어 자세를 유지하세요 "
engine=tts.init()
engine.setProperty('rate',150) #말하기 속도
engine.setProperty('volume',1) #볼륨(0~1)
engine.say(text)
engine.save_to_file(text,"./audio/origin/30.wav")
engine.runAndWait()