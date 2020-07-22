"""
Manipulate Hyperparameter Spaces for Hyperparameter Tuning
===========================================================

This demonstrates how to manipulate hyperparameters and hyperparameter spaces.

..
    Copyright 2019, Neuraxio Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

..
    Thanks to Umaneo Technologies Inc. for their contributions to this Machine Learning
    project, visit https://www.umaneo.com/ for more information on Umaneo Technologies Inc.

"""

from sklearn.decomposition import PCA

from neuraxle.base import Identity
from neuraxle.hyperparams.distributions import RandInt
from neuraxle.hyperparams.space import HyperparameterSpace
from neuraxle.pipeline import Pipeline
from neuraxle.steps.numpy import MultiplyByN


def main():
    p = Pipeline([
        ('step1', MultiplyByN()),
        ('step2', MultiplyByN()),
        Pipeline([
            Identity(),
            Identity(),
            PCA(n_components=4)
        ])
    ])

    p.set_hyperparams_space({
        'step1__multiply_by': RandInt(42, 50),
        'step2__multiply_by': RandInt(-10, 0),
        'Pipeline__PCA__n_components': RandInt(2, 3)
    })

    samples = p.get_hyperparams_space().rvs()
    p.set_hyperparams(samples)

    samples = p.get_hyperparams().to_flat_as_dict_primitive()
    assert 42 <= samples['step1__multiply_by'] <= 50
    assert -10 <= samples['step2__multiply_by'] <= 0
    assert samples['Pipeline__PCA__n_components'] in [2, 3]
    assert p['Pipeline']['PCA'].get_wrapped_sklearn_predictor().n_components in [2, 3]


if __name__ == "__main__":
    main()
