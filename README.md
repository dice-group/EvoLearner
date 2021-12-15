## Note: Use this repository to reproduce the exact numbers from the paper, otherwise try out the new implementation of EvoLearner that is part of [Ontolearn](https://github.com/dice-group/Ontolearn) (work in progress)
# EvoLearner: Learning Description Logics with Evolutionary Algorithms

This repository contains code to reproduce the results of our paper ```EvoLearner: Learning Description Logics with Evolutionary Algorithms```.

In order to run all experiments, this repository contains [SML-Bench](https://github.com/SmartDataAnalytics/SML-Bench).

The code of `EvoLearner` can be found in this [folder](https://github.com/dice-group/EvoLearner/tree/master/learningsystems/evolearner/EvoLearner).

## Installation

### Requirements

* Ubuntu 18.04 LTS
* Python 3.6.9+ as `python`
* Java 8/11
* Apache Maven 3.6.0+
* 32GB RAM

Clone the repository:
```
git clone https://github.com/EvoLearnerOnto/EvoLearner.git
```
Then run:
```
./setup.sh
```
Alternatively, use the provided ```Dockerfile```: 
```
docker build -t evolearner .
docker run -it --rm --name=evolearner evolearner
```

When running the experiments below in the container, they will be written to the
```results``` folder in the container. 

To make them available outside the container, you can mount a local directory:
```
docker run -it -v /path-to-local-directory:/sml-bench/results --rm --name=evolearner evolearner
```

### Install Aleph (optional, already installed in the ```Dockerfile```)

To install Aleph follow the instructions [here](https://github.com/EvoLearnerOnto/EvoLearner/tree/master/learningsystems/aleph_swipl).

This is not required, so if Aleph is not installed the results of Aleph will just be missing.

## Reproduce results

To reproduce the results of EvoLearner, CELOE, OCEL, SPaCEL, Aleph (Table 3) run:
```
./reproduce_systems.sh
```
To reproduce the results of the ablation analysis of EvoLearner (Table 4) run:
```
./reproduce_ablation.sh
```
To reproduce the results of different variants of the random walk init (Table 5) run:
```
./reproduce_random_walk_variants.sh
```
To reproduce the results of the initialization methods (Table 7) run:
```
./reproduce_init_methods.sh
```
To reproduce the results of different `mutation` operators (Table 8) run:
```
./reproduce_mutation.sh
```
To reproduce the results of different settings for the `maxT` parameter (Table 9) run:
```
./reproduce_maxT.sh
```
To reproduce the results of different settings for the fitness function run:
```
./reproduce_fitness.sh
```
To reproduce the results of the F-measure over runtime experiment (Figure 3) run:
```
./reproduce_plot.sh
```
Afterward, the results can be found in the ```results``` folder.

## Examples

Some solutions that were found by the systems for the `Uncle` learning problem:

**EvoLearner**

`Male ⊓ ((∃ hasSibling.Parent) ⊔ (∃ married.(∃ hasSibling.Parent)))`

- Perfect solution both on training and test data, short length

**CELOE**

`(Son ⊓ (∃ hasSibling.Parent))  ⊔ ∃ married.Sister`

- Short length, not 100% correct (Son vs. Male, Sister vs. hasSibling.Parent)

**OCEL**

`Male ⊓ ((∃ hasSibling.Parent) ⊔ (∃ married.(Daughter ⊓ ∃ hasSibling.Parent)))`

- Perfect solution on training and test data but a bit longer than necessary (one atomic concept too much: Daughter)
 
**SPaCEL**

`(¬Female ⊓ (∃ hasSibling.Parent)) ⊔ (¬Female ⊓ ∃ married.(∃ hasSibling.Parent)))`

- Perfect solution on training and test data but a bit longer than necessary (Male expressed as ¬Female, and ¬Female expressed two times)

## Fitness Function

Showing the influence of different settings of the weight parameter of the fitness function.

(by how much the quality of an individual, i.e. concept, is weighted compared to its length)

### F1-measure
|   | 8092 | 4096 | 2048 | 1024 | 512 | 256 | 128 | 64 | 32  |
|:--|:--:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|:---:|
| Carcinogenesis   | 0.68 | 0.67 | 0.70 | 0.69 | 0.67  | 0.64 | 0.61  | 0.60  | 0.60  |
| Uncle   | 0.99 | 0.99 | 1.00 | 1.00 | 1.00  | 0.98 | 0.93  | 0.88  | 0.87  |
| Hepatitis  | 0.79 | 0.80 | 0.79 | 0.78 | 0.76 | 0.71 | 0.70  | 0.61  | 0.59  |
| Lymphography  | 0.84 | 0.85 | 0.84 | 0.83 | 0.83 | 0.84 | 0.87  | 0.87  | 0.87  |
| Mammographic  | 0.81 | 0.81  | 0.81  | 0.81  | 0.80  | 0.78  | 0.78  | 0.78  | 0.78  |
| Mutagenesis  | 1.00 | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  |
| NCTRER  | 1.00 | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  |
| Premier League  | 1.00 | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  | 1.00  |
| Pyrimidine  | 0.91  | 0.91  | 0.91  | 0.91  | 0.92  | 0.92  | 0.88  | 0.89  | 0.78  |

### Length
|   | 8092 | 4096 | 2048 | 1024 | 512 | 256 | 128 | 64 | 32  |
|:--|:--:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|:---:|
| Carcinogenesis   | 27.43 | 28.60 | 23.41 | 22.20 | 17.10  | 10.00 | 5.40  | 3.13  | 3.00  |
| Uncle   | 10.90 | 10.90 | 10.87 | 10.60 | 11.40  | 9.20 | 6.50  | 4.23  | 3.33  |
| Hepatitis  | 25.33 | 24.30 | 19.77 | 14.97 | 11.17 | 9.77 | 7.33  | 5.63  | 5.43  |
| Lymphography  | 22.20 | 21.27 | 17.10 | 12.53 | 7.67 | 3.77 | 3.07  | 3.00  | 3.00  |
| Mammographic  | 27.17 | 23.30  | 20.43  | 14.67  | 11.20  | 3.00  | 3.00  | 3.00  | 3.00  |
| Mutagenesis  | 3.00 | 3.00  | 3.00  | 3.00  | 3.00  | 3.00  | 3.00  | 3.00  | 3.00  |
| NCTRER  | 3.00 | 3.00  | 3.00  | 3.00  | 3.00  | 3.00  | 3.00  | 3.00  | 3.00  |
| Premier League  | 6.93  | 6.93  | 6.93  | 6.93  | 6.87  | 6.93  | 7.13  | 6.87  | 7.00  |
| Pyrimidine  | 11.40  | 11.40  | 11.40  | 11.40  | 11.27  | 12.20  | 10.87  | 7.13  | 5.13  |

## Involved systems and frameworks

* SML-Bench (used to run all experiments): https://github.com/SmartDataAnalytics/SML-Bench
* DL-Learner (CELOE and OCEL): https://github.com/SmartDataAnalytics/DL-Learner
* SParCEL: https://github.com/tcanvn/SParCEL
* DEAP: https://github.com/DEAP/deap
* Aleph: https://www.cs.ox.ac.uk/activities/programinduction/Aleph/aleph.html
* Owlready2: https://github.com/pwin/owlready2 
