import os
# from cvmblaster.blaster import Blaster
from Bio.Blast.Applications import NcbimakeblastdbCommandline
from Bio.Blast.Applications import NcbiblastnCommandline


db = '/Users/cuiqingpo/Downloads/blast_db/resfinder'

input = "/Users/cuiqingpo/Downloads/resblaster/17BJBY25.fa"
output = "temp.xml"


class Blaster():
    def __init__(self, inputfile, database, output, threads, minid=90, mincov=60):
        self.inputfile = os.path.abspath(inputfile)
        self.database = database
        self.minid = int(minid)
        self.mincov = int(mincov)
        self.temp_output = os.path.join(os.path.abspath(output), 'temp.xml')
        self.threads = threads

    def biopython_blast(self):
        hsp_results = {}
        cline = NcbiblastnCommandline(query=self.inputfile, db=self.database, dust='no',
                                      evalue=1E-20, out=self.temp_output, outfmt=5,
                                      perc_identity=self.minid, max_target_seqs=50000,
                                      num_threads=self.threads)
        # print(cline)
        # print(self.temp_output)

        stdout, stderr = cline()

        result_handler = open(self.temp_output)

        blast_records = NCBIXML.parse(result_handler)
        df_final = pd.DataFrame()

        for blast_record in blast_records:

            # if blast_record.alignments:
            #     print("QUERY: %s" % blast_record.query)
            # else:
            #     for alignment in blast_record.alignments:
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    strand = 0
                    query_name = blast_record.query
                    # print(query_name)
                    target_gene = alignment.title.split(' ')[1]

                    # Get gene name and accession number from target_gene
                    gene = target_gene.split('_')[0]
                    accession = target_gene.split('_')[2]

                    # print(target_gene)
                    sbjct_length = alignment.length  # The length of matched gene
                    # print(sbjct_length)
                    sbjct_start = hsp.sbjct_start
                    sbjct_end = hsp.sbjct_end
                    gaps = hsp.gaps  # gaps of alignment
                    query_string = str(hsp.query)  # Get the query string
                    identities_length = hsp.identities  # Number of indentity bases
                    # contig_name = query.replace(">", "")
                    query_start = hsp.query_start
                    query_end = hsp.query_end
                    # length of query sequence
                    query_length = len(query_string)

                    # calculate identities
                    perc_ident = (int(identities_length)
                                  / float(query_length) * 100)
                    IDENTITY = "%.2f" % perc_ident
                    # print("Identities: %s " % perc_ident)

                    # coverage = ((int(query_length) - int(gaps))
                    #             / float(sbjct_length))
                    # print(coverage)

                    perc_coverage = (((int(query_length) - int(gaps))
                                      / float(sbjct_length)) * 100)
                    COVERAGE = "%.2f" % perc_coverage
                    # print("Coverage: %s " % perc_coverage)

                    # cal_score is later used to select the best hit
                    cal_score = perc_ident * perc_coverage

                    # Calculate if the hit is on minus strand
                    if sbjct_start > sbjct_end:
                        temp = sbjct_start
                        sbjct_start = sbjct_end
                        sbjct_end = temp
                        strand = 1

                    if strand == 0:
                        strand_direction = '+'
                    else:
                        strand_direction = '-'

                    if perc_coverage >= self.mincov:
                        hit_id = "%s:%s_%s:%s" % (
                            query_name, query_start, query_end, target_gene)
                        # hit_id = query_name
                        # print(hit_id)
                        best_result = {
                            'FILE': os.path.basename(self.inputfile),
                            'SEQUENCE': query_name,
                            'GENE': gene,
                            'START': query_start,
                            'END': query_end,
                            'SBJSTART': sbjct_start,
                            'SBJEND': sbjct_end,
                            'STRAND': strand_direction,
                            # 'COVERAGE':
                            'GAPS': gaps,
                            "%COVERAGE": COVERAGE,
                            "%IDENTITY": IDENTITY,
                            # 'DATABASE':
                            'ACCESSION': accession,
                            'cal_score': cal_score,
                            'remove': 0
                            # 'PRODUCT': target_gene,
                            # 'RESISTANCE': target_gene
                        }
                    print(best_result)


Blaster(input, db, output, 8).biopython_blast()

# help(Blaster)
# output = "~/Downloads/test_genome/test"
# if not os.path.exists(output):
#     os.mkdir(output)
# # outpath = os.path.abspath(output)
# print(output)


# # print(os.path.abspath('~/Downloads/test_genome/test'))


# test = Blaster(input, db, output, 8, ).biopython_blast()

# print(test)


# db_file = '/Users/cuiqingpo/Downloads/blast_db/all.fsa'
# name = '/Users/cuiqingpo/Downloads/blast_db/resfinder'


# def initialize_db():
#     database_path = os.path.join(
#         os.path.dirname(__file__), f'db')
#     for file in os.listdir(database_path):
#         if file.endswith('.fsa'):
#             file_path = os.path.join(database_path, file)
#             file_base = os.path.splitext(file)[0]
#             out_path = os.path.join(database_path, file_base)
#             Blaster.makeblastdb()


# def makeblastdb(file, name):
#     cline = NcbimakeblastdbCommandline(
#         dbtype="nucl", out=name, input_file=file)
#     stdout, stderr = cline()


# print('Start')
# makeblastdb(db_file, name)
