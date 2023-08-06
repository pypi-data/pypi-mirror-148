Package: SJM_tools

Author: Jianheng Liu

License: MIT

Description: This package is used for manage SJM jobs. Check https://jhfoxliu.github.io/projects/tools_1_sjm/ for better presentation of the workflow.

(1) Import the package

import from sjm_tools import job,check_env

(2) Check environments (file/path/prefix)

ref_genome = check_env("/share/public1/data/liujh/database/mouse/ensembl_release102/genome/Mus_musculus.GRCm38.dna_sm.primary_assembly.format.fa")

ref_genome_index = check_env("/share/public1/data/liujh/database/mouse/ensembl_release102/BS_index/hisat2_index/",is_path=True)

bowtie2_index = check_env("/share/public1/data/liujh/database/mouse/ensembl_release102/BS_index/bowtie2_index/Mus_musculus.GRCm38.allrna.format.c2t",is_prefix=True)

(3) Set up a JOB object

JOB = job(workpath, SJM_file_name)

(4) Add a STEP to a JOB

JOB.step_start(step_name="QC",memory="50G")

(5) Add a process to a STEP (repeat this for multiple process in a JOB)

JOB.add_process("{java} -jar {trimmomatic} PE -threads 2 -phred33 read1.cutadapt.fastq read2.cutadapt.fastq rev.fastq rev.UP.fastq fwd.fastq fwd.UP.fastq HEADCROP:10 SLIDINGWINDOW:4:22 AVGQUAL:25 MINLEN:40".format(java=java,trimmomatic=trimmomatic))

(6) End adding a STEP

JOB.step_end()

(7) Repeat (4) to (6) for multiple steps

(8) When everything is added, finish the JOB

JOB.job_finish()

(9) If you want to submit the job automatically

JOB.submit()