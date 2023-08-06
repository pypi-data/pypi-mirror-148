# -*- coding: utf-8 -*-
# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Parameter resolver."""

import json
from collections.abc import Iterable
from copy import deepcopy
import numpy as np
import sympy as sp
from mindquantum import mqbackend as mb
from mindquantum.utils.type_value_check import _num_type
from mindquantum.utils.type_value_check import _check_input_type
from mindquantum.utils.type_value_check import _check_int_type


class ParameterResolver(dict):
    """
    A ParameterRsolver can set the parameter of parameterized quantum gate or
    parameterized quantum circuit.

    By specific which part of parameters needs to calculate gradient, the PQC
    operator can only calculate gradient of these parameters.

    Args:
        data (dict): initial parameter names and its values. Default: None.

    Examples:
        >>> from mindquantum.core import ParameterResolver
        >>> pr = ParameterResolver({'a': 0.3})
        >>> pr['b'] = 0.5
        >>> pr.no_grad_part('a')
        {'a': 0.3, 'b': 0.5}
        >>> pr *= 2
        >>> pr
        {'a': 0.6, 'b': 1.0}
        >>> pr.no_grad_parameters
        {'a'}
    """
    def __init__(self, data=None):
        if data is None:
            data = {}
        if not isinstance(data, (dict, ParameterResolver)):
            raise TypeError("Data require a dict or a ParameterResolver, but get {}!".format(type(data)))
        for k, v in data.items():
            if not isinstance(k, str):
                raise TypeError("Parameter name should be a string, but get {}!".format(type(k)))
            if not isinstance(v, _num_type):
                raise TypeError("Require a number, but get {}, which is {}!".format(v, type(v)))
        super(ParameterResolver, self).__init__(data)
        self.no_grad_parameters = set()
        self.requires_grad_parameters = set(self.params_name)

    def get_cpp_obj(self):
        """Get cpp obj of this parameter resolver"""
        return mb.parameter_resolver(self, self.no_grad_parameters, self.requires_grad_parameters)

    def __setitem__(self, keys, values):
        """
        Set parameter or as list of parameters of this parameter resolver.

        By default, the parameter you set requires gradient.

        Args:
            keys (Union[str, list[str]]): The name of parameters.
            values (Union[number, list[number]]): The value of parameters.

        Raises:
            TypeError: If the key that you set is not a string or a iterable of
                string.
        """
        if isinstance(keys, str):
            if not isinstance(values, _num_type):
                raise TypeError("Parameter value should be a number, but get {}, which is {}!".format(
                    values, type(values)))
            super().__setitem__(keys, values)
            self.requires_grad_parameters.add(keys)
        elif isinstance(keys, Iterable):
            if not isinstance(values, Iterable):
                raise ValueError("Values should be iterable.")
            if len(values) != len(keys):
                raise ValueError("Size of keys and values do not match.")
            for i, k in enumerate(keys):
                self.__setitem__(k, values[i])
        else:
            raise TypeError("Parameter name should be a string, but get {}!".format(type(keys)))

    def __add__(self, pr):
        """
        Add a parameter resolver with other parameter.

        Returns:
            ParameterResolver, parameter resolver after adding.

        Args:
            pr (ParameterResolver): The parameter resolver need to add.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr1 = ParameterResolver({'a': 1})
            >>> pr2 = ParameterResolver({'a': 2, 'b': 3})
            >>> (pr1 + pr2).expression()
            3*a + 3*b
        """
        if not isinstance(pr, ParameterResolver):
            raise ValueError('Require a parameter resolver, but get {}.'.format(type(pr)))
        res = self * 1
        pr = pr * 1
        for k, v in pr.items():
            if k in res:
                res[k] += v
                pr[k] = res[k]
        res.update(pr)
        return res

    def __sub__(self, pr):
        """
        Subtraction a parameter resolver with other parameter.

        Returns:
            :class:`mindquantum.core.parameterresolver.ParameterResolver`

        Args:
            pr (ParameterResolver): The parameter resolver need to subtract.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr1 = ParameterResolver({'a': 1})
            >>> pr2 = ParameterResolver({'a': 2, 'b': 3})
            >>> (pr1 - pr2).expression()
            -a - 3*b
        """
        return self + (-1 * pr)

    def __neg__(self):
        """
        Get the negative version of this parameter resolver.

        Returns:
            ParameterResolver, the negative version.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr1 = ParameterResolver({'a': 1})
            >>> (-pr1).expression()
            -a
        """
        return -1 * self

    def __imul__(self, num):
        """
        Parameter support inplace multiply.

        Returns:
            :class:`mindquantum.core.parameterresolver.ParameterResolver`

        Args:
            num (number): Multiply factor.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr = ParameterResolver({'a': 1, 'b': 2})
            >>> pr *= 2
            >>> pr
            {'a': 2, 'b': 4}
        """
        no_grad_parameters = deepcopy(self.no_grad_parameters)
        requires_grad_parameters = deepcopy(self.requires_grad_parameters)
        for k in self.keys():
            self[k] = self[k] * num
        self.no_grad_parameters = no_grad_parameters
        self.requires_grad_parameters = requires_grad_parameters
        return self

    def __mul__(self, num):
        """
        Multiply num with every value of parameter resolver.

        Returns:
            :class:`mindquantum.core.parameterresolver.ParameterResolver`

        Args:
            num (number): Multiply factor.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr1 = ParameterResolver({'a': 1, 'b': 2})
            >>> pr2 = pr1 * 2
            >>> pr2
            {'a': 2, 'b': 4}
        """
        no_grad_parameters = deepcopy(self.no_grad_parameters)
        requires_grad_parameters = deepcopy(self.requires_grad_parameters)
        out = deepcopy(self)
        out *= num
        out.no_grad_parameters = no_grad_parameters
        out.requires_grad_parameters = requires_grad_parameters
        return out

    def __rmul__(self, num):
        """
        See :class:`mindquantum.core.parameterresolver.ParameterResolver.__mul__`.
        """
        return self.__mul__(num)

    def __eq__(self, other):
        _check_pr_type(other)
        no_grad_eq = self.no_grad_parameters == other.no_grad_parameters
        requires_grad_eq = self.requires_grad_parameters == other.requires_grad_parameters
        return super().__eq__(other) and no_grad_eq and requires_grad_eq

    @property
    def params_name(self):
        """
        Get the parameters name.

        Returns:
            list, a list of parameters name.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr = ParameterResolver({'a': 1, 'b': 2})
            >>> pr.params_name
            ['a', 'b']
        """
        return list(self.keys())

    @property
    def para_value(self):
        """
        Get the parameters value.

        Returns:
            list, a list of parameters value.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr = ParameterResolver({'a': 1, 'b': 2})
            >>> pr.para_value
            [1, 2]
        """
        return list(self.values())

    def requires_grad(self):
        """
        Set all parameters of this parameter resolver to require gradient
        calculation. Inplace operation.

        Returns:
            ParameterResolver, the parameter resolver itself.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr = ParameterResolver({'a': 1, 'b': 2})
            >>> pr.no_grad_part('a')
            {'a': 1, 'b': 2}
            >>> pr.requires_grad()
            {'a': 1, 'b': 2}
            >>> pr.requires_grad_parameters
            {'a', 'b'}
        """
        self.no_grad_parameters = set()
        self.requires_grad_parameters = set(self.params_name)
        return self

    def no_grad(self):
        """
        Set all parameters to not require gradient calculation. Inplace operation.

        Returns:
            ParameterResolver, the parameter resolver itself.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr = ParameterResolver({'a': 1, 'b': 2})
            >>> pr.no_grad()
            {'a': 1, 'b': 2}
            >>> pr.requires_grad_parameters
            set()
        """
        self.no_grad_parameters = set(self.params_name)
        self.requires_grad_parameters = set()
        return self

    def requires_grad_part(self, *names):
        """
        Set part of parameters that requires grad. Inplace operation.

        Args:
            names (tuple[str]): Parameters that requires grad.

        Returns:
            ParameterResolver, the parameter resolver itself.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr = ParameterResolver({'a': 1, 'b': 2})
            >>> pr.no_grad()
            {'a': 1, 'b': 2}
            >>> pr.requires_grad_part('a')
            {'a': 1, 'b': 2}
            >>> pr.requires_grad_parameters
            {'a'}
        """
        for name in names:
            if not isinstance(name, str):
                raise TypeError("name should be a string, but get {}!".format(type(name)))
            if name not in self:
                raise KeyError("Parameter {} not in this parameter resolver!".format(name))
            while name in self.no_grad_parameters:
                self.no_grad_parameters.remove(name)
            while name not in self.requires_grad_parameters:
                self.requires_grad_parameters.add(name)
        return self

    def no_grad_part(self, *names):
        """
        Set part of parameters that not requires grad.

        Args:
            names (tuple[str]): Parameters that not requires grad.

        Returns:
            ParameterResolver, the parameter resolver itself.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr = ParameterResolver({'a': 1, 'b': 2})
            >>> pr.no_grad_part('a')
            {'a': 1, 'b': 2}
            >>> pr.requires_grad_parameters
            {'b'}
        """
        for name in names:
            if not isinstance(name, str):
                raise TypeError("name should be a string, but get {}!".format(type(name)))
            if name not in self:
                raise KeyError("Parameter {} not in this parameter resolver!".format(name))
            while name not in self.no_grad_parameters:
                self.no_grad_parameters.add(name)
            while name in self.requires_grad_parameters:
                self.requires_grad_parameters.remove(name)
        return self

    def update(self, others):
        """
        Update this parameter resolver with other parameter resolver.

        Args:
            others (ParameterResolver): other parameter resolver.

        Raises:
            ValueError: If some parameters require grad and not require grad in
                other parameter resolver and vice versa.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr1 = ParameterResolver({'a': 1})
            >>> pr2 = ParameterResolver({'b': 2})
            >>> pr2.no_grad()
            {'b': 2}
            >>> pr1.update(pr2)
            >>> pr1
            {'a': 1, 'b': 2}
            >>> pr1.no_grad_parameters
            {'b'}
        """
        _check_pr_type(others)
        super().update(others)
        conflict = (self.no_grad_parameters & others.requires_grad_parameters) | (others.no_grad_parameters
                                                                                  & self.requires_grad_parameters)
        if conflict:
            raise ValueError("Parameter conflict, {} require grad in some parameter \
resolver and not require grad in other parameter resolver ".format(conflict))
        self.no_grad_parameters.update(others.no_grad_parameters)
        self.requires_grad_parameters.update(others.requires_grad_parameters)

    def expression(self):
        """
        Get the expression of this parameter resolver.

        Returns:
            sympy.Expr, the symbol expression of this parameter resolver.

        Examples:
            >>> from mindquantum.core.parameterresolver import ParameterResolver as PR
            >>> pr = PR({'a' : 2, 'b' : 0.3})
            >>> pr.expression()
            2*a + 0.3*b
        """
        res = 0
        for k, v in self.items():
            res += sp.Symbol(k) * v
        return res

    def conjugate(self):
        """
        Get the conjugate of the parameter resolver.

        Returns:
            ParameterResolver, the conjugate version of this parameter resolver.

        Examples:
            >>> from mindquantum.core.parameterresolver import ParameterResolver as PR
            >>> pr = PR({'a' : 1, 'b': 1j})
            >>> pr.conjugate().expression()
            a - 1.0*I*b
        """
        out = 1 * self
        for k, v in out.items():
            out[k] = np.conj(v)
        return out

    def combination(self, pr):
        """
        Apply linear combination between this parameter resolver with input pr.

        Args:
            pr (Union[dict, ParameterResolver]): The parameter resolver you
                want to do linear combination.

        Returns:
            numbers.Number, the combination result.

        Examples:
            >>> from mindquantum import ParameterResolver
            >>> pr1 = ParameterResolver({'a': 1, 'b': 2})
            >>> pr2 = ParameterResolver({'a': 2, 'b': 3})
            >>> pr1.combination(pr2)
            8
        """
        if not isinstance(pr, (ParameterResolver, dict)):
            raise ValueError('Require a parameter resolver or a dict, but get {}.'.format(type(pr)))
        res = 0
        for k, v in self.items():
            if k not in pr:
                raise KeyError('{} not in input parameter resolver'.format(k))
            res += v * pr[k]
        return res

    @property
    def real(self):
        """
        Get the real part of this parameter resolver

        Returns:
            ParameterResolver, the real part of this parameter resolver.

        Examples:
            >>> from mindquantum.core.parameterresolver import ParameterResolver as PR
            >>> pr = PR({'a': 1.2 + 1.3j})
            >>> pr.real
            {'a': 1.2}
        """
        out = 1 * self
        for k, v in self.items():
            out[k] = np.real(v)
        return out

    @property
    def imag(self):
        """
        Get the real part of this parameter resolver

        Returns:
            ParameterResolver, the image part of this parameter resolver.

        Examples:
            >>> from mindquantum.core.parameterresolver import ParameterResolver as PR
            >>> pr = PR({'a': 1.2 + 1.3j})
            >>> pr.imag
            {'a': 1.3}
        """
        out = 1 * self
        for k, v in self.items():
            out[k] = np.imag(v)
        return out

    def dumps(self, indent=4):
        '''
        Dump ParameterResolver into JSON(JavaScript Object Notation)

        Args:
            indent (int): Then JSON array elements and object members will be
                pretty-printed with that indent level. Default: 4.

        Returns:
            string(JSON), the JSON of ParameterResolver

        Examples:
            >>> from mindquantum.core.parameterresolver import ParameterResolver
            >>> pr = ParameterResolver({'a': 1, 'b': 2, 'c': 3, 'd': 4})
            >>> pr.no_grad_part('a', 'b')
            >>> print(pr.dumps())
            {
                "a": 1,
                "b": 2,
                "c": 3,
                "d": 4,
                "__class__": "ParameterResolver",
                "__module__": "parameterresolver",
                "no_grad_parameters": [
                    "a",
                    "b"
                ]
            }
        '''
        if indent is not None:
            _check_int_type('indent', indent)
        dic = dict(zip(self.params_name, self.para_value))
        dic['__class__'] = self.__class__.__name__
        dic['__module__'] = self.__module__

        dic['no_grad_parameters'] = list()
        for j in self.no_grad_parameters:
            dic["no_grad_parameters"].append(j)
        dic["no_grad_parameters"].sort()

        return json.dumps(dic, indent=indent)

    @staticmethod
    def loads(strs):
        '''
        Load JSON(JavaScript Object Notation) into FermionOperator

        Args:
            strs (str): The dumped parameter resolver string.

        Returns:
            FermionOperator, the FermionOperator load from strings

        Examples:
            >>> from mindquantum.core.parameterresolver import ParameterResolver
            >>> strings = """
                {
                    "a": 1,
                    "b": 2,
                    "c": 3,
                    "d": 4,
                    "__class__": "ParameterResolver",
                    "__module__": "parameterresolver",
                    "no_grad_parameters": [
                        "a",
                        "b"
                    ]
                }
                """
            >>> obj = ParameterResolver.loads(string)
            >>> print(obj)
            {'a': 1, 'b': 2, 'c': 3, 'd': 4}
            >>> print('requires_grad_parameters is:', obj.requires_grad_parameters)
            requires_grad_parameters is: {'c', 'd'}
            >>> print('no_grad_parameters is :', obj.no_grad_parameters)
            no_grad_parameters is : {'b', 'a'}
        '''
        _check_input_type('strs', str, strs)
        dic = json.loads(strs)

        if '__class__' in dic:
            class_name = dic.pop('__class__')

            if class_name == 'ParameterResolver':
                module_name = dic.pop('__module__')
                module = __import__(module_name)
                class_ = getattr(module, class_name)
                no_grad_parameters_list = dic.pop('no_grad_parameters')

                args = dic
                p = class_(args)

                for i in no_grad_parameters_list:
                    p.no_grad_part(str(i))

            else:
                raise TypeError("Require a ParameterResolver class, but get {} class".format(class_name))

        else:
            raise ValueError("Expect a '__class__' in strings, but not found")

        return p


def _check_pr_type(pr):
    if not isinstance(pr, ParameterResolver):
        raise TypeError("Require a ParameterResolver, but get {}".format(type(pr)))
