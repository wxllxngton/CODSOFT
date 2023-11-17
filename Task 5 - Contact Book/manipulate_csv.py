import csv

class CSVThings:
    def __init__(self, file_path):
        """
        Initialize CSVThings with the given file path.

        Parameters:
        - file_path (str): The path to the CSV file.

        Returns:
        - None
        """
        self.file_path = file_path
        with open(self.file_path) as csv_file:
            self.csvreader = csv.reader(csv_file)
            self.header = next(self.csvreader)
            self.data = [row for row in self.csvreader]

    def add_record_to_csv(self, record):
        """
        Add a record to the CSV file.

        Parameters:
        - record (list): The record to be added as a list of values.

        Returns:
        - None
        """
        with open(self.file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(record)

    def overwrite_csv(self, data):
        """
        Overwrite the entire CSV file with new data.

        Parameters:
        - data (list): The new data to be written to the CSV file.

        Returns:
        - None
        """
        with open(self.file_path, 'w+', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(self.header)
            csv_writer.writerows(data)

    def delete_record_from_csv(self, records):
        """
        Deletes a record(s) from the CSV file.

        Parameters:
        - records (list of lists): The record(s) to be deleted as a list of lists of values.

        Returns:
        - None
        """
        updated_data = [row for row in self.data if row not in records]
        self.overwrite_csv(updated_data)


    def update_record_in_csv(self, original_record, record):
        """
        Updates a record in the CSV file.

        Parameters:
        - original_record (list): The record to be updated as a list of values.
        - record (list): The record to be updated as a list of values, now with the updated values.

        Returns:
        - None
        """
        updated_data = [record if row == original_record else row for row in self.data]
        self.overwrite_csv(updated_data)
