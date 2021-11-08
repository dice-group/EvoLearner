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
        add_to_file "max_neighbours = $1"
        mvn -e exec:java -Dexec.mainClass=org.aksw.mlbenchmark.Benchmark -Dexec.args=scripts/evolearner_ablation.plist
        mv testResult.xml "$1_$i.xml" && results+=("$1_$i.xml")
        rm "$config_file"
    done

    python scripts/sml_parser.py "${results[@]}" "${1}"
    rm "${results[@]}"
}

mkdir -p results

parameters=(1 2 4 6 8 10)
for j in "${parameters[@]}"
do
    run $j
done

python scripts/combine_frames_misc.py "${parameters[@]/%/f1}" "results/EvoLearner_maxT.md"
rm -rf *"f1" *"acc" *"length" "sml-temp"*
