import pymongo

ordered_labels = ['Approved Drug','Clinical Trial Drug','Experimental Drug',
'Food Ingredient or Additive','Human Metabolite','Cosmetic Ingredient',
'Agrochemical','Toxic Substance','Peptide','Bioactive Potent','Bioactive Moderate','Natural Product']
labels_order = {}
for i, label in enumerate(ordered_labels):
    labels_order[label] = i

page_size = 20

syn_num = 10

mongo_cfam = pymongo.MongoClient().cfam2017
mongo_mols = mongo_cfam.molecules
mongo_fams = mongo_cfam.families
mongo_vars = mongo_cfam.variables


