import zhtts

# tts = zhtts.TTS(text2mel_name="TACOTRON")
tts = zhtts.TTS(text2mel_name="FASTSPEECH2")

# text = "2020年，这是一个开源的端到端中文语音合成系统"
text = "我的名字是罗汉伦。"
tts = zhtts.TTS() # use fastspeech2 by default

tts.text2wav(text, "demo.wav")
tts.frontend(text)
tts.synthesis(text)
