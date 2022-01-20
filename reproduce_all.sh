#!/bin/bash
echo "Running System Comparison..."
./reproduce_systems.sh
echo "Running Ablation Analysis..."
./reproduce_ablation.sh
echo "Running Random Walk Variants..."
./reproduce_random_walk_variants.sh
echo "Running Initialization Methods..."
./reproduce_init_methods.sh
echo "Running Mutation Operators..."
./reproduce_mutation.sh
echo "Running maxT Settings..."
./reproduce_maxT.sh
echo "Running Fitness Function Settings..."
./reproduce_fitness.sh
