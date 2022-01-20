#!/bin/bash

dllearner_version=1.4.0

wget "https://github.com/SmartDataAnalytics/DL-Learner/releases/download/${dllearner_version}/dllearner-${dllearner_version}.tar.gz"
tar xf "dllearner-${dllearner_version}.tar.gz"
cp -R "dllearner-${dllearner_version}" learningsystems/celoe/
mv "dllearner-${dllearner_version}" learningsystems/ocel/
rm "dllearner-${dllearner_version}.tar.gz"
mvn package && pip install -e learningsystems/evolearner/EvoLearner
mkdir learningtasks/premierleague/owl/data
wget --output-document learningtasks/premierleague/owl/data/premierleague.owl \
    https://github.com/SmartDataAnalytics/SML-Bench/blob/updates/learningtasks/premierleague/owl/data/premierleague.owl?raw=true
