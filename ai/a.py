import torch

num_of_gpus = torch.cuda.device_count()
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
print(device)