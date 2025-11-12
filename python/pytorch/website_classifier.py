from argparse import ArgumentParser
from enum import Enum
from typing import Tuple
from torch import nn
import torch
import torch.nn.functional as F
import string


letters = string.ascii_lowercase + '@.' + string.digits


class WebsiteType(Enum):
  NORMAL = 0
  NSFW = 1
  FRAUD = 2

  @property
  def array(self) -> list:
    zeros = [0] * len(WebsiteType)
    zeros[self.value] = 1
    return zeros


class CharToInt:
  def __init__(self) -> None:
    self.mapping = dict()
    self.next_value = 0

    for letter in letters:
      self.mapping[letter] = self.next_value
      self.next_value += 1

  def encode(self, s: str) -> list:
    numbers = []
    for char in s:
      numbers.append(self.mapping[char])

    return numbers

  def __call__(self, s: str) -> list:
    return self.encode(s)

  @property
  def vocab_size(self) -> int:
    return self.next_value


class WebsiteClassifier(nn.Module):
  def __init__(self, vocab_size: int) -> None:
    super().__init__()

    self.embedding_dim = 5
    self.embedding = nn.Embedding(vocab_size, self.embedding_dim)
    self.rnn = nn.RNN(self.embedding_dim, 20, 1, batch_first=True, nonlinearity='relu')
    # self.linear1 = nn.Linear(20, 10)
    # self.linear2 = nn.Linear(10, 5)
    self.bn = nn.BatchNorm1d(20)
    self.linear3 = nn.Linear(20, len(WebsiteType))

  def forward(self, x: torch.Tensor) -> torch.Tensor:
    x = self.embedding(x)
    _, x = self.rnn(x)
    x = x.permute(1, 0, 2)
    x = x.view(x.size(0), -1)

    # x = F.relu(self.linear1(x))
    # x = F.relu(self.linear2(x))
    x = self.bn(x)
    x = F.sigmoid(self.linear3(x))
    return x


def generate_websites() -> Tuple[list, list]:
  websites = list()
  labels = list()

  websites.append('google.com')
  labels.append(WebsiteType.NORMAL)

  websites.append('microsoft.com')
  labels.append(WebsiteType.NORMAL)

  websites.append('apple.com')
  labels.append(WebsiteType.NORMAL)

  websites.append('bankofamerica.com')
  labels.append(WebsiteType.NORMAL)

  websites.append('ixl.com')
  labels.append(WebsiteType.NORMAL)

  websites.append('pornhub.com')
  labels.append(WebsiteType.NSFW)

  websites.append('xvideos.com')
  labels.append(WebsiteType.NSFW)

  websites.append('clips4sale.com')
  labels.append(WebsiteType.NSFW)

  websites.append('xhamster.com')
  labels.append(WebsiteType.NSFW)

  websites.append('bankoffamerica.com')
  labels.append(WebsiteType.FRAUD)

  return websites, labels


def preprocess(
  raw_websites: Tuple[list, list],
) -> Tuple[torch.Tensor, torch.Tensor, CharToInt]:
  char_to_int = CharToInt()
  websites = list()
  labels = list()

  raw_X, raw_y = raw_websites

  # Find maximum length
  max_length = max(len(website) for website in raw_X)

  for raw_website, raw_label in zip(raw_X, raw_y):
    # Convert email to numbers and pad with zeros
    website_nums = char_to_int(raw_website)
    padded_website = [0] * (max_length - len(website_nums)) + website_nums
    websites.append(padded_website)
    labels.append(raw_label.array)

  return (
    torch.as_tensor(websites),
    torch.as_tensor(labels, dtype=torch.float32),
    char_to_int,
  )


def train(model: nn.Module, X: torch.Tensor, y: torch.Tensor):
  # shuffle X and y
  indices = torch.randperm(X.size(0))
  X = X[indices]
  y = y[indices]

  criterion = nn.BCELoss()
  optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

  n_epochs = 6000
  for epoch in range(n_epochs):
    # Training
    model.train()
    optimizer.zero_grad()
    outputs = model(X)
    loss = criterion(outputs, y)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
      print(f'Epoch [{epoch + 1}/{n_epochs}], Loss: {loss:.4f}')


def main():
  torch.manual_seed(0)
  parser = ArgumentParser()
  parser.add_argument('--device', default='cpu')

  options = parser.parse_args()
  device = torch.device(options.device)

  X, y, map = preprocess(generate_websites())
  model = WebsiteClassifier(map.vocab_size).to(device)
  X, y = X.to(device), y.to(device)

  train(model, X, y)

  model.eval()

  with torch.no_grad():
    while True:
      website = input('Enter a website: ')
      website = torch.as_tensor(map(website), dtype=torch.long).to(device)
      website = website.unsqueeze(0)

      classification = model(website)

      print(classification)


if __name__ == '__main__':
  main()
