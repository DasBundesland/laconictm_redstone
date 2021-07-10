from frontend import *

file = "sample_inputs/zf2.tm"
print("======================  COMPILING NQL TM  ======================")
NQLFrontend.gen_ir(file, False)
print("======================COMPILING LACONIC TM======================")
LaconicFrontend.gen_ir("sample_inputs/example_tmd_dir.tm2", False)
