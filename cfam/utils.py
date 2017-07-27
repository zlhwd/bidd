def _id2id(mongo_entry):
    mongo_entry['id'] = mongo_entry.pop('_id')
    if 'name' in mongo_entry:
        mongo_entry['show_name'] = mongo_entry['name']
    else:
        mongo_entry['show_name'] = mongo_entry['id']


def make_link(src,src_id):
    if src == 'PubChem':
        return 'https://pubchem.ncbi.nlm.nih.gov/compound/%s' % src_id
    elif src == 'ChEMBLdb':
        return 'https://www.ebi.ac.uk/chembl/compound/inspect/%s' % src_id
    elif src == 'ChEBI':
        return 'https://www.ebi.ac.uk/chebi/searchId.do?chebiId=%s' % src_id
    elif src == 'HMDB':
        return 'http://www.hmdb.ca/metabolites/%s' % src_id
    elif src == 'FooDB':
        return 'http://foodb.ca/compounds/%s' % src_id
    elif src == 'T3DB':
        return 'http://www.t3db.ca/toxins/%s' % src_id
    elif src == 'DrugBank':
        return 'https://www.drugbank.ca/drugs/%s' % src_id
    elif src == 'ZINC':
        return 'http://zinc15.docking.org/substances/%s/' % src_id
    elif src == 'TTD':
        return 'http://bidd.nus.edu.sg/BIDD-Databases/TTD/ZFTTDDRUG.asp?ID=%s' % src_id
    elif src == 'CosIng':
        return 'http://ec.europa.eu/growth/tools-databases/cosing/index.cfm?fuseaction=search.details_v2&id=%s' % src_id
    elif src == 'PPDB':
        return 'http://sitem.herts.ac.uk/aeru/ppdb/en/Reports/%s.htm' % src_id
    elif src == 'BPDB':
        return 'http://sitem.herts.ac.uk/aeru/bpdb/Reports/%s.htm' % src_id
    elif src == 'VSDB':
        return 'http://sitem.herts.ac.uk/aeru/vsdb/Reports/%s.htm' % src_id
    elif src == 'SuperNature':
        return 'http://bioinf-applied.charite.de/supernatural_new/index.php?site=compound_input'


import json

def make_pie_json(mols):
    label_count = {}
    for mol in mols:
        label_count.setdefault(mol['label'],set()).add(mol['id'])
    pie_data = [['label','count']]
    pie_data += [[k,len(v)] for k,v in label_count.iteritems()]
    return json.dumps(pie_data)