#!/bin/bash

python test_Ann_JP.py --year 2007
python modify_xml.py  --year 2007
python statistic_xml.py --year 2007
python create_data.py --year 2007
