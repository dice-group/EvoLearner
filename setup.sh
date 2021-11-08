#!/bin/bash

wget https://github.com/SmartDataAnalytics/DL-Learner/releases/download/1.4.0/dllearner-1.4.0.tar.gz
tar xf dllearner-1.4.0.tar.gz
cp -R dllearner-1.4.0 learningsystems/celoe/
mv dllearner-1.4.0 learningsystems/ocel/
rm dllearner-1.4.0.tar.gz
mvn package && pip install -e learningsystems/evolearner/EvoLearner
mkdir learningtasks/premierleague/owl/data
gdown --id 1VyfV7I8fcoX1gzCz4wPs7uFY1_2jfqVy --output \
        learningtasks/premierleague/owl/data/premierleague.owl
