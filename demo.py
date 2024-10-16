import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch.utils.tensorboard import SummaryWriter
import torch.autograd.profiler as profiler
import torch.quantization
from captum.attr import IntegratedGradients
import torch.jit

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define the model
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28*28)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleNN().to(device)

# Data Loading
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Training Loop
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def train(model, train_loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    return running_loss / len(train_loader)

# TensorBoard Integration
writer = SummaryWriter('runs/mnist_experiment')

# Log the model graph
dataiter = iter(train_loader)
images, labels = next(dataiter)
writer.add_graph(model, images.to(device))

# Log training loss
for epoch in range(2):
    loss = train(model, train_loader, criterion, optimizer, device)
    writer.add_scalar('training loss', loss, epoch)
    print(f'Epoch {epoch+1}, Loss: {loss:.4f}')

writer.close()

# Profiling
with profiler.profile(record_shapes=True) as prof:
    with profiler.record_function("model_inference"):
        model.eval()
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)

print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))

# TorchScript
scripted_model = torch.jit.script(model)
scripted_model.save("mnist_model.pt")

# Quantization
quantized_model = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)

# Save the quantized model
torch.jit.save(torch.jit.script(quantized_model), "mnist_quantized_model.pt")

# Captum for Model Interpretability
model.eval()
ig = IntegratedGradients(model)

# Get a sample image
dataiter = iter(test_loader)
images, labels = next(dataiter)
image = images[0].unsqueeze(0).to(device)

# Compute attributions
attributions, delta = ig.attribute(image, target=labels[0], return_convergence_delta=True)

print('Attributions:', attributions)
print('Convergence Delta:', delta)
