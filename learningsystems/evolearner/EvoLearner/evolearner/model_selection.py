import random
import numpy as np


def cross_validation(learner, pos, neg, folds, verbose=False, **kwargs):
    random.shuffle(pos)
    random.shuffle(neg)
    pos_folds = np.array_split(pos, folds)
    neg_folds = np.array_split(neg, folds)

    accuracy = 0
    f_1 = 0
    size = 0
    for val in range(folds):
        pos_train = np.concatenate(pos_folds[:val] + pos_folds[val+1:])
        neg_train = np.concatenate(neg_folds[:val] + neg_folds[val+1:])
        pos_val = pos_folds[val]
        neg_val = neg_folds[val]

        learner.fit(pos_train, neg_train, **kwargs)
        val_score_f1 = learner.score(pos_val, neg_val, measure="f1")
        train_score_f1 = learner.score(pos_train, neg_train, measure="f1")

        val_score_acc = learner.score(pos_val, neg_val, measure="accuracy")
        train_score_acc = learner.score(pos_train,
                                        neg_train,
                                        measure="accuracy")

        if verbose:
            best = learner.best_hypotheses(n=1)[0]
            print("Fold ", val+1, " : ", best.str,
                  "Val score F1: ", val_score_f1,
                  "Train score F1: ", train_score_f1,
                  "Val score accuracy: ", val_score_acc,
                  "Train score accuracy: ", train_score_acc)

        size += (sum(len(a) for a in
                 learner.result_population)/learner.population_size)

        accuracy += val_score_acc
        f_1 += val_score_f1

    return accuracy/folds, size/folds, f_1/folds
