# -*- coding: utf-8 -*-
"""LSTM Bit Flipper - PyTorch Lightning Version

Ported from TensorFlow implementation.
"""

import os
import numpy as np
import torch
import torch.nn as nn
import lightning as L
from torch.utils.data import DataLoader, TensorDataset

NUM_WORKERS = os.cpu_count() or 1


def generate_data(
  num_sequences: int, min_length: int = 5, max_length: int = 20
) -> tuple[np.ndarray, np.ndarray]:
  """Generate training data with random binary sequences and their flipped versions."""
  sequences = []
  targets = []
  lengths = np.random.randint(min_length, max_length + 1, num_sequences)

  for length in lengths:
    sequence = np.random.randint(0, 2, (length, 1))
    sequences.append(sequence)
    targets.append(1 - sequence)  # Flip the bits

  # Pad sequences to the same length
  max_len = max(lengths)
  padded_sequences = np.zeros((num_sequences, max_len, 1), dtype=np.float32)
  padded_targets = np.zeros((num_sequences, max_len, 1), dtype=np.float32)

  for i, (seq, tgt) in enumerate(zip(sequences, targets)):
    padded_sequences[i, : len(seq)] = seq
    padded_targets[i, : len(tgt)] = tgt

  return padded_sequences, padded_targets


def test_generate_data() -> None:
  """Test the data generation function."""
  sequences, targets = generate_data(1)
  print('Sequences:', sequences)
  print('Targets:', targets)


class SequenceFlipper(L.LightningModule):
  """LSTM model that learns to flip binary sequences."""

  def __init__(self, hidden_size: int = 64, dropout: float = 0.2):
    super().__init__()
    self.save_hyperparameters()

    self.lstm = nn.LSTM(
      input_size=1, hidden_size=hidden_size, batch_first=True, dropout=0.0
    )
    self.dropout = nn.Dropout(dropout)
    self.output_layer = nn.Linear(hidden_size, 1)

  def forward(self, x: torch.Tensor) -> torch.Tensor:
    lstm_out, _ = self.lstm(x)
    lstm_out = self.dropout(lstm_out)
    output = torch.sigmoid(self.output_layer(lstm_out))
    return output

  def training_step(
    self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int
  ) -> torch.Tensor:
    x, y = batch
    y_hat = self(x)
    loss = nn.functional.binary_cross_entropy(y_hat, y)
    acc = ((y_hat > 0.5).float() == y).float().mean()
    self.log('train_loss', loss, prog_bar=True)
    self.log('train_acc', acc, prog_bar=True)
    return loss

  def validation_step(
    self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int
  ) -> torch.Tensor:
    x, y = batch
    y_hat = self(x)
    loss = nn.functional.binary_cross_entropy(y_hat, y)
    acc = ((y_hat > 0.5).float() == y).float().mean()
    self.log('val_loss', loss, prog_bar=True)
    self.log('val_acc', acc, prog_bar=True)
    return loss

  def configure_optimizers(self) -> torch.optim.Optimizer:
    return torch.optim.Adam(self.parameters())


def train_sequence_flipper() -> tuple[SequenceFlipper, L.Trainer]:
  """Create and train the model."""
  # Generate training data
  X_train, y_train = generate_data(1000)
  X_val, y_val = generate_data(200)

  assert X_train.dtype == np.float32
  assert X_val.dtype == np.float32
  assert X_train.shape == (1000, 20, 1)
  assert X_val.shape == (200, 20, 1)

  # Convert to PyTorch tensors
  train_dataset = TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train))
  val_dataset = TensorDataset(torch.from_numpy(X_val), torch.from_numpy(y_val))

  train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    persistent_workers=True,
    num_workers=NUM_WORKERS,
  )
  val_loader = DataLoader(
    val_dataset, batch_size=32, persistent_workers=True, num_workers=NUM_WORKERS
  )

  # Create model and trainer
  model = SequenceFlipper()
  trainer = L.Trainer(max_epochs=20, enable_progress_bar=True, logger=False)

  # Train the model
  trainer.fit(model, train_loader, val_loader)

  return model, trainer


def predict_sequence(model: SequenceFlipper, input_sequence: np.ndarray) -> np.ndarray:
  """Use the model for predictions."""
  model.eval()
  with torch.no_grad():
    input_tensor = torch.from_numpy(input_sequence.reshape(1, -1, 1))
    predictions = model(input_tensor)
    return (predictions.numpy() > 0.5).astype(int)


if __name__ == '__main__':
  test_generate_data()

  # Train the model
  model, trainer = train_sequence_flipper()

  while True:
    test_sequence = np.array(
      input('sequence (comma separated): ').split(','), dtype=np.float32
    ).reshape(-1, 1)
    result = predict_sequence(model, test_sequence)
    print('Input sequence:', test_sequence.flatten())
    print('Flipped sequence:', result[0].flatten())
