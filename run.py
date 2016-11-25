import os


os.system("sudo perf record -e cycles:u,instructions:u,cache-references:u,cache-misses:u -g -c 1000 ../test/test_newhope")
os.system("sudo perf report -n > All_Data")
os.system("python extract-data.py")