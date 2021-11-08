import xml.etree.ElementTree as ET
import statistics
import sys
import collections
import pandas as pd

def length_manchester(concept_string):
    return len(concept_string.split()) - concept_string.count("[")

def length_evo(concept_string):
    concept_string = concept_string.replace(",", "")
    concept_string = concept_string.replace("(", " ")
    return len(concept_string.split()) + sum(map(concept_string.count, ("exists", "forall", "someValues", "hasValue", "cargeq", "carleq")))

def get_averages(f):
    root = ET.parse(f).getroot()

    datasets = collections.OrderedDict()
    main = root.findall('dict')[0]

    for d, r in zip(main[0::2], main[1::2]):
        dataset = d.text
        if dataset not in datasets:
            n = collections.OrderedDict()
            datasets[dataset] = n
        else:
            n = datasets[dataset]

        for number, r2 in zip(r[0::2], r[1::2]):
            number = number.text
            if number not in n:
                nn = collections.OrderedDict()
                n[number] = nn
            else:
                nn = n[number]

            for fold, r3 in zip(r2[0::2], r2[1::2]):
                for system, r4 in zip(r3[0::2], r3[1::2]):
                    system = system.text
                    if system not in nn:
                        nnn = collections.OrderedDict()
                        nn[system] = nnn
                    else:
                        nnn = nn[system]

                    for key, value in zip(r4[0::2], r4[1::2]):
                        if key.text == "validationResult":
                            # no result
                            if value.text != "ok":
                                break

                        if key.text == "measure":
                            for measure, val in zip(value[0::2], value[1::2]):
                                measure = measure.text
                                if measure not in nnn:
                                    nnnn = []
                                    nnn[measure] = nnnn
                                else:
                                    nnnn = nnn[measure]

                                if val.text == "NaN":
                                    nnnn.append(0.0)
                                else:
                                    nnnn.append(float(val.text))

                        if key.text == "trainingRaw":
                            length_string = "length"
                            if length_string not in nnn:
                                output = []
                                nnn[length_string] = output
                            else:
                                output = nnn[length_string]

                            if system == "celoe":
                                length = length_manchester(value.text)
                                output.append(length)
                            elif system == "ocel":
                                length = length_manchester(value.text)
                                output.append(length)
                            elif system == "spacel":
                                length = length_manchester(value[-2].text)
                                output.append(length)
                            elif system == "evolearner":
                                length = length_evo(value.text)
                                output.append(length)
    return datasets


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("wrong arguments")

    runs = []
    for f in sys.argv[1:-1]:
        print(f)
        runs.append(get_averages(f))

    datasets = runs[0]

    data_f1 = collections.OrderedDict()
    data_acc = collections.OrderedDict()
    data_length = collections.OrderedDict()
    systems = []

    for d in datasets:
        vals_acc = []
        data_acc[d] = vals_acc

        vals_f1 = []
        data_f1[d] = vals_f1

        vals_length = []
        data_length[d] = vals_length

        for x in datasets[d]:
            for system in datasets[d][x]:

                if system not in systems:
                    systems.append(system)

                current_mean = -1
                for measure in datasets[d][x][system]:
                    means = []
                    stdevs = []
                    for r in runs:
                        values = r[d][x][system][measure]
                        if len(values) == 10:
                            means.append(statistics.mean(values))
                            stdevs.append(statistics.stdev(values))



                    if len(means) == len(sys.argv) - 2:
                        current_mean = round(statistics.mean(means), 2)
                        current_stdev = round(statistics.mean(stdevs), 2)
                        if measure == "pred_acc":
                            vals_acc.append((current_mean, current_stdev))
                        if measure == "fmeasure":
                            vals_f1.append((current_mean, current_stdev))
                        if measure == "length":
                            vals_length.append((current_mean, current_stdev))
                if current_mean == -1:
                    vals_acc.append((None))
                    vals_f1.append((None))
                    vals_length.append((None))
                elif system == "aleph_swipl":
                    vals_length.append((None))


    df = pd.DataFrame(data_acc, index =systems)
    df.to_csv(sys.argv[-1] + 'acc')

    df = pd.DataFrame(data_f1, index =systems)
    df.to_csv(sys.argv[-1] + 'f1')

    df = pd.DataFrame(data_length, index =systems)
    df.to_csv(sys.argv[-1] + 'length')
