# An Gentle Introduction to Generatvie Adeverisal Network(GAN)

In this tutorial I will introduce GAN from different perspectives by proposing and answering questions.

## First, Why GAN?

GAN is a creative network that facilitate a number of interesting and valuable applciations in recent years. Tranditional model takes a input and output a fixed output. The output will be the same long as the input is fixed. While GAN can output different results even we give the same input. You may ask, how is that a big deal? well, The creativity makes GAN the most exicting and interesting application in AI. You have seen a lots funny apps that is based on GAN. For example, style transfer. You can input your selfie and GAN would translate it to the animated version fo you. Or transfer a horse image to zebra. I will talk about this more later.

Without further ado, let’s dive into the world of GAN!

## what is GAN?

well, the underlaying principle is super simple and intuitive. If you are a basketball player that really want to play a game. You asked your coach, and he said:”no, you are way out of the league.” So you have to practice ten hours a day like Kobe. A week later, you ask your coach again. This time he notice your improvement but still refuse your request. But he said:” practice harder, young man. ” You did not give up. A mouth later, he finally notice your skills. You got to play.

The training process of the player get him strong. And that is how GAN get trained. By training and improving to make the coach recognize him.

Take Anime Face Generation as an example. The goal is to generate animate picture.

The GAN consists of two parts: generator and discriminator. Generator takes a low-dim vector that sampled from normal distribution and genderate a animate picture. The Discriminator takes pictures from animate image database and generated pictures. Its goal is to identify if the input image if generated. If it is true image, output 1. Otherwise, output 0. Once the generator is smart enough, the genderated image can fool the discriminator to believe its true animate image. 

You can find that the generator and disciminator are compete. That is the term adversarial comes from.

## What is the training algorithm?

![image-20211019180628205](An%20Introduction%20to%20GAN.assets/image-20211019180628205.png)

initialize Generator (G) and Discriminator (D).

For each interation:

- fix generator G, update discriminator D.
-  fix D, update G.

 

This is the genderated results using state-of-the-art GAN.

![image-20211019180818475](An%20Introduction%20to%20GAN.assets/image-20211019180818475.png)

## What is the theory behind GAN?

We know that the real animate images are from a very complex distribution. While we merely sample a vetor from a normal distribuition. Why does this work?   The answer is generator. Generator can transorm a normal distribution to the image distribution.

We use Pg denoting the generated distribution and Pdata denoting the distribution of data.

![image-20211019181548873](An%20Introduction%20to%20GAN.assets/image-20211019181548873.png)

Our goal is to make Pg and Pdata as close as possible.

Formally,


$$
G^* = arg \min Div(P_G,P_{data})
$$
Div is a measurement that calliberate the distance between the two distribution.

However the distribution of Generator output and data are unknown, so the Diversity is hard to calculate.

For discriminator, the goal is to classify if the image is generated.

So cross entropy loss are used as the criterion.

![image-20211019182125408](An%20Introduction%20to%20GAN.assets/image-20211019182125408.png)

The ultimate criterion as shown below, which indicating that we need find a discriminator that are capable of classify if an input is generated. On top of this discriminator, we can train a generator to fool it. However, It is a hard optimization problem. So the practical solution is train each part few epochs and switch to another.  

![image-20211019182242457](An%20Introduction%20to%20GAN.assets/image-20211019182242457.png)



## JS divergence is suitable for GAN?

In most cases, Pg and Pdata are not overlapped.

Because they are low-dim manifold in high-dim space.

Even though they have overlap. If you can not sample enough data... 

![image-20211019223657177](An%20Introduction%20to%20GAN.assets/image-20211019223657177.png)

What is the problem of JS divergence?

JS divergence is always log2 if two distribuition do not overlap.

![image-20211019223721367](An%20Introduction%20to%20GAN.assets/image-20211019223721367.png)

If the two distribution do not overlap, the classifer achieves 100% accuracy. But this means nothing for training generator.

## Wasserstein distance

![image-20211019223929834](An%20Introduction%20to%20GAN.assets/image-20211019223929834.png)

![image-20211019223949926](An%20Introduction%20to%20GAN.assets/image-20211019223949926.png)

![image-20211019224336579](An%20Introduction%20to%20GAN.assets/image-20211019224336579.png)

![image-20211020121101183](An%20Introduction%20to%20GAN.assets/image-20211020121101183.png)

![image-20211020121108150](An%20Introduction%20to%20GAN.assets/image-20211020121108150.png)

## GAN for sequecne generation?

The same as image, we can ask the generator to ouput a sequence and further evaluated by discriminator.

The problem, however, here is the genderated sentence is sampled  from a probability distribution,  the process is not differentiable.

![image-20211020121259654](An%20Introduction%20to%20GAN.assets/image-20211020121259654.png)

A solution is use RL.

 ![image-20211020121545485](An%20Introduction%20to%20GAN.assets/image-20211020121545485.png)



![image-20211020121934821](An%20Introduction%20to%20GAN.assets/image-20211020121934821.png)



## Other posible solution to train a generator?

We can assign a vector **v** to each image **i** and force the generator to output a image  that is close to **i** given input vector. This is the supervised manner.

![image-20211020122149528](An%20Introduction%20to%20GAN.assets/image-20211020122149528.png)

However, directly training the genderator in such method would not have promising results.

The two papers may have better implmentation.

