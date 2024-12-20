import torch
import numpy as np
import librosa
import sounddevice as sd
from scipy.io.wavfile import write
from torchvision import transforms
from PIL import Image
import torch.nn as nn
import torchvision.models as models
from torchvision.models import ResNet50_Weights
import os
import paho.mqtt.client as mqtt
import json  # JSON 라이브러리 추가

# GunshotClassifier 정의 (이전에 사용한 모델)
class GunshotClassifier(nn.Module):
    def __init__(self, num_classes):
        super(GunshotClassifier, self).__init__()
        # ResNet50 모델을 최신 권장 방식으로 로드
        weights = ResNet50_Weights.IMAGENET1K_V1  # 또는 ResNet50_Weights.DEFAULT 사용 가능
        self.model = models.resnet50(weights=weights)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        x = self.model(x)
        return x
    
# 멜 스펙트로그램 변환 함수
def preprocess_audio(y, sr=44100, duration=1.0, n_mels=128):
    if len(y) < sr * duration:
        y = np.pad(y, (0, sr * duration - len(y)), mode='constant')
    y = y[:sr]
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    return mel_spec_db

# 모델을 로드하고 평가 모드로 전환
num_classes = 6
model = GunshotClassifier(num_classes=num_classes)
# 보안 문제를 피하기 위해 weights_only=True로 설정
model.load_state_dict(torch.load('new_model.pth', map_location=torch.device('cpu'), weights_only=True))
model.eval()

# 데이터 증강 및 전처리 설정
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# 샘플 음원을 예측하는 함수
def predict_gunshot(y, model, transform, classes, sr=44100):
    mel_spec_db = preprocess_audio(y, sr)
    min_val = mel_spec_db.min()
    max_val = mel_spec_db.max()
    if max_val - min_val != 0:
        mel_spec_db = (mel_spec_db - min_val) / (max_val - min_val)
    else:
        mel_spec_db = np.zeros_like(mel_spec_db)
    
    mel_spec_db = (mel_spec_db * 255).astype(np.uint8)
    image = Image.fromarray(mel_spec_db).convert('RGB')
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs.data, 1)
        predicted_class = classes[predicted.item()]

    return predicted_class

# MQTT 설정
#MQTT_BROKER = "i11c102.p.ssafy.io"  # MQTT 브로커 주소
MQTT_BROKER = "192.168.0.4"
MQTT_PORT = 1883  # MQTT 포트 (기본: 1883)
MQTT_TOPIC = "orin/sensor"  # MQTT 주제

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
#client.username_pw_set(username="orin", password="ssafyi11C102!!")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")

client.on_connect = on_connect
client.on_disconnect = on_disconnect

# 총기 클래스 리스트
classes = ['ACE', 'AKM', 'AUG', 'M416', 'M762', 'SCAR']

# 녹음된 파일을 저장하고 예측하는 함수
def record_and_predict(duration=1.0, sr=44100, save_path="recordings"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    print("Recording...")
    y = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()
    y = y.flatten()

    predicted_class = predict_gunshot(y, model, transform, classes, sr)
    print(f'The predicted gunshot class is: {predicted_class}')

    message = {
            "gun": predicted_class
            }

    client.publish(MQTT_TOPIC, json.dumps(message))
# 키보드 인터럽트로 루프 종료
try:
    print("Press Ctrl+C to stop the recording.")
    while True:
        record_and_predict(duration=2.0, sr=44100)
except KeyboardInterrupt:
    print("Recording stopped by user.")

