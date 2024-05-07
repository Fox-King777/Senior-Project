"""
Optimizers for neural network training
"""

# pylint: disable=E1101, C0200
from typing import List
import autograd.numpy as np
from autograd import grad
from neural_network import NeuralNetwork
from loss_function import mse_loss_function
from training_utility import print_loss, plot_loss


def gradient_descent(
    t: np.array, neural_networks: List[NeuralNetwork], num_iters: int, learn_rate: float
):
    """Runs gradient descent for a given number of iterations

    Args:
        t: The input vector
        num_iters: The number of iterations
        learn_rate: The learning rate

    Returns:
        neural_networks: A list of neural networks after gradient descent
    """
    loss_grad_function = grad(mse_loss_function, 2)
    loss = [0] * num_iters
    for i in range(num_iters):
        weights_list = [neural_networks[j].weights for j in range(len(neural_networks))]
        loss[i] = print_loss(t, neural_networks, weights_list, i, loss[i - 1])

        loss_grad = loss_grad_function(t, neural_networks, weights_list)
        for j in range(len(neural_networks)):
            for k in range(len(neural_networks[j].weights)):
                neural_networks[j].weights[k] = (
                    neural_networks[j].weights[k] - learn_rate * loss_grad[j][k]
                )

    plot_loss(num_iters, loss)

    return neural_networks


def adam(
    t, neural_networks, num_iters=10000, step_size=0.001, b1=0.9, b2=0.999, eps=10**-8
):
    """Runs adam for a given number of iterations

    Args:
        t: The input vector
        num_iters: The number of iterations
        step_size: The step size per iteration

    Returns:
        neural_networks: A list of neural networks after running adam
    """
    loss_grad_function = grad(mse_loss_function, 2)

    m = [
        [
            np.zeros_like(neural_networks[i].weights[j])
            for j in range(len(neural_networks[0].weights))
        ]
        for i in range(len(neural_networks))
    ]
    v = [
        [
            np.zeros_like(neural_networks[i].weights[j])
            for j in range(len(neural_networks[0].weights))
        ]
        for i in range(len(neural_networks))
    ]

    mhat = [
        [None] * len(neural_networks[i].weights) for i in range(len(neural_networks))
    ]
    vhat = [
        [None] * len(neural_networks[i].weights) for i in range(len(neural_networks))
    ]

    loss = [0] * num_iters
    for i in range(num_iters):
        weights_list = [neural_networks[j].weights for j in range(len(neural_networks))]
        loss[i] = print_loss(t, neural_networks, weights_list, i, loss[i - 1])

        g = loss_grad_function(t, neural_networks, weights_list)
        for j in range(len(neural_networks)):
            for k in range(len(neural_networks[j].weights)):
                # First  moment estimate.
                m[j][k] = (1 - b1) * g[j][k] + b1 * m[j][k]
                # Second moment estimate.
                v[j][k] = (1 - b2) * (g[j][k] ** 2) + b2 * v[j][k]

                # Bias correction.
                mhat[j][k] = m[j][k] / (1 - b1 ** (i + 1))
                vhat[j][k] = v[j][k] / (1 - b2 ** (i + 1))
                neural_networks[j].weights[k] = neural_networks[j].weights[
                    k
                ] - step_size * mhat[j][k] / (np.sqrt(vhat[j][k]) + eps)

    plot_loss(num_iters, loss)

    return neural_networks
