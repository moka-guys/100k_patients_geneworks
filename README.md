# 100k_patients_geneworks v1.0
GeL alert us that new results are available by email.
Recently they have stopped including patient information in these emails. Instead we just get a comma separated list of interpretation request IDs and family IDs. e.g.
```
request_id, family_id
OPA-11585-1, 203351
OPA-11612-1, 266435
OPA-11636-1, 267035
```
We need to identify these samples so that we can inform clinicians and add details into our tracking system.

This script takes a csv file (which can be created by copying and pasting directly from the results email into a text file), gets the participant ID from the CIPAPI, and uses this to return patient information from Geneworks.

## Usage

This script requires access to the CIPAPI so must be run on our trust linux server.

Requirements:

* Python 2.7
* Access to Geneworks via ODBC
* Access to CIPAPI
* JellyPy (in PYTHONPATH)
* pyodbc
* numpy
* pandas

Create the input csv file (see above) and transfer to the server where code will be run.

On `SV-TE-GENAPP01` activate the `jellypy` conda environment so that above requirements are met:

```
source activate jellypy
```

Run the script:

```
python /home/mokaguys/Documents/100k_patients_geneworks/100k_geneworks_participants.py -i INPUT_FILE -o OUTPUT_FILE
```