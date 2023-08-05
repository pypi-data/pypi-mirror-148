import torch
import torch.nn as nn
from torch.nn import Parameter
from transformers import AutoTokenizer, AutoModel, AutoConfig


class get_ascending_optimizer_params():
    def __init__(self,
                 model,
                 ):
        self.model = model

    def return_optimizer_parameters(self,backbone_name,enconder_lr,deconder_lr, coefficient=2.6,weight_decay=0.01,momentum=0.99,no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]):
        group_nums = 3
        backbone_layers = self.model.backbone_name.config.num_attention_heads
        list_layernums = [i for i in range(backbone_layers)]
        list_groupnums = [list_layernums[i*len(list_layernums)//group_nums:i*len(list_layernums)//group_nums+len(list_layernums)//group_nums] for i in range(0,3)]
        group_layers = []
        group_all = []
        for group_temp in list_groupnums:
           temp_list = ['layer.' + str(num) + '.' for num in group_temp]
           group_layers.append(temp_list)
           group_all.extend(temp_list)
        group1, group2, group3 = group_layers
        optimizer_parameters = [
            {'params': [p for n, p in self.model.backbone_name.named_parameters() if not any(nd in n for nd in no_decay) and not any(nd in n for nd in group_all)],'weight_decay': weight_decay},
            {'params': [p for n, p in self.model.backbone_name.named_parameters() if not any(nd in n for nd in no_decay) and any(nd in n for nd in group1)],'weight_decay': weight_decay, 'lr': enconder_lr/coefficient},
            {'params': [p for n, p in self.model.backbone_name.named_parameters() if not any(nd in n for nd in no_decay) and any(nd in n for nd in group2)],'weight_decay': weight_decay, 'lr': enconder_lr},
            {'params': [p for n, p in self.model.backbone_name.named_parameters() if not any(nd in n for nd in no_decay) and any(nd in n for nd in group3)],'weight_decay': weight_decay, 'lr': enconder_lr*coefficient},
            {'params': [p for n, p in self.model.backbone_name.named_parameters() if any(nd in n for nd in no_decay) and not any(nd in n for nd in group_all)],'weight_decay': 0.0},
            {'params': [p for n, p in self.model.backbone_name.named_parameters() if any(nd in n for nd in no_decay) and any(nd in n for nd in group1)],'weight_decay': 0.0, 'lr': enconder_lr/coefficient},
            {'params': [p for n, p in self.model.backbone_name.named_parameters() if any(nd in n for nd in no_decay) and any(nd in n for nd in group2)],'weight_decay': 0.0, 'lr': enconder_lr},
            {'params': [p for n, p in self.model.backbone_name.named_parameters() if any(nd in n for nd in no_decay) and any(nd in n for nd in group3)],'weight_decay': 0.0, 'lr': enconder_lr*coefficient},
            {'params': [p for n, p in self.model.named_parameters() if backbone_name not in n], 'lr':deconder_lr, "momentum":momentum},
        ]
        return optimizer_parameters













