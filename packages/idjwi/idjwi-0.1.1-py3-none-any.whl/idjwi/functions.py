# Importing necessary libraries
import pandas as pd, os

class open_data:

	def __init__(self, file_source):
		self.file_source = file_source

	def csv_excel(self, file_source):
		"""
		This function is used to open csv and Excel files
		ursus
		:param file_source: is where you put your file path directory
		:type file_source: str

		:return: Dataframe
		:rtype: Dataframe
		"""
		try:
			file_name, file_extension = os.path.splitext(file_source)
			if file_extension =='.csv':
				data = pd.read_csv(file_source, sep=';')
				return data
			elif file_extension =='.xlsx':
				data = pd.read_excel(file_source)
				return data
			else:
				print('Check Your Source')
		except FileNotFoundError:
			print('Check your file directory and try again')
open_data = open_data('file_soucre.csv')

