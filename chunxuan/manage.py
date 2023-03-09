#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


## 共享底层参数的多任务学习模型 ## 

class ShareBottomModel(nn.Module):
    def __init__(self, input_size, hidden_size, p = 0.2):
        super().__init__()
        self.bottom = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(p),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(p),
        )
        
        self.tower1 = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
        
        self.tower2 = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
        
        self.tower3 = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

        self.tower4 = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

        self.tower5 = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
    
    def forward(self, x):
        return self.tower1(x), self.tower2(x), self.tower3(x), self.tower4(x), self.tower5(x)
    






## 混合专家模型 ##
# 专家块
class Expert(nn.Module):
    def __init__(self, input_size, hidden_size, expert_size):
        super().__init__()
        self.expert_layer = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, expert_size),
            nn.ReLU(),
        )
        
    def forward(self, x):
        return self.expert_layer(x)


# 门控专家网络
class ExpertGate(nn.Module):
    def __init__(self, input_size, hidden_size, expert_size, n_expert, n_task, use_gate = True, multigate = True):
        super().__init__()
        self.n_task = n_task
        self.use_gate = use_gate
        self.multigate = multigate
        
        # 专家网络 #
        # 每个专家网络接受一个输入向量，输出一个向量
        for i in range(n_expert):
            setattr(self, "expert_layer" + str( i + 1), Expert(input_size, hidden_size, expert_size))
        self.expert_layers = [getattr(self, "expert_layer" + str(i + 1)) for i in range(n_expert)]
        
        # 门控网络 #
        # 如果是多门控机制，针对每个子任务设置一组门控单元；如果是单门控，则只使用一组门控单元
        if multigate:
            for i in range(n_task):
                setattr(self, "gate_layer" + str(i + 1), nn.Sequential(nn.Linear(input_size, n_expert), nn.Softmax(dim = 1)))
            self.gate_layers = [getattr(self, "gate_layer" + str(i + 1)) for i in range(n_task)]
        else:
            self.gate_layer = nn.Sequential(
                nn.Linear(input_size, n_expert),
                nn.Softmax(dim = 1)
            )
        
    def forward(self, x):
        if self.use_gate:
            E_net = [expert(x) for expert in self.expert_layers]
            E_net = torch.cat(([e[:, np.newaxis, :] for e in E_net]), dim = 1) # 维度 (batch_size, n_expert, expert_dim)
            towers = []
            
            if self.multigate:
                gate_net = [gate(x) for gate in self.gate_layers] # n_task个(batch_size, n_expert)
                for i in range(self.n_task):
                    g = gate_net[i].unsqueeze(2) # (batch_size, n_expert, 1)
                    tower = torch.matmul(E_net.transpose(1, 2), g) # (batch_size, expert_dim, 1)
                    towers.append(tower.squeeze(-1)) # (batch_size, expert_dim)
            else:
                gate = self.gate_layer(x)
                for i in range(self.n_task):
                    g = gate.unsqueeze(2) 
                    tower = torch.matmul(E_net.transpose(1, 2), g) 
                    towers.append(tower.squeeze(-1)) 
        else:
            E_net = [expert(x) for expert in self.expert_layers]
            towers = sum(E_net) / len(E_net)
        return towers


# MMoE 模型；当不使用多门控机制时退化为单门控MoE模型
class MMoE(nn.Module):
    def __init__(self, input_size, hidden_size, expert_size, n_expert, n_task, use_gate = True, multigate = True):
        super().__init__()
        self.use_gate = use_gate
        self.expert_gate = ExpertGate(input_size, hidden_size, expert_size, n_expert, n_task, use_gate, multigate)
        
        self.tower1 = nn.Sequential(
            nn.Linear(expert_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
        
        self.tower2 = nn.Sequential(
            nn.Linear(expert_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
        
        self.tower3 = nn.Sequential(
            nn.Linear(expert_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

        self.tower4 = nn.Sequential(
            nn.Linear(expert_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

        self.tower5 = nn.Sequential(
            nn.Linear(expert_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
    
    def forward(self, x):
        towers = self.expert_gate(x)
        if self.use_gate:
            output1 = self.tower1(towers[0])
            output2 = self.tower2(towers[1])
            output3 = self.tower3(towers[2])
            output4 = self.tower4(towers[3])
            output5 = self.tower5(towers[4])
        else:
            output1 = self.tower1(towers)
            output2 = self.tower2(towers)
            output3 = self.tower3(towers)
            output4 = self.tower4(towers)
            output5 = self.tower5(towers)
        return output1, output2, output3, output4, output5

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chunxuan.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
