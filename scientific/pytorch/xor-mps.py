"""Demonstrate the use of MPS (Metal Performance Shader) backend in Pytorch.
"""
import torch
import torch.nn.functional as F


class XORModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = torch.nn.Linear(2, 4)
        self.fc2 = torch.nn.Linear(4, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x

def generate_data():
    # XOR truth table
    data = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    labels = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)
    return data, labels

def train(model, data, labels, epochs=1000, lr=0.01):
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(data)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

def main():
    torch.random.manual_seed(0)
    model = XORModel()
    model.to("mps")
    data, labels = generate_data()
    data, labels = data.to("mps"), labels.to("mps")
    train(model, data, labels)

    model.eval()

    eval_labels = model(data)
    print(eval_labels)

if __name__ == "__main__":
    if torch.backends.mps.is_available():
        print("MPS is available")
        main()
    else:
        print("MPS is not available")
