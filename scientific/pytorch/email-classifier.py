from argparse import ArgumentParser
from enum import Enum
from typing import Tuple
from torch import nn
import torch
import torch.nn.functional as F
import itertools
import string


letters = string.ascii_lowercase + '@.'


class EmailDomain(Enum):
    PRIVATE_INDIVIDUAL = [1, 0, 0]
    EDUCATION_INSTITUTION = [0, 1, 0]
    PRIVATE_COMPANY = [0, 0, 1]

class CharToInt:
    def __init__(self) -> None:
        self.mapping = dict()
        self.next_value = 0

        for letter in letters:
            self.mapping[letter] = self.next_value
            self.next_value += 1

    def map(self, email: str) -> list:
        numbers = []
        for char in email:
            numbers.append(self.mapping[char])

        return numbers

    @property
    def vocab_size(self) -> int:
        return self.next_value


class EmailClassifier(nn.Module):
    def __init__(self, vocab_size: int, sequence_length: int) -> None:
        super().__init__()

        self.embedding_dim = 3
        self.embedding = nn.Embedding(vocab_size, self.embedding_dim)
        self.linear1 = nn.Linear(self.embedding_dim * sequence_length, 10)
        self.linear2 = nn.Linear(10, 5)
        self.linear3 = nn.Linear(5, 3)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embedding(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = F.sigmoid(self.linear3(x))
        return x

def generate_emails() -> Tuple[list, list]:
    random_people = list(itertools.islice(itertools.permutations(letters, 5), 25))
    emails = list()
    labels = list()

    # private individuals
    for person in random_people:
        email = ''.join(person) + '@abc.com'
        emails.append(email)
        labels.append(EmailDomain.PRIVATE_INDIVIDUAL)

    # education institutions 1
    for person in random_people:
        email = ''.join(person) + '@abc.edu'
        emails.append(email)
        labels.append(EmailDomain.EDUCATION_INSTITUTION)

    # private company 1
    for person in random_people:
        email = ''.join(person) + '@aaa.com'
        emails.append(email)
        labels.append(EmailDomain.PRIVATE_COMPANY)

    return emails, labels

def preprocess(raw_emails: Tuple[list, list]) -> Tuple[torch.Tensor, torch.Tensor, CharToInt]:
    char_to_int = CharToInt()
    emails = list()
    labels = list()

    raw_X, raw_y = raw_emails

    for (raw_email, raw_label) in zip(raw_X, raw_y):
        emails.append(char_to_int.map(raw_email))
        labels.append(raw_label.value)

    return torch.as_tensor(emails), torch.as_tensor(labels, dtype=torch.float32), char_to_int

def train(model: nn.Module, X: torch.Tensor, y: torch.Tensor):
    # Split data into train/val (80/20)
    train_size = int(0.8 * len(X))
    X_train, X_val = X[:train_size], X[train_size:]
    y_train, y_val = y[:train_size], y[train_size:]

    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    n_epochs = 5000
    for epoch in range(n_epochs):
        # Training
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

        # Validation
        model.eval()
        with torch.no_grad():
            val_outputs = model(X_val)
            val_loss = criterion(val_outputs, y_val)

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{n_epochs}], Train Loss: {loss.item():.4f}, Val Loss: {val_loss.item():.4f}')

def main():
    parser = ArgumentParser()
    parser.add_argument("--device", default="cpu")

    options = parser.parse_args()
    device = torch.device(options.device)

    X, y, map = preprocess(generate_emails())
    sequence_length = X.shape[1]
    model = EmailClassifier(map.vocab_size, sequence_length).to(device)
    model.to(device)
    X, y = X.to(device), y.to(device)

    train(model, X, y)

    model.eval()

    while True:
        email = input("Enter an email: ")
        email = email[0:sequence_length]
        email = torch.as_tensor(map.map(email), dtype=torch.long).to(device)
        email = email.unsqueeze(0)

        print(model(email))

if __name__ == "__main__":
    main()
