import torch.nn as nn
from torch.nn.utils import weight_norm


class Chomp1d(nn.Module):
    def __init__(self, chomp_size):
        """Chomp1d

        Source: https://github.com/locuslab/TCN/blob/8845f88f31def1e7ffccb8811ea966e9f58d9695/TCN/tcn.py

        Args:
            chomp_size:
        """
        super(Chomp1d, self).__init__()
        self.chomp_size = chomp_size

    def forward(self, x):
        return x[:, :, :-self.chomp_size].contiguous()


class TemporalBlock(nn.Module):
    def __init__(self, n_inputs, n_outputs, kernel_size, stride, dilation, padding, dropout=0.2):
        """Temporal Block

        Source: https://github.com/locuslab/TCN/blob/8845f88f31def1e7ffccb8811ea966e9f58d9695/TCN/tcn.py

        Args:
            n_inputs:
            n_outputs:
            kernel_size:
            stride:
            dilation:
            padding:
            dropout:
        """
        super(TemporalBlock, self).__init__()
        self.conv1 = weight_norm(nn.Conv1d(n_inputs, n_outputs, kernel_size,
                                           stride=stride, padding=padding, dilation=dilation))
        self.chomp1 = Chomp1d(padding)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(dropout)

        self.conv2 = weight_norm(nn.Conv1d(n_outputs, n_outputs, kernel_size,
                                           stride=stride, padding=padding, dilation=dilation))
        self.chomp2 = Chomp1d(padding)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(dropout)

        self.net = nn.Sequential(self.conv1, self.chomp1, self.relu1, self.dropout1,
                                 self.conv2, self.chomp2, self.relu2, self.dropout2)
        self.downsample = nn.Conv1d(n_inputs, n_outputs, 1) if n_inputs != n_outputs else None
        self.relu = nn.ReLU()
        self.init_weights()

    def init_weights(self):
        self.conv1.weight.data.normal_(0, 0.01)
        self.conv2.weight.data.normal_(0, 0.01)
        if self.downsample is not None:
            self.downsample.weight.data.normal_(0, 0.01)

    def forward(self, x):
        out = self.net(x)
        res = x if self.downsample is None else self.downsample(x)
        return self.relu(out + res)


class TemporalConvNet(nn.Module):
    def __init__(self, num_inputs, num_channels, kernel_size=2, dropout=0.2):
        """Temporal Convolution Network (TCN)

        Source: https://github.com/locuslab/TCN/blob/8845f88f31def1e7ffccb8811ea966e9f58d9695/TCN/tcn.py

        Args:
            num_inputs:
            num_channels:
            kernel_size:
            dropout:
        """
        super(TemporalConvNet, self).__init__()
        layers = []
        num_levels = len(num_channels)
        for i in range(num_levels):
            dilation_size = 2 ** i
            in_channels = num_inputs if i == 0 else num_channels[i - 1]
            out_channels = num_channels[i]
            layers += [TemporalBlock(in_channels, out_channels, kernel_size, stride=1, dilation=dilation_size,
                                     padding=(kernel_size - 1) * dilation_size, dropout=dropout)]

        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)


class TCNAdapterForRNN(TemporalConvNet):
    def __init__(self, input_size, hidden_size, num_layers=2, kernel_size=2, dropout=0.2, rnn_compatibility=True):
        """RNN adapter for TCN

        Allows for drop-in replacement of RNN encoders

        Args:
            input_size (int): input size
            hidden_size (int): hidden size specifying the number of channels per convolutional layer
            num_layers (int): the number of dilated convolutional layers
            kernel_size (int): size of the kernel of each layer
            dropout (float): dropout rate
            rnn_compatibility (bool): should we reshape the inputs and output to retain compatibility with RNN layers?
        """
        num_channels = [hidden_size for _ in range(num_layers)]
        super(TCNAdapterForRNN, self).__init__(input_size, num_channels, kernel_size, dropout)
        self.rnn_compatibility = rnn_compatibility

    def forward(self, x):
        x = x.permute(0, 2, 1) if self.rnn_compatibility else x
        output = self.network(x)
        output = output.permute(0, 2, 1) if self.rnn_compatibility else output
        return output
