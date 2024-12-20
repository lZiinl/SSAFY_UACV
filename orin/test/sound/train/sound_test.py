import torch
import numpy as np
import librosa
import sounddevice as sd
from scipy.io.wavfile import write
from torchvision import transforms
from PIL import Image
import torch.nn as nn
import torchvision.models as models

# GunshotClassifier 정의 (이전에 사용한 모델)
class GunshotClassifier(nn.Module):
    def __init__(self, num_classes):
        super(GunshotClassifier, self).__init__()
        self.model = models.resnet50(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        x = self.model(x)
        return x
    
# 멜 스펙트로그램 변환 함수
def preprocess_audio(y, sr=22050, duration=1.0, n_mels=128):
    if len(y) < sr * duration:
        y = np.pad(y, (0, sr * duration - len(y)), mode='constant')
    y = y[:sr]
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    return mel_spec_db

# 모델을 로드하고 평가 모드로 전환
num_classes = 6
model = GunshotClassifier(num_classes=num_classes)
model.load_state_dict(torch.load('new_model.pth', map_location=torch.device('cpu')))
model.eval()

# 데이터 증강 및 전처리 설정
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# 샘플 음원을 예측하는 함수
def predict_gunshot(y, model, transform, classes, sr=22050):
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

# 총기 클래스 리스트
classes = ['ACE', 'AKM', 'AUG', 'M416', 'M762', 'SCAR']

# 마이크 입력을 통해 오디오 캡처 및 예측
def record_and_predict(duration=1.0, sr=22050):
    print("Recording...")
    y = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()
    y = y.flatten()

    predicted_class = predict_gunshot(y, model, transform, classes, sr)
    print(f'The predicted gunshot class is: {predicted_class}')

# 키보드 인터럽트로 루프 종료
try:
    print("Press Ctrl+C to stop the recording.")
    while True:
        record_and_predict(duration=2.0, sr=22050)
except KeyboardInterrupt:
    print("Recording stopped by user.")

