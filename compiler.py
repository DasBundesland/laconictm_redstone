from frontend import *

print("======================  COMPILING NQL TM  ======================")
NQLFrontend.gen_ir("sample_inputs/zf2.tm", True)
print("====================== COMPILING EXAMPLE LAC ======================")
LaconicFrontend.gen_ir("sample_inputs/example_tmd_dir.tm2", False)
print("====================== COMPILING FRIEDMAN LAC ======================")
LaconicFrontend.gen_ir("sample_inputs/friedman.tm2", False)
