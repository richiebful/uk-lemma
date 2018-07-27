mkdir ../data
wget -P ../data https://github.com/LinguisticAndInformationSystems/mphdict/raw/master/src/data/mph_ua.db
python3 gen_morphy.py ../data/mph_ua.db
