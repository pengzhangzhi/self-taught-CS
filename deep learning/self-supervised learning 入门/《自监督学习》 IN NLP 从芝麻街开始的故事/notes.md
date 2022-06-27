# Overview

two pre-trained models in self-supervised learning

1. BERT
2. GPT

参数量：

![image-20210812211052137](notes.assets/image-20210812211052137.png)

![image-20210812230624450](notes.assets/image-20210812230624450.png)

# Self-supervised learning

![image-20210812211145889](notes.assets/image-20210812211145889.png)

supervised learning： 通过label 提供监督信息。

self-supervised learning： 数据就是监督信息。

# BERT

## **在NLP中如何做self-supervised learning？**

1. ### Masking input（random）

   

   ![image-20210812211421150](notes.assets/image-20210812211421150.png)

#### masking method

- 用一个特殊的token
- 随机选一个其他的词

![image-20210812211441313](notes.assets/image-20210812211441313.png)

![image-20210812211633758](notes.assets/image-20210812211633758.png)

### next sentence prediction

predict if sentence 2 is next sentence. 

![image-20210812211758652](notes.assets/image-20210812211758652.png)

![image-20210812211850687](notes.assets/image-20210812211850687.png)

![image-20210812212050534](notes.assets/image-20210812212050534.png)



BERT are pre-trained with self-supervised learning then transfer to downstream tasks.

![image-20210812213038392](notes.assets/image-20210812213038392.png)



### Benchmark

How to evaluate the performance of pre-trained models?

![image-20210812213131339](notes.assets/image-20210812213131339.png)

BERT and its family:

![image-20210812213315728](notes.assets/image-20210812213315728.png)

### downstream tasks

How to use BERT/ What is the downstream tasks?

Case 1: sentiment analysis

![image-20210812213508479](notes.assets/image-20210812213508479.png)

![image-20210812213533317](notes.assets/image-20210812213533317.png)

结果：对于任意一个模型， fine-tune都能加速收敛，且收敛到更好的结果。

![image-20210812213750486](notes.assets/image-20210812213750486.png)



![image-20210812213913222](notes.assets/image-20210812213913222.png)

predict the relationship between premise and hypothesis.

![image-20210812214157043](notes.assets/image-20210812214157043.png)

![image-20210812214221151](notes.assets/image-20210812214221151.png)

Find a sentence that related to the question.

![image-20210812214328337](notes.assets/image-20210812214328337.png)

output two digits are to point the range of answer.

![image-20210812214612699](notes.assets/image-20210812214612699.png)

use two vectors(begin and end) to map each token to a score which indicating that probability that this is the begin or end.

![image-20210812214905553](notes.assets/image-20210812214905553.png)

![image-20210812215334604](notes.assets/image-20210812215334604.png)

之前train的都是encoder的BERT，能不能pre-train 一个 seq2seq model？

![image-20210812215535980](notes.assets/image-20210812215535980.png)

对input做augmentation， MASS（mask），delete， permutaion，rotation，composition of above 

其实可以做对比学习。

![image-20210812215723662](notes.assets/image-20210812215723662.png)



### Why does BERT WORK?

![image-20210812223449496](notes.assets/image-20210812223449496.png)

The meaning is determined by its context.

![image-20210812223547794](notes.assets/image-20210812223547794.png)

![image-20210812223618810](notes.assets/image-20210812223618810.png)



一个很奇怪的现象，把在语言中训练的BERT用在protein，DNA,Music分类问题上，竟然有效果。

![image-20210812223828002](notes.assets/image-20210812223828002.png)

![image-20210812223948822](notes.assets/image-20210812223948822.png)

在英文任务中训练，竟然在中文数据中test 结果不错。

在muti-languague上pre-train,在 中文和英文上fine-tune 效果最好。

说明不同语言间没有差异，有语义相似性。 BERT就能捕获到这一点。

![image-20210812225055766](notes.assets/image-20210812225055766.png)

![image-20210812224258778](notes.assets/image-20210812224258778.png)

但其中不同语言间肯定会有一些差异，不同embedding中肯定有一些与language 相关的信息来表明这个embedding代表的词是哪种语言。 不然输入中文时如何重建中文而不是其他语言？

![image-20210812224732029](notes.assets/image-20210812224732029.png)

语言的信息在哪？

对所有中文和英文的embedding做average，两者作差得到的向量就是不同语言之间的差距。

![image-20210812225111951](notes.assets/image-20210812225111951.png)

输入英文得到的embedding加上差距后重建得到的就是中文的embedding

![image-20210812225130703](notes.assets/image-20210812225130703.png)

一个英文句子的embedding加上中英差距向量，得到的就是中文的embedding

![image-20210812225232499](notes.assets/image-20210812225232499.png)

# GPT

如何训练？

Predict Next Token

![image-20210812225451076](notes.assets/image-20210812225451076.png)

![image-20210812225633541](notes.assets/image-20210812225633541.png)

Evaluation：

task：

description of task

examples

prompt



![image-20210812225853365](notes.assets/image-20210812225853365.png)

![image-20210812225913855](notes.assets/image-20210812225913855.png)

效果也就那样.....

# 不仅仅是TEXT:

![image-20210812230017330](notes.assets/image-20210812230017330.png)