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

If any participant IDs aren't found in Geneworks, a note will be added to the bottom of the output file.
