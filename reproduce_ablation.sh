#!/bin/bash

config_file="learningsystems/evolearner/evo_config.prop"

add_to_file() {
    echo "$1" >> "$config_file"
}

run() {
    results=()
    for i in {1..3}
    do
       add_to_file "seed = $i"
       mvn -e exec:java -Dexec.mainClass=org.aksw.mlbenchmark.Benchmark -Dexec.args=scripts/evolearner_ablation.plist
       mv testResult.xml "$1_$i.xml" && results+=("$1_$i.xml")
       grep -v "seed" "$config_file" > "learningsystems/evolearner/temp"
       mv "learningsystems/evolearner/temp" "$config_file"
    done

    rm "$config_file"
    python scripts/sml_parser.py "${results[@]}" "${1}"
    rm "${results[@]}"
}

mkdir -p results

# Run EvoLearner
run "EvoLearner"

# Run EvoLearner without random walk initialization, using ramped-half-half with maximum height of 6
add_to_file "init_method = random_rhh"
add_to_file "random_max_height = 6"
run "WithoutRandomWalkInit"

# Run EvoLearner without data properties
add_to_file "expressivity = ALCN"
run "WithoutDataProperties"

# Run EvoLearner without data properties and random walk initialization, using ramped-half-half with maximum height of 6
add_to_file "init_method = random_rhh"
add_to_file "random_max_height = 6"
add_to_file "expressivity = ALCN"
run "WithoutBoth"

python scripts/combine_frames.py "EvoLearnerf1" "WithoutRandomWalkInitf1" "WithoutDataPropertiesf1" "WithoutBothf1" "results/EvoLearner_Ablation.md"
rm -rf *"f1" *"acc" *"length" "sml-temp"*
