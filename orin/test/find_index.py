import pyaudio

audio = pyaudio.PyAudio()

# 모든 오디오 장치의 정보를 출력
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    print(f"Device Index: {i}, Name: {device_info['name']}, Max Input Channels: {device_info['maxInputChannels']}")

audio.terminate()

