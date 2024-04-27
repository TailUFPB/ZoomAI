import torch

cuda = torch.cuda.get_device_name(0)

print(torch.cuda.is_available())
print(cuda)
print(torch.cuda.device_count())
