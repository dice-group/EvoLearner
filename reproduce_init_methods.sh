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
        add_to_file "init_method = $1"
        mvn -e exec:java -Dexec.mainClass=org.aksw.mlbenchmark.Benchmark -Dexec.args=scripts/evolearner_ablation.plist
        mv testResult.xml "$1_$i.xml" && results+=("$1_$i.xml")
        rm "$config_file"
    done

    python scripts/sml_parser.py "${results[@]}" "${1}"
    rm "${results[@]}"
}

mkdir -p results

parameters=("random_walk" "random_grow" "random_full" "random_rhh")
for j in "${parameters[@]}"
do
    run $j
done

python scripts/combine_frames.py "${parameters[@]/%/f1}" "results/EvoLearner_Init_Methods.md"
rm -rf *"f1" *"acc" *"length" "sml-temp"*
