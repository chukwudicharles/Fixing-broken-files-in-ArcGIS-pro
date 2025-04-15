import arcpy
import logging
import csv
import os

def fix_aprx_connections(aprx_path, old_connection, new_connection):
    """Fixes broken connections in a single APRX file."""
    try:
        aprx = arcpy.mp.ArcGISProject(aprx_path)
        if old_connection:  # Check if old_connection is not empty
            logging.info(f"Replacing {old_connection} with {new_connection} in {aprx_path}")
            aprx.updateConnectionProperties(old_connection, new_connection, validate=False)
        aprx.save()
        logging.info(f"Saved APRX: {aprx_path}")
        del aprx
        return True  # Indicate successful change.
    except Exception as e:
        logging.error(f"Error processing APRX {aprx_path}: {e}")
        return False  # Indicate failure

def main(aprx_folder, sde_csv_path):
    """Main function to process APRX files in a folder, using the last row of the CSV."""

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Load the last SDE connection path from CSV
        old_connection = None # to initialize the variable. Nb it's connection path isn't specified, as it (both old and new connection) are contained in the sde_csv_file, and both are called from there
        new_connection = None

        if os.path.exists(sde_csv_path):
            with open(sde_csv_path, mode="r") as csvFile:
                reader = list(csv.reader(csvFile)) # Read csv file
                if reader:  # Check if the CSV file is not empty
                    last_row = reader[-1] # because we are only interested to fix the last row of the sde_csv
                    if len(last_row) >= 2: # Check if the last row has at least two columns
                        old_connection = last_row[0]
                        new_connection = last_row[1]
                    else:
                        logging.warning("Last row of CSV does not have two columns.")
                        return
                else:
                    logging.warning("CSV file is empty.")
                    return
        else:
            logging.error(f"SDE CSV file not found: {sde_csv_path}")
            return

        # Find all APRX files in the specified folder
        aprx_files = []
        for filename in os.listdir(aprx_folder):
            if filename.lower().endswith(".aprx"):
                aprx_files.append(os.path.join(aprx_folder, filename))

        if not aprx_files:
            logging.info(f"No APRX files found in: {aprx_folder}")
            return

        # Process each APRX file
        for aprx_path in aprx_files:
            fix_aprx_connections(aprx_path, old_connection, new_connection) # Replace  old connection path with the new connection path, to fix the broken file issue
                                                                            # The broken file issue might be due to the file been moved to a new location, renamed, replaced or removed.
                                                                            # By prompting for the new paths, the script can update the layer's connection properties to point to the correct data source


    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Call Main script:
if __name__ == "__main__":
    aprx_folder_path = r"\\gisfileintprd\TeamWorkSpaces\iCapture\RegionSchemes\Amdts\MRS\MRS_4973\Version1\Amending Plans"  # Replace with your APRX folder path
    sde_csv_file_path = r"C:\Users\charles.owuama\Downloads\SdeConnectionPaths_NEC_UAT_to_NEC_PROD.csv" # Replace with your CSV file path
    main(aprx_folder_path, sde_csv_file_path)