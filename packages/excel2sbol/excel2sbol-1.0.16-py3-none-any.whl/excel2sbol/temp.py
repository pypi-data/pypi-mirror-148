import excel2sbol.converter as conv
import os

cwd = os.getcwd()
print(cwd)
file_path_in = os.path.join(cwd, "excel2sbol", 'tests', 'test_files', 'flapjack_compiler_sbol3_v023.xlsx')
file_path_out = os.path.join(cwd, "excel2sbol", 'tests', 'test_files', 'out.xml')


conv.converter(file_path_in, file_path_out, sbol_version=2)
