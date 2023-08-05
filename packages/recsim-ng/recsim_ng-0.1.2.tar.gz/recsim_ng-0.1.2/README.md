# RecSim NG: Toward Principled Uncertainty Modeling for Recommender Ecosystems

RecSim NG, a probabilistic platform for multi-agent recommender systems
simulation. RecSimNG is a scalable, modular, differentiable simulator
implemented in Edward2 and TensorFlow. It offers: a powerful, general
probabilistic programming language for agent-behavior specification; an
XLA-based vectorized execution model for running simulations on accelerated
hardware; and tools for probabilistic inference and latent-variable model
learning, backed by automatic differentiation and tracing. We describe RecSim NG
and illustrate how it can be used to create transparent, configurable,
end-to-end models of a recommender ecosystem. Specifically, we present a
collection of use cases that demonstrate how the functionality described above
can help both researchers and practitioners easily develop and train novel
algorithms for recommender systems. Please refer to
[Mladenov et al](https://arxiv.org/abs/2103.08057) for the
high-level design of RecSim NG. Please cite the paper if you use the code from
this repository in your work.

### Bibtex

```
@article{mladenov2021recsimng,
    title = {RecSim {NG}: Toward Principled Uncertainty Modeling for Recommender Ecosystems},
    author = {Martin Mladenov, Chih-Wei Hsu, Vihan Jain, Eugene Ie, Christopher Colby, Nicolas Mayoraz, Hubert Pham, Dustin Tran, Ivan Vendrov, Craig Boutilier}
    year = {2021},
    eprint={2103.08057},
    archivePrefix={arXiv},
    primaryClass={cs.LG}
}
```

<a id='Disclaimer'></a>

## Disclaimer

This is not an officially supported Google product.

## Installation and Sample Usage

It is recommended to install RecSim NG using
(https://pypi.org/project/recsim_ng).

```shell
pip install recsim_ng
```

Here are some sample commands you could use for testing the installation:

```
git clone https://github.com/google-research/recsim_ng
cd recsim_ng/recsim_ng/applications/ecosystem_simulation
python ecosystem_simulation_demo.py
```

## Tutorials

To get started, please check out our Colab tutorials. In
[**RecSim NG: Basics**](https://colab.research.google.com/github/google-research/recsim_ng/blob/master/recsim_ng/colab/RecSim_NG_Basics.ipynb),
we introduce the RecSim NG model and corresponding modeling APIs and runtime
library. We then demonstrate how we define a simulation using **entities**,
**behaviors**, and **stories**. Finally, we illustrate differentiable
simulation including model learning and inference.

In [**RecSim NG: Dealing With Uncertainty**](https://colab.research.google.com/github/google-research/recsim_ng/blob/master/recsim_ng/colab/RecSim_NG_Dealing_With_Uncertainty.ipynb),
we explicitly address the stochastics of the Markov process captured by a DBN.
We demonstrate how to use Edward2 in RecSim NG and show how to use the
corresponding RecSim NG APIs for inference and learning tasks. Finally, we
showcase how the uncertainty APIs of RecSim NG can be used within a
recommender-system model-learning application.

## Documentation


Please refer to the [white paper](https://arxiv.org/abs/2103.08057)
for the high-level design.
