import zhtts
from scipy.io import wavfile

# text = "2020年，这是一个开源的端到端中文语音合成系统"
text = "我的名字是罗汉伦。"
# tts = zhtts.TTS() # use fastspeech2 by default
tts = zhtts.TTS(text2mel_name="TACOTRON")
# tts = zhtts.TTS(text2mel_name="FASTSPEECH2")

# tts.text2wav(text, "demo.wav")
# tts.frontend(text)
# tts.sample_rate = 14000   # deep voice
tts.sample_rate = 24000   # normal
# tts.sample_rate = 30000   # kid?
audio = tts.synthesis(text, sil_time=0.1)

wavfile.write("demo.wav", tts.sample_rate, audio)
