33 calls to ntt;
14 calls to invntt;
375 calls to keccak;
I made some changes in the code to make the calls to the Keccak in the gem5/gem5-Aladdin consistent with the native execution. **Almost all the probelms of keccak is related to the sampling a polynomial!!!**

# Summary of the README: generate DSE related files and run DSE: ################
```
bash run-gen-trace-bin-dse.sh
cd kyber512 && sh run-all-version.sh
cd kyber768 && sh run-all-version.sh
cd kyber1024 && sh run-all-version.sh
```


########################################################


updated README.md can be found [here](https://github.com/Hamidu68/gem5-aladdin/tree/master/dse_scripts)
Place `Makefile` and `run-gen-trace-bin-dse.sh` and `src`, source files of the benchmark, in the same directory.
# file and folders description:
## run-gen-trace-bin-dse.sh
By running `bash run-gen-trace-bin-dse.sh`, as below, trace files, input binary files for gem5 and gem5-Aladdin, DSE related files and Elastic search files are generated in folder with the name of the test, ex: kyber512; in that folder two subfolder, `base` and `opt` will be generated:

```
base # Original code without any algorithmtic changes
opt  # loop transformation have been done in this version
```
More detailed on the `base` and `opt` version can be found [here](). Lets look at `base` folder for `kyber512` with 3 accelerators named `ntt`, `invntt`, and `KeccakF1600_StatePermute`; it has below some folder and two `.sh` file:
-	*bin*: includes `[ACCEL]-gem5` and `[ACCEL]-gem5-accel` which will be used in DSE as the inputs of gem5 and gem5-Aladdin;
	-[ACCEL] is the accelerator that we want to peform DSE on. List of the accelerators are specified in `run-gen-trace-bin-dse.sh` file.
		-[ACCEL]=ntt,invntt, KeccakF1600_StatePermute
-	*trace*: includes [ACCEL].gz, trace files, of the accelerator. [ACCEL]=ntt,invntt, KeccakF1600_StatePermute
-	*dse-[ACCEL], ex: dse-ntt* : inclue all the neccassary files to perform DSE. More information of DSE can be found [here](DSE: template+parse stats)
-	*run-all-dse.sh*: call `run-dse.sh` in each of the `dse-[ACCEL]` folders. 
-	*run-all-elastic.sh*: call `run-elastic.sh` in each of the `dse-[ACCEL]` folders. 

## Makefile
This makefile generates the trace and binary files. In the case of kyber,  we want to generate files for two different version that only differ in `ntt.c and ntt-base.c` where `ntt-base` is the original implementation and `ntt.c` is our version of ntt. 
This is how we generate the trace file for a kernel. 
-      `KERNEL`: exact name of the annotated function in the C file [link]()
-      `KERNEL_ID`: id of the accelerator in the invokation function [link]()
-      `VERSION`: version of the code we want to analyze. 
-      `DUMP_ACCEL_STATS`: 1: we need stats of the accelerator; 0: we just need stats of the scheme. (just used in gem5-Aladdin).

```
make run-trace KERNEL=invntt KERNEL_ID=16777217 VERSION=opt  #generate the dynamic trace file (ex: ntt.gz)
```
and to generate the binary files: 
```
make gem5 KERNEL=invntt KERNEL_ID=16777217 VERSION=opt DUMP_ACCEL_STATS=1  ##generate the binary files for gem5 (i.e., just CPU; ex: kyber-gem5) and gem5-aladdin(i.e., CPU+accel; ex: kyber-gem5-accel)
```
#dse
Contains templates, files with `-template` postfix, and scripts to perform the DSE. *template files are filled by `dse.py`*
-	`cacti_cache-template.cfg`: tempalte file that is use to calculate power of the accel's cache
-	`cacti_tlb-template.cfg`: tempalte file that is use to calculate power of the accel's TLB
-	`dse.py`: gets sweeping parameters and sweept them using `Sweeper.py`.
-	`gem5-template.cfg`: template for micro-architectural configs of the accelerator
-	`[ACCEL]-tempate.cfg ,ex: kyber-template.cfg`: other design paramters such as `loop unrolling` and `loop pipelining` in addition to allocation of arrays in cache or SPM
-	`parse_stats.py`: gem5-Aladdin dumps lots of data and this python file parse them and generate per accelerator in both client and the server. This python file is called in `run.sh` shell script.
-	`run-gem5-tempalte.sh`: template file that runs the benchmark on X86 (no accelerator is attached). *CPU and accelerator have the same cache line size and bus width;* these two paramters are sweepted for the base line.
-	`run-tempalte.sh`: shell file to call the gem5 and gem5-Aladdin. 
-	`Sweeper.py`: sweep the paramters with values specified in `dse.py`


#Peform the DSE:
In the [VER] folder, e.g. opt, we have two shell files:

-	`run-all-dse.sh`: DSE for all the accelerators (gem5-Aladdin) plus baseline (gem5) are performed.
-	`run-all-elastic.sh`: all the results for the DSE of the accels are pushed to Kibana; *TODO*: make kibana portable!


#Separation of Client and the Server:
we should use `m5_dump_stats(0,0)` in the main file after each function to be able to separate client from the server. ex [link](https://github.com/Hamidu68/aladdin/commit/6f14e71fd7dcc21a2fb822ed2b330ba4d13e0cb5?diff=unified#diff-c33f6208160dce8538a7d99683ef97fe)
After annotating the code, we should change  the last line of the [run-template.sh](gem5-aladdin/dse_scripts/sweep+dse/run-template.sh) that calls [parse_stats.py](gem5-aladdin/dse_scripts/sweep+dse/parse_stats.py) as below:

```
python parse_stats.py {OUT_DIR} ntt:1 invntt:2 #keccak:3
```
*in this example two accels are attached to the bus so ntt and invtt are passed to parse_stats.py; usuallay we peform the DSE one accelerator at a time so perhaps you will se only one accelerator to be passed in most of cases.*

the script will parse `stats.txt` and `ntt_summary` and `invntt_summary` and generate below files:

- *invntt_summary_client.json* : summary of invntt's accelerator stats for the client side (Accelerator)
- *invntt_summary_server.json* : summary of invntt's accelerator stats for the server  side (Accelerator)
- *ntt_summary_client.json*    : summary of ntt's accelerator stats for the client  side (Accelerator) 
- *ntt_summary_server.json*    : summary of ntt's accelerator stats for the server  side (Accelerator)
- *stats_server.txt* : merge all the dumped stats inside the client code (CPU + Accelerator)
- *stats_client.txt* : merge all the dumped stats inside the server code (CPU + Accelerator)
- *power-mcpat_client.txt* : total power consumption of host CPU for the client side (CPU)
- *power-mcpat_server.txt* : total power consumption of host CPU for the server side (CPU)
- *power_cpu_plus_accel_client.txt* : total power consumption of system for the client side (CPU + Accelerator)
- *power_cpu_plus_accel_server.txt* : total power consumption of system for the server side (CPU + Accelerator)


This how we annotate the code in the main function [e.g., Kyber](aladdin/integration-test/with-cpu/kyber/non-seprated/kyber_poly/src/test_kyber.c) which will be used in [parse_stats.py](gem5-aladdin/dse_scripts/sweep+dse/parse_stats.py) to separate client and the server.
```
 //Alice generates a public key
#if !defined(LLVM_TRACE)
    m5_reset_stats(0,0);
    crypto_kem_keypair(pk, sk_a);
    m5_dump_stats(0,0);
    m5_mynewop(SERVER,1);
#else
    crypto_kem_keypair(pk, sk_a); /*server*/
#endif

    //Bob derives a secret key and creates a response
#if !defined(LLVM_TRACE)
    crypto_kem_enc(sendb, key_b, pk);
    m5_dump_stats(0,0);
    m5_mynewop(CLIENT,1);
#else
    crypto_kem_enc(sendb, key_b, pk); /*client*/
#endif

#if !defined(LLVM_TRACE)
    //Alice uses Bobs response to get her secret key
    crypto_kem_dec(key_a, sendb, sk_a);
    m5_dump_stats(0,0);
    m5_mynewop(SERVER,1);
#else
    crypto_kem_dec(key_a, sendb, sk_a); /*client*/
#endif

``` 

#Accelerator invocation
to be added!
-----------------------------------------------------------------------
~~**NEW**~~

accelerator for keccak is attached to the cpu; use below:
```
make clean-gem5
make gem5 ACCEL=3
python dse.py
```
at the end, keys are established successfully. total cycle of the whole scheme withou accelerator is 2094169 and with the accelerator is 1998580 which means around 5% of improvement.


if you want to attach all the three accels, type:
```
sh run-trace-dse.sh
```
when all the accelerator are connected, total cycle would be 1200735 which is 42% improvement  in the performance.


we generate the traces for each workload (ntt and invntt here) which will be used in the future to be attached to the host CPU. We will access the output traces (ntt.gz and invntt.gz) and point to them in the gem5-template.cfg

how to get traces:

```
sh run_traces.sh
```
We will have two output folders. test-traces-mine and test-traces-base which has ntt.gz and invntt.gz for baseline and merged loops, respectively.

now generate the `-gem5` and `-gem5-accel` file run the DSE by:
```
sh run-dse.sh
```
which calls dse and calcualte the total power/area/cycles in the accelerator by 

```
python dse.py
python $GEM5_HOME/power-whole-system-mcpat-x86/power_core_plus_accel.py tests
```


or all can be done by:

```
sh run-trace-dse.sh
```

if you want to check sanity of accelerator, set DUMP_ACCEL_STATS to be one in `run-dse.sh` and run `run-sanity-check.sh`.

**Note**: 
at the end of the running the gem5-Aladdin, `parse_stats.py` is called which parse `stats.txt` file and generate below files:
- *accel-client-stats.txt*  : individual of all the dumped stats inside the accelrators of the client code (Accelerator) 
- *accel-server-server.txt* : individual of all the dumped stats inside the accelrators of the server code (Accelerator) 
- *merged-accel-client-stats.txt* : merge all the dumped stats inside the accelrators of the client code (Accelerator)
- *merged-accel-server-stats.txt* : merge all the dumped stats inside the accelrators of the server code (Accelerator)
- *stats-server.txt* : merge all the dumped stats inside the client code (CPU + Accelerator)
- *stats-client.txt* : merge all the dumped stats inside the server code (CPU + Accelerator)

by running `run-sanity-check.sh` you can compare the parsed result with `stats.txt`.



**NOTES**:

TLB page size:256 bytes.
TLB page size is the size of a page in your simulation. We usually use 4KB pages. 
Each page table entries is pointing to a page table of the memory. If memory is 4GB, each entry is 32 bits (4 bytes) 
We have usually 64 tlb entries (gem5-aladdin examples) hence size of tlb (in cacti config file) is 4*64=256 . 
