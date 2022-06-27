# transformer and its variants review

focuses:

- background:

- contribution / conclusion
- method
- experiments

## references:

Early Convolutions Help Transformers See Better

Escaping the Big Data Paradigm with Compact Transformers

Tokens-to-Token ViT: Training Vision Transformers from Scratch on ImageNet

CvT: Introducing Convolutions to Vision Transformers

[lucidrains/vit-pytorch: Implementation of Vision Transformer, a simple way to achieve SOTA in vision classification with only a single transformer encoder, in Pytorch (github.com)](https://github.com/lucidrains/vit-pytorch)

## Go Wider Instead of Deeper

### background:

To improve the effectiveness and efficiency of the transformer, there are two trains of thought
among existing works: 

(1) going wider by scaling to more trainable parameters;

replace part of the feed-forward network (FFN) layer in transformer blocks with MoE layers.

 (2) going shallower by parameter sharing or model compressing along with the depth.

### Contribution:

The two trains of thoughts are achieved in one Network. WideNet employs parameter sharing along with depth and uses mixture-of-experts (MoE) to extend trainable parameters along the width. Specially, we use the same MoE layer in all transformer blocks. The multi-head attention layer is also shared across transformer blocks in WideNet. Therefore, the trainable parameters of WideNet go wider by MoE layers and become shallower by parameter sharing across transformer blocks.

### Method:

![image-20210803091316928](transformer%20and%20variants%20review.assets/image-20210803091316928.png)

#### MoE：

![image-20210803092456363](transformer%20and%20variants%20review.assets/image-20210803092456363.png)

![image-20210803092615867](transformer%20and%20variants%20review.assets/image-20210803092615867.png)

Inherent problem of Softmax:

![image-20210803093105187](transformer%20and%20variants%20review.assets/image-20210803093105187.png)

![img](transformer%20and%20variants%20review.assets/v2-1d7ef7b8fb59a925470dc52218b43117_720w.jpg)

可以看到，数量级对softmax得到的分布影响非常大。**在数量级较大时，softmax将几乎全部的概率分布都分配给了最大值对应的标签**。

When a is large enough, the output distribution will be : [1,0,0]

![image-20210803094109184](transformer%20and%20variants%20review.assets/image-20210803094109184.png)



Most expert receive few tokens.

use a differentiable load balance loss to force the model evenly assigning tokens to experts. For each routing operation, given E experts and N batches with NL tokens, the following auxiliary loss is added to the total model loss during training:

![image-20210803103150611](transformer%20and%20variants%20review.assets/image-20210803103150611.png)

![image-20210803145534693](transformer%20and%20variants%20review.assets/image-20210803145534693.png)

### Sharing MoE across transformer blocks

### Individual Layer Normalization

### Experiments:

#### result:

ImageNet-1K

![image-20210803145744165](transformer%20and%20variants%20review.assets/image-20210803145744165.png)

![image-20210803145757508](transformer%20and%20variants%20review.assets/image-20210803145757508.png)

![image-20210803150813232](transformer%20and%20variants%20review.assets/image-20210803150813232.png)

more experts (trainable parameters) lead to overfitting although more experts mean stronger modeling capacity.

Training accuracy is lower than testing accuracy because of data augmentation we introduced in the Experimental Settings Section.

#### Ablation:

![image-20210803150925453](transformer%20and%20variants%20review.assets/image-20210803150925453.png)

W/O: without

#### Routing:

![image-20210803152313147](transformer%20and%20variants%20review.assets/image-20210803152313147.png)

fewer groups, which means we have fewer routing operations, there is an obvious performance drop.

#### Performance:

![image-20210803152354562](transformer%20and%20variants%20review.assets/image-20210803152354562.png)

computation expensive.

Reference:

Shazeer, N.; Mirhoseini, A.; Maziarz, K.; Davis, A.; Le, Q.;Hinton, G.; and Dean, J. 2017. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. arXiv preprint arXiv:1701.06538




https://www.zhihu.com/question/339723385/answer/782509914



### Summary:

What is the contribution? Fusion of two method: MoE and shared parameters to achieve parameter effciency.

Tranditional approaches to tackle the inbanlced distribution of Softmax is to rescale the output to a small range, where the value is evenly distributed. While in this paper, they use a loss term to balance the inbalance.

MoE can adptively select experts to process tokens, each forward will select different experts. That is each forward will generate a different sub-models,  the final model is the ensemble of multiple sub-model.  Each forward will dynamically activate and drop parts of modules to generate a sub-model. The same idea have been proposed in Dropout and ResNet. The is another way to achieve regularization.

