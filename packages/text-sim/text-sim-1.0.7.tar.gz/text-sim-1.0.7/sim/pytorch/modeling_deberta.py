#! -*- coding: utf-8 -*-
""" Pytorch DeBERTa Common Modules
"""
# Author: DengBoCong <bocongdeng@gmail.com>
#
# License: MIT License

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import torch
import torch.nn as nn
from sim.pytorch.common import truncated_normal_
from typing import Any


class BertEmbeddings(nn.Module):
    """Bert Embedding
    """

    def __init__(self,
                 hidden_size: int,
                 embedding_size: int,
                 hidden_dropout_prob: float = None,
                 shared_segment_embeddings: bool = False,
                 max_position: int = None,
                 position_merge_mode: str = "add",
                 hierarchical_position: Any = None,
                 type_vocab_size: int = None,
                 layer_norm_eps: float = None,
                 initializer: Any = truncated_normal_(),
                 position_ids: Any = None):
        """Bert Embedding
        :param hidden_size: 编码维度
        :param embedding_size: 词嵌入大小
        :param hidden_dropout_prob: Dropout比例
        :param shared_segment_embeddings: 若True，则segment跟token共用embedding
        :param max_position: 绝对位置编码最大位置数
        :param position_merge_mode: 输入和position合并的方式
        :param hierarchical_position: 是否层次分解位置编码
        :param type_vocab_size: segment总数目
        :param layer_norm_eps: layer norm 附加因子，避免除零
        :param initializer: Embedding的初始化器
        :param position_ids: 位置编码ids
        """
        super(BertEmbeddings, self).__init__()
        self.hidden_size = hidden_size
        self.embedding_size = embedding_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.shared_segment_embeddings = shared_segment_embeddings
        self.max_position = max_position
        self.position_merge_mode = position_merge_mode
        self.hierarchical_position = hierarchical_position
        self.type_vocab_size = type_vocab_size
        self.layer_norm_eps = layer_norm_eps
        self.initializer = initializer
        self.position_ids = position_ids

        if self.type_vocab_size > 0 and not self.shared_segment_embeddings:
            self.segment_embeddings = nn.Embedding(
                num_embeddings=self.type_vocab_size,
                embedding_dim=self.embedding_size
            )
            self.initializer(self.segment_embeddings.weight)

        self.position_embeddings = PositionEmbedding(
            input_dim=self.max_position,
            output_dim=self.embedding_size,
            merge_mode=self.position_merge_mode,
            hierarchical=self.hierarchical_position,
            custom_position_ids=self.position_ids is not None,
            initializer=self.initializer
        )

        self.layer_norm = nn.LayerNorm(normalized_shape=self.embedding_size, eps=self.layer_norm_eps)
        self.dropout = nn.Dropout(p=self.hidden_dropout_prob)

        if self.embedding_size != self.hidden_size:
            self.outputs_dense = nn.Linear(in_features=self.embedding_size, out_features=self.hidden_size)

    def forward(self, input_ids, segment_ids, token_embeddings):
        outputs = token_embeddings(input_ids)

        if self.type_vocab_size > 0:
            if self.shared_segment_embeddings:
                segment_outputs = token_embeddings(segment_ids)
            else:
                segment_outputs = self.segment_embeddings(segment_ids)

            outputs = outputs + segment_outputs

        if self.position_ids is None:
            outputs = self.position_embeddings(outputs)
        else:
            outputs = self.position_embeddings([outputs, self.position_ids])

        outputs = self.layer_norm(outputs)
        outputs = self.dropout(outputs)

        if self.embedding_size != self.hidden_size:
            outputs = self.outputs_dense(outputs)

        return outputs

