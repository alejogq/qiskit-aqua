# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

from qiskit_aqua.components.optimizers import Optimizer
from ._nloptimizer import minimize
from ._nloptimizer import check_pluggable_valid as check_nlopt_valid
import logging

logger = logging.getLogger(__name__)

try:
    import nlopt
except ImportError:
    logger.info('nlopt is not installed. Please install it if you want to use them.')


class CRS(Optimizer):
    """Controlled Random Search (CRS) with local mutation.

    NLopt global optimizer, derivative-free
    https://nlopt.readthedocs.io/en/latest/NLopt_Algorithms/#controlled-random-search-crs-with-local-mutation
    """

    CONFIGURATION = {
        'name': 'CRS',
        'description': 'GN_CRS2_LM Optimizer',
        'input_schema': {
            '$schema': 'http://json-schema.org/schema#',
            'id': 'crs_schema',
            'type': 'object',
            'properties': {
                'max_evals': {
                    'type': 'integer',
                    'default': 1000
                }
            },
            'additionalProperties': False
        },
        'support_level': {
            'gradient': Optimizer.SupportLevel.ignored,
            'bounds': Optimizer.SupportLevel.supported,
            'initial_point': Optimizer.SupportLevel.required
        },
        'options': ['max_evals'],
        'optimizer': ['global']
    }

    def __init__(self):
        super().__init__()

    @staticmethod
    def check_pluggable_valid():
        check_nlopt_valid(CRS.CONFIGURATION['name'])

    def optimize(self, num_vars, objective_function, gradient_function=None,
                 variable_bounds=None, initial_point=None):
        super().optimize(num_vars, objective_function, gradient_function, variable_bounds, initial_point)

        return minimize(nlopt.GN_CRS2_LM, objective_function, variable_bounds, initial_point, **self._options)