> Generative Latent Optimization (GLO), https://arxiv.org/abs/1707.05776 
>
> Gradient Origin Networks, https://arxiv.org/abs/2007.02798

## Ask the model to generate what you want? -Conditional Generation

An interesting application is Text-to-Image. You can input a text and the model will geneate a corresponding image.

For example, you can ask the mode lto generate a red eyes image. 

![image-20211020122653450](An%20Introduction%20to%20GAN.assets/image-20211020122653450.png) 

For the generator, it takes two input: a text and a vector, and output a image that is corresponded to your text.

While the discriminator have not only to identify if the input image is fake but aslo if it corresponds to the text.

Thus, the output of discriminator should be 1 if it real image and corresponds to the text. 

Other two cases would be: 1. the image is fake. 2. the image is real but do not correspond to the text.

This idea behind the Conditional GAN can do a lots of cool things. Except for text, you can serve a image as a condition. Like generate a photo based on a draft.

Or colorize a image based on grey image. Even generate a image based on the sound.

![image-20211020123740858](An%20Introduction%20to%20GAN.assets/image-20211020123740858.png)

![image-20211020124101774](An%20Introduction%20to%20GAN.assets/image-20211020124101774.png)

Conditional GAN has a condition that ask generator to output what you want. Thus you have to tell the model that the relationship between condition and generated data by pairing data and condition. Except for the postive samples, you also need to mis-pair some samples (the image do not correspond to the condition) and ask the discriminator to classify them as 0 (mis-match).

## Pairing data requires extra resources, Can model learn from unpaired data?

If we want to transform the selfie of a person to the animate version,  we must tell the model the paired relationship. This requires extra resources. Can we do it in unsupervised manner? Absolutely.

![image-20211020174558991](An%20Introduction%20to%20GAN.assets/image-20211020174558991.png)

Formally, the problem is transform a domain x to domain way in an unsupervised manner.

The genderator takes in a data from domain X and generate a output that is similar to domain y.

The Discriminator need to classify if the input data is from domain y or not.

![image-20211020175137312](An%20Introduction%20to%20GAN.assets/image-20211020175137312.png)

A bad case is: the generator output a data that is close to doamin Y but completely unrelated to domain X. 

To handle this issue, we must add a constraint that foceses the generated data close to input.

Cycle GAN have a very clever idea that uses another generator that takes the generated data to re-generate the original input.

![image-20211020175559500](An%20Introduction%20to%20GAN.assets/image-20211020175559500.png)

## Any funny applications of GAN?

Use your imagine, Cycle GAN can do anything. 

For example, transfer a negtive sentence to postive. As long as you input a negtive sentence, and use a postive sentence database. You can ask the model to genderate a postive sentence based on your negtive sentence and reconstruct it to negtive one. 

![image-20211020180333454](An%20Introduction%20to%20GAN.assets/image-20211020180333454.png)

![image-20211020175908535](An%20Introduction%20to%20GAN.assets/image-20211020175908535.png)



![image-20211020180536350](An%20Introduction%20to%20GAN.assets/image-20211020180536350.png)



## How to evaluate a GAN?

A more specific question is: how to evlauate the quality of generated images?

Use a off-the-shelf image classifer to classify the generated image and evaluate how concentrated the output class distribution is.

![image-20211020180803460](An%20Introduction%20to%20GAN.assets/image-20211020180803460.png)

Another aspect is diversity. We want the generator can generate diverse images.

Mode dropping is a long-standing problem for GAN. The output image will turn to similar after iterations. Because model are very lazy.

![image-20211020181808949](An%20Introduction%20to%20GAN.assets/image-20211020181808949.png)

![image-20211020181012998](An%20Introduction%20to%20GAN.assets/image-20211020181012998.png)



how to evaluate diversity?

The same as before, we use a off-the -shelf model to classify the generated image. Then average the probability distribution of each class to get a overall distribution. If it is concentrated, meaning low diversity. And uniform means higher divesity. Note this is not contradicted to qualify evaluation. Because Diversity is evaluated over all samples. While quality is for a single image.



![image-20211020181909097](An%20Introduction%20to%20GAN.assets/image-20211020181909097.png)

**Inception Score (IS):** 

 Good quality, large diversity → Large IS

However, there still exists a problem. IS use inception network as the classifer. If we are trying to generate animate image, no matter what we feed in the classifier, it always output the class of person.  This is biased.  We may need a classifier that is trained in a so large dataset that it can recoginize all kinds of animate images, which is impossible.

A better solution is  Fréchet Inception Distance (FID), which measure the distribution distance between generated image and real images. The smaller the distance is, the better the quality of generated images is.

 Specifically, we serve the distribution of generated data and real data as normal distribution (which may not corresponds to the real world). We take the ouput vector as a sample from the distribution. Thus to better model the distribution, we need to sample as much data as we can. ![image-20211020205243764](An%20Introduction%20to%20GAN.assets/image-20211020205243764.png) 

# Conclusion

![image-20211020205310377](An%20Introduction%20to%20GAN.assets/image-20211020205310377.png)



There is a lots to learn about GAN. You may go over a lots of tutorial over and over again.



# Reference

[PowerPoint 簡報 (ntu.edu.tw)](https://speech.ee.ntu.edu.tw/~hylee/ml/ml2021-course-data/gan_v10.pdf)

