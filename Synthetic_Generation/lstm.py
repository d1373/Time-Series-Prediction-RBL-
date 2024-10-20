import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Load the data
data = pd.read_csv('synthetic_waste_data.csv')

# Preprocess the data
data['date_time'] = pd.to_datetime(data['date'] + ' ' + data['time'], format='%Y-%m-%d %H:%M')
data = data[['dustbin_id', 'filled_capacity', 'date_time']]
data.set_index('date_time', inplace=True)
data = data.groupby(['dustbin_id']).resample('H').mean().reset_index()
data = data.pivot(index='date_time', columns='dustbin_id', values='filled_capacity').fillna(0)

# Normalize the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# Convert to PyTorch tensors
def create_dataset(data, time_steps=1):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:(i + time_steps)])
        y.append(data[i + time_steps])
    return np.array(X), np.array(y)

time_steps = 24  # Number of hours to look back
X, y = create_dataset(scaled_data, time_steps)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Convert to PyTorch tensors
X_train = torch.Tensor(X_train)
y_train = torch.Tensor(y_train)
X_test = torch.Tensor(X_test)
y_test = torch.Tensor(y_test)

# Define the LSTM model
class LSTMModel(nn.Module):
    def _init_(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self)._init_()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

input_size = X_train.shape[2]
hidden_size = 50
num_layers = 2
output_size = 1

model = LSTMModel(input_size, hidden_size, num_layers, output_size)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the model
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')

# Evaluate the model
model.eval()
with torch.no_grad():
    train_preds = model(X_train).numpy()
    test_preds = model(X_test).numpy()

train_rmse = np.sqrt(mean_squared_error(y_train.numpy(), train_preds))
test_rmse = np.sqrt(mean_squared_error(y_test.numpy(), test_preds))

print(f'Training RMSE: {train_rmse}')
print(f'Test RMSE: {test_rmse}')

# Plot results
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(y_test.numpy(), label='Actual')
plt.plot(test_preds, label='Predicted')
plt.title('Test Data')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(y_train.numpy(), label='Actual')
plt.plot(train_preds, label='Predicted')
plt.title('Training Data')
plt.legend()

plt.show()