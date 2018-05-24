'''
v1.0 - AB 2018/05/24
Requirements:
    Access to Geneworks via ODBC
    Access to CIPAPI
    JellyPy
    pyodbc
    pandas

usage: 100k_geneworks_participants.py [-h] -i INPUT_FILE -o OUTPUT_FILE

Takes an input csv file containing request ids and family ids in format sent
in GeL results emailOutputs a csv file with patient information from Geneworks

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        Input CSV file
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output CSV file
'''


import argparse
import pyodbc
import pandas
from pyCIPAPI.interpretation_requests import get_interpretation_request_list

def process_arguments():
    """
    Uses argparse module to define and handle command line input arguments and help menu
    """
    # Create ArgumentParser object. Description message will be displayed as part of help message if script is run with -h flag
    parser = argparse.ArgumentParser(
        description='Takes an input csv file containing request ids and family ids in format sent in GeL results email' 
        'Outputs a csv file with patient information from Geneworks'
    )
    # Define the arguments that will be taken.
    parser.add_argument('-i', '--input_file', required=True, help='Input CSV file')
    parser.add_argument('-o', '--output_file', required=True, help='Output CSV file')
    # Return the arguments
    return parser.parse_args()

def get_ir_id_dataframe(input_csv):
    """
    Reads information in input file dataframe
    """
    # Read input CSV file into a dataframe
    request_id_df = pandas.read_csv(input_csv)
    # Split the request_id (e.g. OPA-1234-1) column into 3 seperate fields cip, ir_id and version (e.g. 'OPA', '1234' and '1')
    request_id_df[['cip', 'ir_id', 'version']] = request_id_df['request_id'].str.split('-',expand=True)
    # Return a list of the interpretation request IDs
    return request_id_df

def get_participant_id(ir_id):
    """
    Takes an interpretation request ID and returns participant ID from CIPAPI
    """
    # Use JellyPy to query CIP-API and get proband ID from the interpretation request ID. 
    return get_interpretation_request_list(interpretation_request_id=ir_id)[0]['proband']

def add_participant_id_to_df(request_id_df):
    """
    Takes a dataframe containing ir_id and adds participant ID from CIPAPI
    """
    request_id_df['Participant Id'] = request_id_df['ir_id'].apply(get_participant_id)
    print request_id_df

def query_geneworks(participant_ids):
    """
    Takes a list of GeL participant IDs and returns a dataframe containing patient information from Geneworks
    """
    # Connect to GW
    cnxn = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server}; SERVER=10.188.194.121; DATABASE=geneworks; UID=moka; PWD=moka", autocommit=True)
    # SQL for stored procedure to return all GMC participants (unfortanately cannot filter this on participant ID so need to return everything)
    sql = "EXEC SelectRegister_GMCParticipants_RegisterEntryDetails"
    # Execute SQL and return results in pandas dataframe
    gw_results = pandas.read_sql(sql,cnxn)
    # Fields that are required from geneworks results
    fields = ['PatientTrustID', 'LastName', 'FirstName', 'DoB', 'Participant Id']
    # Return rows that match the participant ids
    return gw_results[gw_results['Participant Id'].isin(participant_ids)][fields]

def main():
    # Get command line arguments
    args = process_arguments()
    # CSV input file containing interpretation request IDs in following format:
    # request_id, family_id
    # OPA-11585-1, 203351
    # OPA-11612-1, 266435
    # OPA-11636-1, 267035
    in_file = args.input_file
    # CSV file to write results to
    out_file = args.output_file
    # Convert input_file to dataframe, splitting request_id into seperate columns for cip, ir_id and version 
    ir_id_dataframe = get_ir_id_dataframe(in_file)
    # Use CIPAPI to find participant IDs and add to dataframe
    add_participant_id_to_df(ir_id_dataframe)
    # Query Geneworks using list of participant IDs from dataframe, returens a dataframe with results
    gw_results = query_geneworks(list(ir_id_dataframe['Participant Id']))
    # Merge dataframes with an outer join on 'partcipant_id'
    all_results = ir_id_dataframe.merge(gw_results, how='outer', on='Participant Id')
    # Write results to csv file
    all_results.to_csv(out_file, index=False)

if __name__ == '__main__':
    main()