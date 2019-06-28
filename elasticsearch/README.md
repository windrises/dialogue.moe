# elasticsearch

## Install

Download elasticsearch-5.6.16.tar.gz

```bash
tar -xzvf elasticsearch-5.6.16.tar.gz
cd elasticsearch-5.6.16
# install elasticsearch-analysis-ik
./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v5.6.16/elasticsearch-analysis-ik-5.6.16.zip
./bin/elasticsearch
```

with python3

```bash
pip install elasticsearch==5.5.1
```

## Start

```bash
python create_mapping.py
```
