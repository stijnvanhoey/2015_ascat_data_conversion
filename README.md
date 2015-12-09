# 2015_ascat_data_conversion
Small conversion function written to convert idx/dat files into .mat files. Written as a small tool for Hans Lievens.

In the notebook file, an introduction and analysis of the data handling is explored and explained. 

As such, a summarized function is written to provide the functionality from the command line:

            python convert_ascat.py ./ASCAT/1323 2301795

for an individual element, and

            python convert_ascat.py ./ASCAT/1322 all

To convert all available grid points in the dataset (assumed that your python file is in a folder containing the ASCAT data-folder with the .idx and .dat files)
