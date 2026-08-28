from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class BatchTopKSAE(nn.Module):
    def __init__(
        self,
        d_in: int,
        d_sae: int,
        k: int,
        b_dec_init: torch.Tensor,
        apply_decoder_bias_to_input: bool = True,
    ):
        super().__init__()

        self.d_in = int(d_in)
        self.d_sae = int(d_sae)
        self.k = int(k)

        self.apply_decoder_bias_to_input = bool(
            apply_decoder_bias_to_input
        )

        W_dec = torch.randn(
            self.d_sae,
            self.d_in,
            dtype=torch.float32,
        )

        W_dec = F.normalize(
            W_dec,
            dim=1,
        )

        self.W_dec = nn.Parameter(W_dec)

        self.W_enc = nn.Parameter(
            W_dec.t().contiguous().clone()
        )

        self.b_enc = nn.Parameter(
            torch.zeros(
                self.d_sae,
                dtype=torch.float32,
            )
        )

        self.b_dec = nn.Parameter(
            b_dec_init.detach().float().clone()
        )

    def raw_activations(
        self,
        x: torch.Tensor,
    ) -> torch.Tensor:
        if self.apply_decoder_bias_to_input:
            x_enc = x - self.b_dec
        else:
            x_enc = x

        pre = (
            x_enc @ self.W_enc
            + self.b_enc
        )

        return F.relu(pre)

    def batch_topk(
        self,
        raw: torch.Tensor,
    ):
        batch_size = raw.shape[0]

        flat = raw.flatten()

        n_keep = min(
            self.k * batch_size,
            flat.numel(),
        )

        values, indices = torch.topk(
            flat,
            n_keep,
            sorted=False,
        )

        sparse = torch.zeros_like(flat)

        sparse.scatter_(
            0,
            indices,
            values,
        )

        sparse = sparse.view_as(raw)

        cutoff = (
            values.min()
            if values.numel()
            else raw.new_tensor(0.0)
        )

        return sparse, cutoff

    def encode(
        self,
        x: torch.Tensor,
    ):
        raw = self.raw_activations(x)

        acts, cutoff = self.batch_topk(raw)

        return acts, raw, cutoff

    def decode(
        self,
        acts: torch.Tensor,
    ):
        return (
            acts @ self.W_dec
            + self.b_dec
        )

    def forward(
        self,
        x: torch.Tensor,
    ):
        acts, raw, cutoff = self.encode(x)

        recon = self.decode(acts)

        return (
            recon,
            acts,
            raw,
            cutoff,
        )

    def auxiliary_loss(
        self,
        x: torch.Tensor,
        recon: torch.Tensor,
        raw: torch.Tensor,
        dead_mask: torch.Tensor,
        aux_k: int,
        aux_penalty: float,
    ):
        n_dead = int(
            dead_mask.sum().item()
        )

        if n_dead == 0:
            return x.new_tensor(0.0)

        dead_raw = raw[:, dead_mask]

        k_aux = min(
            int(aux_k),
            n_dead,
        )

        if k_aux <= 0:
            return x.new_tensor(0.0)

        values, indices = torch.topk(
            dead_raw,
            k_aux,
            dim=-1,
            sorted=False,
        )

        aux_acts = torch.zeros_like(
            dead_raw
        )

        aux_acts.scatter_(
            -1,
            indices,
            values,
        )

        aux_recon = (
            aux_acts
            @ self.W_dec[dead_mask]
        )

        residual = x - recon

        aux_loss = (
            aux_recon.float()
            - residual.float()
        ).pow(2).sum(
            dim=-1
        ).mean()

        return (
            float(aux_penalty)
            * aux_loss
        )

    @torch.no_grad()
    def normalize_decoder_(self):
        self.W_dec.data = F.normalize(
            self.W_dec.data,
            dim=1,
        )

    @torch.no_grad()
    def remove_decoder_grad_parallel_(self):
        if self.W_dec.grad is None:
            return

        w = F.normalize(
            self.W_dec.data,
            dim=1,
        )

        g = self.W_dec.grad

        parallel = (
            (g * w)
            .sum(
                dim=1,
                keepdim=True,
            )
            * w
        )

        g.sub_(parallel)
