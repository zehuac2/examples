from torch import nn
import torch


class ExportedModel(nn.Module):
  def __init__(self):
    super().__init__()
    self.fc1 = nn.Linear(2, 4)
    self.fc2 = nn.Linear(4, 1)

  def forward(self, x):
    x = torch.relu(self.fc1(x))
    x = torch.relu(self.fc2(x))
    return x


def main():
  model = ExportedModel()
  input_tensor = torch.rand((1, 2), dtype=torch.float32)

  model(input_tensor)

  torch.onnx.export(model, (input_tensor,), 'model.onnx')


if __name__ == '__main__':
  main()
