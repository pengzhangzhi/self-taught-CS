# Introduction

In this part, I will raise serveral questions of explainable AI and introduce the main contents by answering them.

## First of all, Why we need explainable AI?

Machines now can make accurate predictions and classifications in many task, thought, we are still afraid of using them because of its intricate behaviors. In many real world applications, in addition, we do need to explain the behaviors of model. For example, if a self-driving car suddently acts abnormally, we need to find the reasons. The medical diagnal results should be responsible to patients.

## Interpretable V.S. Explainable, what is the difference?

Interpretable is for some thing that we need its underlaying priciples, while explainable is for those we can understand and trying to figure out a reasonable explainations for their behaviors.

## Interpretable v.s. Powerful, The compromise?

Most existing model in machine learning is interpretable but simple like linear model. While shopisiticated models like deep neural network are exremely black-box. We aspire more powerful tools to help us, thus explaining complex model in the path that we would like to step on.

![image-20211016130131618](Explainable%20AI.assets/image-20211016130131618.png)

## What is the goals of explainable AI?

Trying to figure out a explaination (reason) that satisfy your boss, customers, or readers of your paper.

Completely understand Deep neural network(interpretable AI) is a long journey. I am personally pessimistic about it. 

On the postive side, we do not know how brains works, but we still trust our brains.

# Explainable AI

![image-20211016131233826](Explainable%20AI.assets/image-20211016131233826.png)

### Local explaination

Explain why do you think this image is a cat.

#### Which component is critical for the model to make decision?

For a input image  consisting of pixel components, which pixel is helpful for the model to classify?

We can remove a component, and see its influence to the model output.

we add a increment in a component Xn, add compute the influence on the output e.

![image-20211016131520375](Explainable%20AI.assets/image-20211016131520375.png)

![image-20211016131618289](Explainable%20AI.assets/image-20211016131618289.png)

This term above reflect how much influence a component can cause to the output.

By computing this term for every component, we can get the saliency map.

![image-20211016131710349](Explainable%20AI.assets/image-20211016131710349.png)

> Karen Simonyan, Andrea Vedaldi, Andrew Zisserman, “Deep Inside Convolutional  Networks: Visualising Image Classification Models and Saliency Maps”, ICLR, 2014

#### Limitations: Noisy Gradient

Often time, we would get the saliency map like this below.

![image-20211016131915597](Explainable%20AI.assets/image-20211016131915597.png)

To get a prettier map, we can argument the input image and compute the saliency map of the argumented maps and average them.

#### Limitation: Gradient Saturation

Gradient cannot always reflect importance. In some cases, the gradient is Saturated, close to 0.

![image-20211016132208448](Explainable%20AI.assets/image-20211016132208448.png)

> Alternative: Integrated gradient (IG)  https://arxiv.org/abs/1611.02639

### Visualization: How a network processes the input data?

We can reduce the dimension (PCA or t-SNE) of neuron’s outputs and visualize it.

As shown in the figure below, on the left is the visualized raw data and the right is the the output of hidden layer. We can easily observe that the hidden embedding has more distinguishable features.

![image-20211016183751475](Explainable%20AI.assets/image-20211016183751475.png)

#### Another techqinues is probing.

we can incorperate another module that take advantage of hidden layer output(embedings) to accomplish other tasks. 

The performances on those tasks can demostrate some special properties of embeddings.

![image-20211016184219198](Explainable%20AI.assets/image-20211016184219198.png)

### Global Explaination

Explain what does a cat looks like?

#### What does a filtet detect?

The filters of CNN can detect some patterns, but what is the exact shape?

![image-20211016184802171](Explainable%20AI.assets/image-20211016184802171.png)

We can compute the X that maximize the filter parameters.

![image-20211016184927223](Explainable%20AI.assets/image-20211016184927223.png)

That gives un:

![image-20211016184942603](Explainable%20AI.assets/image-20211016184942603.png)

With this idea, we can compute the image that maximize a specific class probability.  Thus we can know what a image looks like from model’s perspective.



![image-20211016185128492](Explainable%20AI.assets/image-20211016185128492.png)

We may need to add some constrain terms (inducive bias) to make them more like what we think.

![image-20211016185210380](Explainable%20AI.assets/image-20211016185210380.png)

![image-20211016185409659](Explainable%20AI.assets/image-20211016185409659.png)

Or we can train a generator that generate a image x with random vector z, and train a classifier to classify it. By maximizing the class we can compute the vector z.

![image-20211016185634005](Explainable%20AI.assets/image-20211016185634005.png)

The generator can help us translate the envision of model  to human-understandable image.

### Distillation?

Using a interpretable model to mimic the behavior of an uninterpretable model and analyze the easy model.

> Local Interpretable Model-Agnostic Explanations (LIME)
>
> https://youtu.be/K1mWgthGS-A
>
> https://youtu.be/OjqIVSwly4k