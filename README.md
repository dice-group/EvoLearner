# EvoLearner: Learning Description Logics with Evolutionary Algorithms

This repository contains code to reproduce the results of our paper ```EvoLearner: Learning Description Logics with Evolutionary Algorithms```.

In order to run all experiments, this repository contains [SML-Bench](https://github.com/SmartDataAnalytics/SML-Bench).

The code of `EvoLearner` can be found in this [folder](https://github.com/EvoLearnerOnto/EvoLearner/tree/master/learningsystems/evolearner/EvoLearner).

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
To reproduce the results of the F-measure over runtime experiment (Figure 3) run:
```
./reproduce_plot.sh
```
Afterward, the results can be found in the ```results``` folder.

## Involved systems and frameworks

* SML-Bench (used to run all experiments): https://github.com/SmartDataAnalytics/SML-Bench
* DL-Learner (CELOE and OCEL): https://github.com/SmartDataAnalytics/DL-Learner
* SParCEL: https://github.com/tcanvn/SParCEL
* DEAP: https://github.com/DEAP/deap
* Aleph: https://www.cs.ox.ac.uk/activities/programinduction/Aleph/aleph.html
* Owlready2: https://github.com/pwin/owlready2 
