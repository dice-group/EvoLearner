#!/bin/bash

systems=(evolearner celoe spacel aleph_swipl)
time_stamps=(205 210 230 260 320 380 440 500)
#time_stamps=(205 210 230)

# EvoLearner config file for the seed
config_file="learningsystems/evolearner/evo_config.prop"

mkdir -p results

results=()
for system in "${systems[@]}"
do
    for time in "${time_stamps[@]}"
    do
        runs=(1)
        if [[ "$system" == "evolearner" || "$system" == "spacel" ]]; then
            echo "$system $time"
            runs=(1 2 3)
        fi

        if [[ "$system" == "aleph_swipl" ]]; then
            time="$(($time-200))"
        fi

        file="${system}_${time}.plist"
        python scripts/write_plist.py $file "$system" "$time"

        results_runs=()
        for i in "${runs[@]}"
        do
            echo "seed = $i" > "$config_file"
            mvn -e exec:java -Dexec.mainClass=org.aksw.mlbenchmark.Benchmark -Dexec.args=$file
            mv testResult.xml "${system}_${time}_${i}.xml"
            results_runs+=("${system}_${time}_${i}.xml")
        done

        python scripts/sml_parser.py "${results_runs[@]}" "${system}_${time}.csv"
        results+=("${system}_${time}.csvf1")
        rm "${system}_${time}.plist" "${results_runs[@]}" "${system}_${time}.csvacc" \
           "${system}_${time}.csvlength"
    done
done

python scripts/plot.py "${results[@]}"
rm -rf "${results[@]}" "$config_file" "sml-temp"*
