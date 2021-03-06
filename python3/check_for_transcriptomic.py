import urllib.request
import os.path, sys, getopt

is_short_paired=0
is_short_single=0
is_pacbio=0
is_onp=0

class text:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

opts, args = getopt.getopt(sys.argv[1:],"ht:",["taxon_id="])
if not opts:
    print("\nProgram: check_for_transcriptomic (check ENA for transcriptomic data)\nVersion: 1.0\n\nUSAGE:\ncheck_for_transcriptomic  -t <taxon_id> [options]\n\n-h\tShow this help and exit\n")
    sys.exit()

for opt, arg in opts:
    if opt == '-h':
        print("\nProgram: check_for_transcriptomic (check ENA for transcriptomic data)\nVersion: 1.0\n\nUSAGE:\ncheck_for_transcriptomic  -t <taxon_id> [options]\n\n-h\tShow this help and exit\n")
        sys.exit()
    elif opt in ("-t", "--taxon_id"):
       taxon_id = arg

short_paired_page = urllib.request.urlopen("https://www.ebi.ac.uk/ena/portal/api/search?display=report&query=%22tax_eq(" +str(taxon_id)+ ")%20AND%20instrument_platform=ILLUMINA%20AND%20library_layout=PAIRED%20AND%20library_source=TRANSCRIPTOMIC%22&domain=read&result=read_run&fields=run_accession,read_count")
short_paired_list = short_paired_page.readlines()
if len(short_paired_list) > 0:
   short_paired_list.pop(0)
   is_short_paired = 1
   short_paired_runs = len(short_paired_list)

short_single_page = urllib.request.urlopen('https://www.ebi.ac.uk/ena/portal/api/search?display=report&query=%22tax_eq('+str(taxon_id)+')%20AND%20instrument_platform=ILLUMINA%20AND%20library_layout=SINGLE%20AND%20library_source=TRANSCRIPTOMIC%22&domain=read&result=read_run&fields=run_accession,read_count')
short_single_list = short_single_page.readlines()
if len(short_single_list)> 0:
   short_single_list.pop(0)
   is_short_single = 1
   short_single_runs = len(short_single_list)

pacbio_read_page = urllib.request.urlopen('https://www.ebi.ac.uk/ena/portal/api/search?display=report&query=%22tax_eq('+str(taxon_id)+')%20AND%20instrument_platform=PACBIO_SMRT%20AND%20library_source=TRANSCRIPTOMIC%22&domain=read&result=read_run&fields=run_accession,read_count')
pacbio_read_list = pacbio_read_page.readlines()
if len(pacbio_read_list)> 0:
   pacbio_read_list.pop(0)
   is_pacbio = 1
   pacbio_read_runs = len(pacbio_read_list)

onp_read_page = urllib.request.urlopen('https://www.ebi.ac.uk/ena/portal/api/search?display=report&query=%22tax_eq('+str(taxon_id)+')%20AND%20instrument_platform=OXFORD_NANOPORE%20AND%20library_source=TRANSCRIPTOMIC%22&domain=read&result=read_run&fields=run_accession,read_count')
onp_read_list = onp_read_page.readlines()
if len(onp_read_list)> 0:
   onp_read_list.pop(0)
   is_onp = 1
   onp_read_runs = len(onp_read_list)

if is_short_paired:
   print (text.BOLD+"Short-read paired-end illumina data available! "+text.END+"Found "+str(short_paired_runs)+" runs.")

if is_short_single:
   print (text.BOLD+"Short-read single-end illumina data available! "+text.END+"Found "+str(short_single_runs)+" runs.")

if is_pacbio:
   print (text.BOLD+"Long-read PacBio data available! "+text.END+"Found "+str(pacbio_read_runs)+" runs.")

if is_onp:
   print (text.BOLD+"Long_read ONP data available! "+text.END+"Found "+str(onp_read_runs)+" runs.")
