#!/usr/bin/env python
# reddit-reliability


class FeatureVector:
    """ A vector which stores feature values, and possibly the documentation for
        the physical meaning of those features.
    """
    def __init__(self, store_docs=False):
        self.store_docs = store_docs
        self.feature_vector = []

        if self.store_docs:
            self.feature_docs = []

    def append(self, feature_val, doc):
        """ Given a feature value and a docstring for what it is, store them.
        """
        self.feature_vector.append(feature_val)
        if self.store_docs:
            self.feature_docs.append(doc)
