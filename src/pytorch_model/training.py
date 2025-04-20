import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models

from src.pytorch_model.food_dataset import prepare_data, LEARNING_RATE, NUM_EPOCHS


def train_model():
    # Prepare data
    train_loader, val_loader, num_classes = prepare_data()
    print('start training model:', train_loader)

    # Set up device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Create model
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    # Replace the final layer for multi-label classification
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model = model.to(device)

    # Define loss function and optimizer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=2)

    # Training loop
    best_val_loss = float('inf')

    for epoch in range(NUM_EPOCHS):
        # Training phase
        model.train()
        train_loss = 0.0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)

        train_loss = train_loss / len(train_loader.dataset)

        # Validation phase
        model.eval()
        val_loss = 0.0

        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)

        val_loss = val_loss / len(val_loader.dataset)

        # Update learning rate
        scheduler.step(val_loss)

        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), '../../food_model.pth')

        print(f'Epoch {epoch + 1}/{NUM_EPOCHS}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')

    return model

if __name__ == "__main__":
    train_model()