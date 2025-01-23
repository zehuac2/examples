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
    def __init__(self, vocab_size: int) -> None:
        super().__init__()

        self.embedding_dim = 5
        self.embedding = nn.Embedding(vocab_size, self.embedding_dim)
        self.rnn = nn.RNN(self.embedding_dim, 20, 1, batch_first=True, nonlinearity="relu")
        self.linear1 = nn.Linear(20, 10)
        self.linear2 = nn.Linear(10, 5)
        self.linear3 = nn.Linear(5, 3)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embedding(x)
        _, x = self.rnn(x)
        x = x.permute(1, 0, 2)
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
        email = ''.join(person) + '@gmail.com'
        emails.append(email)
        labels.append(EmailDomain.PRIVATE_INDIVIDUAL)

    for person in random_people:
        email = ''.join(person) + '@outlook.com'
        emails.append(email)
        labels.append(EmailDomain.PRIVATE_INDIVIDUAL)

    # education institutions 1
    for person in random_people:
        email = ''.join(person) + '@illinois.edu'
        emails.append(email)
        labels.append(EmailDomain.EDUCATION_INSTITUTION)

    # education institutions 1
    for person in random_people:
        email = ''.join(person) + '@berkley.edu'
        emails.append(email)
        labels.append(EmailDomain.EDUCATION_INSTITUTION)

    # private company 1
    for person in random_people:
        email = ''.join(person) + '@aaa.com'
        emails.append(email)
        labels.append(EmailDomain.PRIVATE_COMPANY)

    for person in random_people:
        email = ''.join(person) + '@microsoft.com'
        emails.append(email)
        labels.append(EmailDomain.PRIVATE_COMPANY)

    for person in random_people:
        email = ''.join(person) + '@google.com'
        emails.append(email)
        labels.append(EmailDomain.PRIVATE_COMPANY)

    return emails, labels

def preprocess(raw_emails: Tuple[list, list]) -> Tuple[torch.Tensor, torch.Tensor, CharToInt]:
    char_to_int = CharToInt()
    emails = list()
    labels = list()

    raw_X, raw_y = raw_emails

    # Find maximum length
    max_length = max(len(email) for email in raw_X)

    for (raw_email, raw_label) in zip(raw_X, raw_y):
        # Convert email to numbers and pad with zeros
        email_nums = char_to_int.map(raw_email)
        padded_email = email_nums + [0] * (max_length - len(email_nums))
        emails.append(padded_email)
        labels.append(raw_label.value)

    return torch.as_tensor(emails), torch.as_tensor(labels, dtype=torch.float32), char_to_int

def create_batches(X: torch.Tensor, y: torch.Tensor, batch_size: int):
    for i in range(0, len(X), batch_size):
        yield X[i:i + batch_size], y[i:i + batch_size]

def train(model: nn.Module, X: torch.Tensor, y: torch.Tensor):
    # shuffle X and y
    indices = torch.randperm(X.size(0))
    X = X[indices]
    y = y[indices]

    # Split data into train/val (80/20)
    train_size = int(0.8 * len(X))
    X_train, X_val = X[:train_size], X[train_size:]
    y_train, y_val = y[:train_size], y[train_size:]

    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    batch_size = 25

    n_epochs = 2000
    for epoch in range(n_epochs):
        # Training
        model.train()
        total_train_loss = 0
        for batch_X, batch_y in create_batches(X_train, y_train, batch_size):
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()

        # Validation
        model.eval()
        total_val_loss = 0
        with torch.no_grad():
            for batch_X, batch_y in create_batches(X_val, y_val, batch_size):
                val_outputs = model(batch_X)
                val_loss = criterion(val_outputs, batch_y)
                total_val_loss += val_loss.item()

        if (epoch + 1) % 10 == 0:
            avg_train_loss = total_train_loss * batch_size / len(X_train)
            avg_val_loss = total_val_loss * batch_size / len(X_val)
            print(f'Epoch [{epoch+1}/{n_epochs}], Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}')

def main():
    torch.manual_seed(0)
    parser = ArgumentParser()
    parser.add_argument("--device", default="cpu")

    options = parser.parse_args()
    device = torch.device(options.device)

    X, y, map = preprocess(generate_emails())
    model = EmailClassifier(map.vocab_size).to(device)
    X, y = X.to(device), y.to(device)

    train(model, X, y)

    model.eval()

    while True:
        email = input("Enter an email: ")
        email = torch.as_tensor(map.map(email), dtype=torch.long).to(device)
        email = email.unsqueeze(0)

        print(model(email))

if __name__ == "__main__":
    main()
