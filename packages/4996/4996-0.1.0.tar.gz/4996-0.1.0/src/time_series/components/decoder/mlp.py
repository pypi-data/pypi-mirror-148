import torch.nn as nn
import numpy as np


class MLP(nn.Module):

    def __init__(self, input_size, hidden_size, output_size, num_layers=2, dropout=0.1, activation=nn.ReLU):
        """Multi-Layer Perceptron

        Allows for a variable number of layers (default=2).

        Args:
            input_size (int): inputs size of the first layer
            hidden_size (int): hidden size of the intermediate layers
            output_size (int): output size of the final layer
            num_layers (int): number of layers in the MLP
            dropout (float): dropout rate
            activation (nn.Module): an activation module that can be initialized
        """
        super(MLP, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.activation = activation()

        layers = []
        for k in np.arange(num_layers) + 1:
            input_size, output_size = self.hidden_size, self.hidden_size
            activation = self.activation

            if k == 1:
                input_size = self.input_size

            if k == self.num_layers:
                output_size = self.output_size
                activation = nn.Identity()

            layer = nn.Linear(input_size, output_size)
            layers.append(layer)
            layers.append(activation)
            layers.append(nn.Dropout(self.dropout))

        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        """ Forward pass

        Args:
            x (nn.Tensor): a tensors of inputs

        Returns:
            a nn.Tensor with `output_size` number of outputs

        """

        return self.layers(x)
