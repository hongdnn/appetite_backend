import torch.nn as nn
from torchvision import models


class FoodModel(nn.Module):
    def __init__(self, num_classes):
        super(FoodModel, self).__init__()
        # Load pre-trained ResNet50
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        # Replace the final layer for multi-label classification
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        return self.model(x)