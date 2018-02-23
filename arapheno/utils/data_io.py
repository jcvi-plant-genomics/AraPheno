from datetime import datetime
import csv
import ontology_parser
import scipy as sp

'''
Accession Class
'''
class AccessionClass(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.country = None
        self.source = None
        self.category = None
        self.status = None
        self.population = None
        self.line = None
        self.cs_number = None
        self.species = None

    def to_dict(self):
        fields = {'name':self.name,'country':self.country}
        return {'model':'phenotypedb.Accession','pk':self.id,'fields':fields}


'''
Parse a country-codes map and creates a dictionary with the passed in key as key
'''
def parse_country_map(filename,key='ISO3166-1-Alpha-3'):
    map = {}
    with open(filename,'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            map[row[key]] = row['name']
    return map

'''
Parse Accession File Including Meta-Information (e.g. 1001 Genomes Master Table)
Input: filename: filename of accession file
Output: accession list: list of accession classes
'''
def parseAccessionFile(filename=None, species=1):
    if filename==None:
        return None
    accession_list = []
    with open(filename,'r') as f:
        reader = csv.reader(f,delimiter='\t')
        header = reader.next()
        if header != ['name','line','population','country','category','source','status']:
            raise Exception('header must be of form %s' % header)
        for row in reader:
            accession = AccessionClass()
            accession.name = row[0]
            accession.id = int(accession.name.lstrip('HM'))
            try:
                accession.line = row[1]
            except:
                pass
            try:
                accession.population = row[2]
            except:
                pass
            try:
                accession.country = row[3]
            except:
                pass
            try:
                accession.category = row[4]
            except:
                pass
            try:
                accession.source = row[5]
            except:
                pass
            accession.status = row[6]
            accession_list.append(accession)
            accession.species = species
    return accession_list


def convertAccessionsToJson(accessions,country_map = {}):
    accession_dict = []
    if country_map is None:
        country_map =  {}
    for acc in accessions:
        country = country_map.get(acc.country,acc.country)
        fields = {'name':acc.name,'country':country,'source':acc.source,
        'category':acc.category,'status':acc.status,'line':acc.line,'population':acc.population,'species':acc.species}
        acc_dict = {'model':'phenotypedb.Accession','pk':acc.id,'fields':fields}
        accession_dict.append(acc_dict)
    return accession_dict

'''
Parse Phenotype File in PLINK format
Input: filename: filename of phenotype file
Output: phenotype_matrix: accession_ids x phenotypes (or replicates)
        accession_ids: scipy array of accession ids
        names: phenotype or replicate names
'''
def parse_plink_file(f):
    #Parse file
    if not hasattr(f, 'read'):
        f = codecs.open(f,'rU',encoding='utf-8')
    try:
        accession_ids = []
        pmatrix = []
        names = None
        split_delimiter = " "
        reader = csv.reader(f,delimiter=split_delimiter)
        for i,line in enumerate(reader):
            if i==0:
                if len(line)==1:
                    reader = csv.reader(f,delimiter='\t')
                    line = next(reader)
                    if len(line)==1:
                        raise Exception("Wrong file format")
                names = map(lambda s: s.replace("_"," "),line[2:])
            else:
                accession_ids.append(line[0].strip())
                pmatrix.append(map(lambda x: sp.nan if x == '' else float(x),line[2:]))
        accession_ids = sp.array(accession_ids)
        pmatrix = sp.array(pmatrix)
        return [pmatrix,accession_ids,names]
    except Exception as error:
        raise error
    finally:
        if f is not None:
            f.close()


'''
Parse an Ontology file as a dictionary
Input: filename: filename of the ontology file
Output: List of ontology terms
'''
def parse_ontology_file(filename):
    return ontology_parser.parseGOOBO(filename)

'''
Converts ontologies to fixture format
'''
def convert_ontologies_to_json(ontologies,ontology_source):
    source_map = {'TO':1,'EO':2,'UO':3}
    source_id = source_map[ontology_source]
    ontology_dict = []
    for ontology in ontologies:
        fields = {'name':ontology['name'],'definition':ontology.get('def',None),'comment':ontology.get('comment',None),'source_id':source_id}
        ont_dict = {'model':'phenotypedb.OntologyTerm','pk':ontology['id'],'fields':fields}
        ontology_dict.append(ont_dict)
    return ontology_dict
