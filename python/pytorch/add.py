import torch
import torch.nn.functional as F
import argparse


class AddModel(torch.nn.Module):
  def __init__(self):
    super().__init__()
    self.fc1 = torch.nn.Linear(2, 1, bias=False)

  def forward(self, x):
    x = self.fc1(x)
    return x


def generate_data():
  # Generate data for addition
  data = torch.randint(0, 100, (100, 2), dtype=torch.float32)
  labels = torch.sum(data, 1, keepdim=True)

  # Shuffle and split data
  shuffled_indices = torch.randperm(data.size(0))
  data = data[shuffled_indices]
  labels = labels[shuffled_indices]

  split_idx = int(0.8 * data.size(0))
  train_data, val_data = data[:split_idx], data[split_idx:]
  train_labels, val_labels = labels[:split_idx], labels[split_idx:]

  return train_data, train_labels, val_data, val_labels


def train(model, train_data, train_labels, val_data, val_labels, epochs=1200, lr=0.01):
  criterion = torch.nn.MSELoss()
  optimizer = torch.optim.Adam(model.parameters(), lr=lr)

  for epoch in range(epochs):
    # Training
    model.train()
    optimizer.zero_grad()
    train_outputs = model(train_data)
    train_loss = criterion(train_outputs, train_labels)
    train_loss.backward()
    optimizer.step()

    # Validation
    model.eval()
    with torch.no_grad():
      val_outputs = model(val_data)
      val_loss = criterion(val_outputs, val_labels)

    if (epoch + 1) % 100 == 0:
      print(
        f'Epoch [{epoch + 1}/{epochs}], Train Loss: {train_loss.item():.4f}, Val Loss: {val_loss.item():.4f}'
      )


def parse_args():
  parser = argparse.ArgumentParser(description='Add Neural Network')
  parser.add_argument(
    '--device', type=str, default='cpu', help='Device to run on (cpu, cuda, mps)'
  )
  return parser.parse_args()


def main():
  args = parse_args()
  device = torch.device(args.device)

  print(f'Training on device {device}')

  torch.random.manual_seed(0)
  model = AddModel()
  model.to(device)
  train_data, train_labels, val_data, val_labels = generate_data()
  train_data, train_labels = train_data.to(device), train_labels.to(device)
  val_data, val_labels = val_data.to(device), val_labels.to(device)
  train(model, train_data, train_labels, val_data, val_labels)

  model.eval()
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
