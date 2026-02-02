from turtle import forward
import torch
import torch.nn as nn
import torch.nn.functional as F
import copy


class ResearchJEPA(nn.Module):
    def __init__(self, input_dim, embed_dim, latent_dim=16):
        super().__init__()
        # Context encoder
        self.context_encoder = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.LayerNorm(512), # Normalization keeps the numbers in the vector from exploding and stable training.
            nn.GELU(),
            nn.Linear(512, embed_dim) # x -> s_{x}
        )

        # Target encoder
        self.target_encoder = copy.deepcopy(self.context_encoder)
        # Freeze target encoder
        for param in self.target_encoder.parameters():
            param.requires_grad = False

        # Predictor
        self.predictor = nn.Sequential(
            nn.Linear(embed_dim + 2 + latent_dim, 512), # context vector + position token (coordinates) + latent variable
            nn.GELU(), # Ussing GELU instead of RELU for smooth probabilistic distribution when calculating gradients, letting some negative values unline RELU which uses only zero for negative values.
            nn.Linear(512, embed_dim)
        )

    @torch.no_grad()
    def update_target_encoder(self, momentum = 0.996):
        """Prevents model collapse, EMA secret sauce"""
        for param_q, param_k in zip(self.context_encoder.parameters(), self.target_encoder.parameters()):
            # Formula, above q is query(weights of context encoder), above k is key(weights of target encoder)
            param_k.data = (param_k * momentum) + (param_q * (1 - momentum))

    def forward(self, x_context, x_target, pos_a):
        s_x = self.context_encoder(x_context) # context vector
        
        with torch.no_grad():
            s_y = self.target_encoder(x_target)

        # latent variable
        z = torch.randn(s_x.size(0), 16).to(s_x.device) # creating a vector of numbers so that it allows the model to learn context from s_x

        # Predictor
        predictor_input = torch.cat([s_x, pos_a, z], dim=-1)

        # Guess
        s_y_tilde = self.predictor(predictor_input)

        return s_y_tilde, s_y


# TRAINING LOOP
model = ResearchJEPA(input_dim=784, embed_dim=128)
optimizer = torch.optim.AdamW(model.context_encoder.parameters(), lr=1e-4)



batch_size = 32
x_context = torch.randn(batch_size, 784)
x_target = torch.randn(batch_size, 784)
pos_a = torch.randn(batch_size, 2)

# Forward Pass
s_y_tilde, s_y = model(x_context, x_target, pos_a)

# Predictor (D(s_y, s_y_tilde))
loss = F.mse_loss(s_y_tilde, s_y)

# Backprogation
loss.backward()
optimizer.step()

# Update teacher
model.update_target_encoder()





