import argparse

import lightning as L
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset


class XORModel(torch.nn.Module):
  def __init__(self):
    super().__init__()
    self.fc1 = torch.nn.Linear(2, 4)
    self.fc2 = torch.nn.Linear(4, 1)

  def forward(self, x):
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    return x


class XORLightningModule(L.LightningModule):
  def __init__(self, lr=0.01, batch_size=4):
    super().__init__()
    self.model = XORModel()
    self.lr = lr
    self.batch_size = batch_size
    self.criterion = torch.nn.MSELoss()
    data, labels = generate_data()
    self.dataset = TensorDataset(data, labels)

  def forward(self, x):
    return self.model(x)

  def training_step(self, batch, batch_idx):
    inputs, targets = batch
    outputs = self(inputs)
    loss = self.criterion(outputs, targets)
    self.log('train_loss', loss, prog_bar=True)
    return loss

  def configure_optimizers(self):
    return torch.optim.Adam(self.parameters(), lr=self.lr)

  def train_dataloader(self):
    return DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True)


def generate_data():
  # XOR truth table
  data = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
  labels = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)
  return data, labels


def parse_args():
  parser = argparse.ArgumentParser(description='XOR Neural Network (Lightning)')
  parser.add_argument(
    '--device', type=str, default='cpu', help='Device to run on (cpu, cuda, mps)'
  )
  parser.add_argument(
    '--epochs', type=int, default=1000, help='Number of training epochs'
  )
  parser.add_argument(
    '--lr', type=float, default=0.01, help='Learning rate for optimizer'
  )
  parser.add_argument(
    '--batch-size', type=int, default=4, help='Batch size for training'
  )
  return parser.parse_args()


def main():
  args = parse_args()
  print(f'Training on device {args.device}')

  torch.random.manual_seed(0)
  module = XORLightningModule(lr=args.lr, batch_size=args.batch_size)
  trainer = L.Trainer(
    max_epochs=args.epochs,
    accelerator=args.device,
    devices=1,
    logger=False,
    enable_checkpointing=False,
    log_every_n_steps=1,
  )
  trainer.fit(module)

  module.eval()
  data, _ = generate_data()
  model_device = next(module.parameters()).device
  data = data.to(model_device)
  with torch.no_grad():
    eval_labels = module(data)
  print(eval_labels.cpu())


if __name__ == '__main__':
  main()
