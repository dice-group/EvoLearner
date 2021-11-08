import math
import copy

from owlready2 import AnnotationPropertyClass
from scipy.stats import entropy


class DefaultValueSplitter:

    def __init__(self, max_nr_splits=10):
        self.max_nr_splits = max_nr_splits

    def compute_splits(self, properties, type_=float):
        splits = {}
        for p in properties:
            if p.range[0] != type_ and p.range[0] != int and \
               not isinstance(p, AnnotationPropertyClass):
                continue
            all_values = {v[1] for v in p.get_relations()}
            splits[p] = self._compute_split_values(all_values)

        return splits

    def compute_split_property(self, property_, kb):
        pairs = kb.role_log[property_]
        all_values = set(pairs.values())
        return self._compute_split_values(property_, all_values)

    def _compute_split_values(self, property_, all_values):
        splits_dp = set()

        nr_values = len(all_values)
        if nr_values == 0:
            return splits_dp

        all_values = sorted(all_values)

        nr_splits = min(self.max_nr_splits, nr_values + 1)
        splits_dp.add(all_values[0])

        for split in range(1, nr_splits):
            index = math.floor(split * nr_values / nr_splits)
            temp = math.floor(split * nr_values / (nr_splits - 1) - 1)
            index = max(index, temp)

            n1 = all_values[index]
            n2 = all_values[min(nr_values-1, index+1)]

            if isinstance(property_, AnnotationPropertyClass) or \
               property_.range[0] == int:
                splits_dp.add(int(round((n1+n2)/2)))
            else:
                splits_dp.add(round((n1+n2)/2, 3))

        return splits_dp


class EntropyValueSplitter:

    def __init__(self, max_nr_splits=10):
        self.max_nr_splits = max_nr_splits
        self.property_values = {}
        self.splits = {}

    def compute_splits(self, properties, pos, neg, type_=float):
        self.splits = {}

        instances_splits = []
        for p in properties:
            if not isinstance(p, AnnotationPropertyClass) and \
               p.range[0] != type_ and p.range[0] != int:
                continue
            all_vl, pos_vl, neg_vl = self._get_values_uri_mappings(p, pos, neg)
            if len(all_vl) == 0:
                continue

            self.property_values[p] = (all_vl, pos_vl, neg_vl, 0, None)
            self.splits[p] = set()
            n_splits = self._compute_split_values(p, [self.property_values[p]])
            instances_splits.extend(n_splits)

        instances_splits = sorted(instances_splits,
                                  key=lambda k: k[3],
                                  reverse=True)

        while True:
            temp_splits = []
            all_done = True
            for p in self.splits:
                if len(self.splits[p]) >= self.max_nr_splits:
                    continue

                all_done = False
                copy_ins = copy.deepcopy(instances_splits)
                new_splits = self._compute_split_values(p, copy_ins)
                temp_splits.extend(new_splits)

            instances_splits = sorted(temp_splits,
                                      key=lambda k: k[3],
                                      reverse=True)

            if all_done or len(instances_splits) == 0:
                break

        return self.splits

    def _get_values_uri_mappings(self, property_, pos, neg):
        all_values = dict()
        pos_values = dict()
        neg_values = dict()
        for p in pos:
            if property_ in pos[p][1]:
                value = property_[pos[p][0]]
                value = value[0]

                all_values[p] = value
                pos_values[p] = value

        for n in neg:
            if property_ in neg[n][1]:
                value = property_[neg[n][0]]
                value = value[0]

                all_values[n] = value
                neg_values[n] = value

        return all_values, pos_values, neg_values

    def _compute_split_values(self, property_, instances_splits):
        new_splits = []
        for split in instances_splits:
            if len(self.splits[property_]) >= self.max_nr_splits:
                break
            if split[4] == property_:
                continue

            all_values, pos_values, neg_values = (
                    self._get_instances_overlapping(property_, split))

            current_pos = len(pos_values) / len(all_values)
            current_neg = len(neg_values) / len(all_values)
            current_entropy = entropy((current_pos, current_neg))

            best_gain = 0
            best_value = None
            best_entropy = None
            values = list(set(all_values.values()))
            values = sorted(values)

            if isinstance(property_, AnnotationPropertyClass) or \
               property_.range[0] == int:
                values = [int(round((x+y)/2))
                          for x, y in zip(values, values[1:])]
            else:
                values = [round((x+y)/2, 3)
                          for x, y in zip(values, values[1:])]

            for value in values:
                pos_below, pos_above = self._get_instances_counts(value,
                                                                  pos_values)
                neg_below, neg_above = self._get_instances_counts(value,
                                                                  neg_values)
                all_below = pos_below + neg_below
                all_above = pos_above + neg_above

                below_entropy = 0
                if all_below > 0:
                    below_entropy = entropy((pos_below / all_below,
                                            neg_below / all_below))

                above_entropy = 0
                if all_above > 0:
                    above_entropy = entropy((pos_above / all_above,
                                            neg_above / all_above))

                cond_entropy = (all_below / len(all_values) * below_entropy
                                + all_above / len(all_values) * above_entropy)

                gain = current_entropy - cond_entropy

                if gain >= best_gain and value not in self.splits[property_]:
                    best_gain = gain
                    best_value = value
                    best_entropy = (below_entropy, above_entropy)

            if best_value is not None:
                self.splits[property_].add(best_value)

                if best_entropy[0] > 0:
                    interval = (min(all_values.values()) - 1, best_value)
                    all_, pos_, neg_ = self._get_instances_interval(interval,
                                                                    all_values,
                                                                    pos_values,
                                                                    neg_values)
                    new_splits.append((all_, pos_, neg_,
                                      best_entropy[0],
                                      property_))

                if best_entropy[1] > 0:
                    interval = (best_value, max(all_values.values()) + 1)
                    all_, pos_, neg_ = self._get_instances_interval(interval,
                                                                    all_values,
                                                                    pos_values,
                                                                    neg_values)
                    new_splits.append((all_, pos_, neg_,
                                       best_entropy[1],
                                       property_))

        return new_splits

    def _get_instances_interval(self, interval,
                                all_values_,
                                pos_values_,
                                neg_values_):
        min_ = interval[0]
        max_ = interval[1]
        all_values = {uri: v for uri, v in all_values_.items()
                      if v > min_ and v <= max_}
        pos_values = {uri: v for uri, v in pos_values_.items()
                      if v > min_ and v <= max_}
        neg_values = {uri: v for uri, v in neg_values_.items()
                      if v > min_ and v <= max_}
        return all_values, pos_values, neg_values

    def _get_instances_counts(self, value, value_dict):
        count_below = len([k for k in value_dict if value_dict[k] <= value])
        count_above = len([k for k in value_dict if value_dict[k] > value])
        return count_below, count_above

    def _get_instances_overlapping(self, p, split):
        property_values = self.property_values[p]
        all_values = {uri: v for uri, v in property_values[0].items()
                      if uri in split[0]}
        pos_values = {uri: v for uri, v in property_values[1].items()
                      if uri in split[1]}
        neg_values = {uri: v for uri, v in property_values[2].items()
                      if uri in split[2]}
        return all_values, pos_values, neg_values
