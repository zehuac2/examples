# -*- coding: utf-8 -*-
"""LSTM number predictor implemented with PyTorch Lightning."""

import os
from typing import Iterable

import lightning as L
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split

NUM_WORKERS = os.cpu_count() or 1


def generate_sequences(
  start: int = 1, length: int = 1000, seq_length: int = 4
) -> tuple[np.ndarray, np.ndarray]:
  """Generate sequences of consecutive numbers and their next value."""

  numbers = np.arange(start, start + length, dtype=np.float32)
  X, y = [], []

  for i in range(len(numbers) - seq_length):
    X.append(numbers[i : i + seq_length])
    y.append(numbers[i + seq_length])

  X_arr = np.array(X, dtype=np.float32).reshape(-1, seq_length, 1)
  y_arr = np.array(y, dtype=np.float32).reshape(-1, 1)
  return X_arr, y_arr


class NumberPredictor(L.LightningModule):
  """Simple LSTM regressor that predicts the next number in a sequence."""

  def __init__(self, hidden_size: int = 64, dropout: float = 0.1):
    super().__init__()
    self.save_hyperparameters()

    self.lstm = nn.LSTM(
      input_size=1, hidden_size=hidden_size, batch_first=True, dropout=0.0
    )
    self.dropout = nn.Dropout(dropout)
    self.output_layer = nn.Linear(hidden_size, 1)

  def forward(self, x: torch.Tensor) -> torch.Tensor:
    lstm_out, _ = self.lstm(x)
    last_hidden = lstm_out[:, -1, :]
    last_hidden = self.dropout(last_hidden)
    return self.output_layer(last_hidden)

  def training_step(
    self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int
  ) -> torch.Tensor:
    x, y = batch
    y_hat = self(x)
    loss = nn.functional.mse_loss(y_hat, y)
    self.log('train_loss', loss, prog_bar=True)
    return loss

  def validation_step(
    self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int
  ) -> torch.Tensor:
    x, y = batch
    y_hat = self(x)
    loss = nn.functional.mse_loss(y_hat, y)
    self.log('val_loss', loss, prog_bar=True)
    return loss

  def configure_optimizers(self) -> torch.optim.Optimizer:
    return torch.optim.Adam(self.parameters(), lr=1e-3)


def make_dataloaders(
  seq_length: int = 4, length: int = 1000, batch_size: int = 32
) -> tuple[DataLoader, DataLoader]:
  """Create train/validation dataloaders from generated data."""

  X, y = generate_sequences(length=length, seq_length=seq_length)
  dataset = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))

  val_size = max(1, int(0.1 * len(dataset)))
  train_size = len(dataset) - val_size
  train_ds, val_ds = random_split(dataset, [train_size, val_size])

  has_workers = NUM_WORKERS > 0
  train_loader = DataLoader(
    train_ds,
    batch_size=batch_size,
    shuffle=True,
    num_workers=NUM_WORKERS,
    persistent_workers=has_workers,
  )
  val_loader = DataLoader(
    val_ds,
    batch_size=batch_size,
    num_workers=NUM_WORKERS,
    persistent_workers=has_workers,
  )
  return train_loader, val_loader


def train_number_predictor(
  seq_length: int = 4, length: int = 1000, max_epochs: int = 50
) -> tuple[NumberPredictor, L.Trainer]:
  """Create and train the Lightning number predictor."""

  train_loader, val_loader = make_dataloaders(
    seq_length=seq_length, length=length, batch_size=32
  )
  model = NumberPredictor(hidden_size=64, dropout=0.1)

  trainer = L.Trainer(max_epochs=max_epochs, enable_progress_bar=True, logger=False)
  trainer.fit(model, train_loader, val_loader)

  return model, trainer


def predict_next_number(model: NumberPredictor, sequence: Iterable[float]) -> int:
  """Predict the next number given a sequence."""

  model.eval()
  sequence_arr = np.array(list(sequence), dtype=np.float32).reshape(1, -1, 1)
  with torch.no_grad():
    input_tensor = torch.from_numpy(sequence_arr)
    prediction = model(input_tensor).item()
  return round(prediction)


if __name__ == '__main__':
  model, _ = train_number_predictor(seq_length=4, length=1000, max_epochs=30)

  examples = [
    [1, 2, 3, 4],
    [2, 3, 4, 5],
    [5, 6, 7, 8],
    [10, 11, 12, 13],
  ]

  for seq in examples:
    predicted = predict_next_number(model, seq)
    print(f'Input sequence: {seq}')
    print(f'Predicted next number: {predicted}')

  # Variable length input
  variable_seq = [1, 2, 3, 5, 6]
  predicted = predict_next_number(model, variable_seq)
  print(f'Input sequence: {variable_seq}')
  print(f'Predicted next number: {predicted}')
