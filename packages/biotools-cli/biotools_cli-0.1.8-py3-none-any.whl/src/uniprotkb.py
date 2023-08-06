import os
from ast import literal_eval
from multiprocessing import Pool
import click
import pandas as pd
from thefuzz import fuzz
from InquirerPy import inquirer
from Bio import SeqIO
from tqdm import tqdm


class UniProtKB:
    def __init__(self):
        self.uniprot_database = None

    @staticmethod
    def extract(infile, outfile, force):
        if not force and os.path.exists(outfile):
            proceed = inquirer.confirm(message="{} 已经存在，继续将覆盖它！是否继续？".format(outfile)).execute()
            if not proceed:
                return

        records = SeqIO.parse(infile, 'uniprot-xml')
        gene_names = list()
        protein_names = list()
        for record in tqdm(records, desc="正在提取基因和蛋白质名称"):
            gene_name = ""
            for gene_name_type in ['gene_name_primary',
                                   'gene_name_synonym',
                                   'gene_name_ordered locus',
                                   'gene_name_ORF']:
                if gene_name_type in record.annotations:
                    gene_name = record.annotations[gene_name_type]
                    if type(gene_name) == list:
                        gene_name = gene_name[0]
                    break
            if gene_name == "":
                continue

            protein_name = list()
            for protein_name_group in ['recommendedName_fullName',
                                       'submittedName_fullName',
                                       'alternativeName_fullName']:
                if protein_name_group in record.annotations:
                    protein_name.extend(
                        record.annotations[protein_name_group])

            gene_names.append(gene_name)
            protein_names.append(protein_name)

        pd.DataFrame({"g": gene_names, "p": protein_names}).to_csv(outfile, sep='\t', index=False, header=False)

    def match(self, protein_name):
        gene_name = ""
        for i, protein_names in enumerate(self.uniprot_database[1]):
            for v in literal_eval(protein_names):
                score = fuzz.token_sort_ratio(protein_name, v, full_process=False)
                if score == 100:
                    if len(gene_name) != 0:
                        gene_name += "/"
                    gene_name += self.uniprot_database[0][i]
                    break
        return gene_name

    def lookup(self, unifile, infile, outfile, force, processes):
        if not force and os.path.exists(outfile):
            proceed = inquirer.confirm(message="{} 已经存在，继续将覆盖它！是否继续？".format(outfile)).execute()
            if not proceed:
                return

        self.uniprot_database = pd.read_csv(unifile, sep='\t', keep_default_na=False, dtype=str, header=None)
        raw_df = pd.read_csv(infile, sep='\t', keep_default_na=False, dtype=str, header=None)
        unique_df = raw_df.copy().drop_duplicates()
        with Pool(processes=processes) as p:
            unique_df[1] = tqdm(p.imap(self.match, unique_df[0]), total=unique_df[0].count(), desc='去重匹配')
        for i in range(len(raw_df)):
            raw_df.at[i, 1] = unique_df.loc[unique_df[0] == raw_df.loc[i, 0]].values[0][1]
        raw_df[1].to_csv(outfile, sep='\t', index=False, header=False)


@click.group()
def uniprotkb():
    """
    基于 UniProtKB（XML格式）的蛋白质名称到基因名称的离线转换工具
    """
    pass


@uniprotkb.command(short_help="从 uniprot_sprot.tsv 文件中查找 protein.list 中蛋白质所对应的基因名，并保存到 gene.list 中")
@click.option("-f", "--force", is_flag=True, default=False, help="如果输出文件已经存在，直接覆盖而不提醒")
@click.option("-j", "--processes", type=int, default=None, help="并行处理进程数，默认为 os.cpu_count()")
@click.argument("unifile", required=True)
@click.argument("infile", required=True)
@click.argument("outfile", required=True)
def lookup(unifile, infile, outfile, force, processes):
    """
    biotools uniprotkb lookup uniprot_sprot.tsv protein.list gene.list

    UNIFILE：使用 extract 命令生成的 tsv 文件，例如：uniprot_sprot.tsv

    INFILE： 需要查找的蛋白质名称列表文件, 例如：protein.list

    OUTFILE：查找结果基因列表所保存的文件，例如：gene.list
    """
    UniProtKB().lookup(unifile, infile, outfile, force, processes)


@uniprotkb.command(short_help="提取 UniProtKB xml 文件中基因和蛋白质名称到 tsv 文件中")
@click.option("-f", "--force", is_flag=True, default=False, help="如果输出文件已经存在，直接覆盖而不提醒")
@click.argument("infile", required=True)
@click.argument("outfile", required=True)
def extract(infile, outfile, force):
    """
    biotools uniprotkb extract uniprot_sprot.xml uniprot_sprot.tsv

    INFILE： 本地保存的 UniProtKB xml 格式的数据库文件路径, 例如：uniprot_sprot.xml

    OUTFILE：用来保存提取的基因和蛋白质名称的输出文件 tsv 格式，例如：uniprot_sprot.tsv
    """
    UniProtKB.extract(infile, outfile, force)
