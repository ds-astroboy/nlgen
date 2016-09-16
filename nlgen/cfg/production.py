from .result import Result
from ..exception import (
    IncongruentFeature,
)
from .feature import unify_features
from ..compat import string_type


class ProductionBase(object):
    pass


class ProductionUnion(ProductionBase):
    """
    the union of several productions. It will
    iterate through all matches through all production lists.
    """

    def __init__(self, individual_production_list):
        self._individual_production_list = individual_production_list

    def permutations(self, cfg):
        for production in self._individual_production_list:
            for permutation in production.permutations(cfg):
                yield permutation


class Production(ProductionBase):
    """
    a list of productions, such as
    PRONOUN " " VERB " " NOUN
    """

    def __init__(self, production_list):
        self._production_list = production_list

    def permutations(self, cfg):
        return self._permutations_from_list(
            self._production_list, cfg
        )

    def _permutations_from_list(self, production_list, cfg):
        if len(production_list) == 0:
            yield Result((), {})
        else:
            lhs = production_list[0]
            rhs = production_list[1:]
            for lhs_value in lhs.permutations(cfg):
                for rhs_value in self._permutations_from_list(rhs, cfg):
                    try:
                        unioned_features = unify_features(lhs_value.features,
                                                          rhs_value.features)
                        yield Result(lhs_value.value + rhs_value.value, unioned_features)
                    except IncongruentFeature:
                        # we don't consider
                        # incongruent features.
                        continue

    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self._production_list == other._production_list


class ProductionRef(ProductionBase):

    def __init__(self, key):
        self._key = key

    def permutations(self, cfg):
        return cfg.permutations(self._key)

    def __eq__(self, other):
        return (
            isinstance(other, ProductionRef) and
            self._key == other._key
        )


class Terminal(ProductionBase):

    def __init__(self, value, features=None):
        self._value = value
        self._features = self._coerce_features(features or {})

    @property
    def features(self):
        return self._features

    def permutations(self, cfg):
        yield Result((self._value,), self._features)

    def __eq__(self, other):
        return (
            isinstance(other, Terminal) and
            self._value == other._value
        )

    def __repr__(self):
        return "<Terminal: {0}>".format(self._value.encode("utf-8"))

    def __hash__(self):
        return hash(self._value)

    @staticmethod
    def _coerce_features(feature_dict):
        """
        the features dictionary can accept a variety
        of types, so this method provides proper
        enforcement to the correct data structure.

        the output data structure is a dictionary
        of <str, set> mappings.
        """
        for k, v in feature_dict.items():
            if isinstance(v, set):
                # the desired type.
                continue
            if isinstance(v, string_type):
                v = set([v])
            elif hasattr(v, "__iter__"):
                v = set(v)
            else:
                v = set([str(v)])
            feature_dict[k] = v
        return feature_dict
