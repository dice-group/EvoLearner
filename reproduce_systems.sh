#!/bin/bash

add_line() {
    sed '$d' "temp1$2" > "$1$2"
    tail -1 "temp2$2" >> "$1$2"
    tail -1 "temp1$2" >> "$1$2"
}

config_file="learningsystems/evolearner/evo_config.prop"
name="EvoLearner_SPaCEL"
name2="CELOE_OCEL"
name3="Aleph"

mkdir -p results
# Run EvoLearner and SPaCEL and average the results 3 times
results=()
for i in {1..3}
do
   echo "seed = $i" > "$config_file"
   mvn -e exec:java -Dexec.mainClass=org.aksw.mlbenchmark.Benchmark -Dexec.args=scripts/evolearner_spacel.plist
   mv testResult.xml "${name}_$i.xml" && results+=("${name}_$i.xml")
done

rm "$config_file"
python scripts/sml_parser.py "${results[@]}" "$name"
rm "${results[@]}"


# Run CELOE, OCEL
mvn -e exec:java -Dexec.mainClass=org.aksw.mlbenchmark.Benchmark -Dexec.args=scripts/celoe_ocel.plist
python scripts/sml_parser.py testResult.xml "temp1"
mvn -e exec:java -Dexec.mainClass=org.aksw.mlbenchmark.Benchmark \
    -Dexec.args=scripts/celoe_ocel_premierleague.plist
python scripts/sml_parser.py testResult.xml "temp2"
# Merge premierleague into the second last line in the tables with all datasets for CELOE and OCEL
add_line "$name2" "f1"
add_line "$name2" "acc"
add_line "$name2" "length"
rm "temp1"* "temp2"*


# Run Aleph
mvn -e exec:java -Dexec.mainClass=org.aksw.mlbenchmark.Benchmark -Dexec.args=scripts/aleph.plist
python scripts/sml_parser.py testResult.xml "$name3"
rm testResult.xml

python scripts/combine_frames.py "${name}f1" "${name2}f1" "${name3}f1" "results/f1_systems.md"
python scripts/combine_frames.py "${name}acc" "${name2}acc" "${name3}acc" "results/accuracy_systems.md"
python scripts/combine_frames.py "${name}length" "${name2}length" "${name3}length" "results/length_systems.md"
rm -rf "${name}"* "${name2}"* "${name3}"* "sml-temp"*
