import argparse

import lightning as L
import torch
from torch.utils.data import DataLoader, TensorDataset


class AddLitModule(L.LightningModule):
  def __init__(self, lr: float = 0.01):
    super().__init__()
    self.save_hyperparameters()
    self.lr = lr
    self.fc1 = torch.nn.Linear(2, 1, bias=False)
    self.criterion = torch.nn.MSELoss()

  def forward(self, x: torch.Tensor) -> torch.Tensor:
    return self.fc1(x)

  def training_step(self, batch, batch_idx: int):
    data, targets = batch
    preds = self(data)
    loss = self.criterion(preds, targets)
    self.log('train_loss', loss, prog_bar=True)
    return loss

  def validation_step(self, batch, batch_idx: int):
    data, targets = batch
    preds = self(data)
    loss = self.criterion(preds, targets)
    self.log('val_loss', loss, prog_bar=True)

  def configure_optimizers(self):
    return torch.optim.Adam(self.parameters(), lr=self.lr)


class AddDataModule(L.LightningDataModule):
  def __init__(self, batch_size: int = 32, dataset_size: int = 100):
    super().__init__()
    self.batch_size = batch_size
    self.dataset_size = dataset_size
    self.train_dataset = None
    self.val_dataset = None

  def setup(self, stage: str | None = None):
    data = torch.randint(0, 100, (self.dataset_size, 2), dtype=torch.float32)
    labels = torch.sum(data, 1, keepdim=True)

    shuffled_indices = torch.randperm(data.size(0))
    data = data[shuffled_indices]
    labels = labels[shuffled_indices]

    split_idx = int(0.8 * data.size(0))
    train_data, val_data = data[:split_idx], data[split_idx:]
    train_labels, val_labels = labels[:split_idx], labels[split_idx:]

    self.train_dataset = TensorDataset(train_data, train_labels)
    self.val_dataset = TensorDataset(val_data, val_labels)

  def train_dataloader(self):
    if self.train_dataset is None:
      raise RuntimeError(
        'train_dataset not initialized; call setup() before train_dataloader().'
      )
    return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

  def val_dataloader(self):
    if self.val_dataset is None:
      raise RuntimeError(
        'val_dataset not initialized; call setup() before val_dataloader().'
      )
    return DataLoader(self.val_dataset, batch_size=self.batch_size)


def parse_args():
  parser = argparse.ArgumentParser(
    description='Add Neural Network with PyTorch Lightning'
  )
  parser.add_argument('--device', type=str, default='cpu', help='cpu | cuda | mps')
  parser.add_argument(
    '--max_epochs', type=int, default=400, help='Number of training epochs'
  )
  parser.add_argument('--batch_size', type=int, default=32, help='Mini-batch size')
  parser.add_argument(
    '--dataset_size', type=int, default=100, help='Number of examples to generate'
  )
  parser.add_argument('--lr', type=float, default=0.01, help='Learning rate')
  return parser.parse_args()


def main():
  args = parse_args()
  print(f'Training on accelerator {args.device}')

  L.seed_everything(0)

  model = AddLitModule(lr=args.lr)
  data_module = AddDataModule(
    batch_size=args.batch_size, dataset_size=args.dataset_size
  )

  trainer = L.Trainer(
    accelerator=args.device,
    devices=1,
    max_epochs=args.max_epochs,
    logger=False,
    enable_checkpointing=False,
    enable_model_summary=False,
  )

  trainer.fit(model, data_module)

  model.eval()
  device = trainer.strategy.root_device
  test_data = torch.tensor(
    [[10, 20], [5, 5], [1, 2], [45, 32], [1000, 100]], dtype=torch.float32
  ).to(device)
  predictions = model(test_data)

  for i in range(test_data.shape[0]):
    x, y = test_data[i].tolist()
    z = predictions[i].item()
    print(f'{x} + {y} = {z:.4f}')

  print(model.state_dict())


if __name__ == '__main__':
  main()
