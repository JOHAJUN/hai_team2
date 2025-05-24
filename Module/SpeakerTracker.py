# SpeakerTracker.py
import torch

class SpeakerTracker:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.load(model_path, map_location=self.device)  # 전체 모델 로드
        self.model.eval()

    def predict(self, audio_features, visual_features):
        with torch.no_grad():
            audio_features = audio_features.to(self.device)
            visual_features = visual_features.to(self.device)
            out = self.model(audio_features, visual_features)
            return torch.argmax(out, dim=1).cpu().numpy()
