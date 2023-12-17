# LFIOKG

## Install dependency
```
pip install -r requirements.txt
```
## LFIOKG

### Use your own data
```
python LFIOKG.py "path_to_input_file" "path_to_output_file" "path_to_background_file"
```

### Reproduce the paper experiments

#### EXP1-1
```
python LFIOKG.py ALS/als_input1.tsv ALS/als_output1.tsv kg1.tsv
```

#### EXP1-2
```
python LFIOKG.py ALS/als_input1.tsv ALS/als_output2.tsv kg1.tsv
```

#### Exp2-1
```
python LFIOKG.py NCF/ncf_input1.tsv NCF/ncf_output1.tsv kg1.tsv
```

#### Exp2-2
```
python LFIOKG.py NCF/ncf_input1.tsv NCF/ncf_output2.tsv kg1.tsv
```