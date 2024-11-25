import torch.nn as nn
import torch

class NetWidth(nn.Module):
        def __init__(self):
            super(NetWidth, self).__init__()
            self.CONV = nn.Sequential(
                nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(64, affine=False),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2, stride=2),
                nn.Conv2d(64, 32, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(32, affine=False),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2, stride=2),
                nn.Conv2d(32, 16, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(16, affine=False),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2, stride=2)
            )
            self.LIN = nn.Sequential(
                nn.Linear(in_features=16 * 4 * 4, out_features=32),
                nn.ReLU(),
                nn.Linear(in_features=32, out_features=6)
            )

        def forward(self, x):
            out = self.CONV(x)
            out = torch.flatten(out, 1)
            out = self.LIN(out)
            return out

class Net_width(nn.Module):
        def __init__(self):
                super(Net_width,self).__init__()
                self.CONV = nn.Sequential(
                      nn.Conv2d(1,64,kernel_size=3,stride=1,padding=1),
                      nn.BatchNorm2d(64, affine=False),
                      nn.ReLU(),
                      nn.MaxPool2d(kernel_size=2,stride=2),
                      nn.Conv2d(64,32,kernel_size=3,stride=1,padding=1),
                      nn.BatchNorm2d(32, affine=False),
                      nn.ReLU(),
                      nn.MaxPool2d(kernel_size=2,stride=2),
                      nn.Conv2d(32,16,kernel_size=3,stride=1,padding=1),
                      nn.BatchNorm2d(16, affine=False),
                      nn.ReLU(),
                      nn.MaxPool2d(kernel_size=2,stride=2)
                )
                self.LIN = nn.Sequential(
                      nn.Linear(in_features=16*4*4,out_features=128),
                      nn.ReLU(),
                      nn.Linear(in_features=128,out_features=62)
                )
        def forward(self, x):
            out = self.CONV(x)
            out = torch.flatten(out,1)
            out = self.LIN(out)
            return out
        
