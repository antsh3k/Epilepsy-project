from medcat.cat import CAT
from medcat.utils.vocab import Vocab
from medcat.prepare_cdb import PrepareCDB
from medcat.cdb import CDB
import os
from medcat.utils.helpers import *

# load the vocab
# vocab = Vocab()
# vocab.load_dict(os.path.join("F:/", "snomed.dat"))

cdb = CDB()
cdb.load_dict(os.path.join("F:/", "snomed.dat"))
print(cdb.cui2pretty_name['S-84757009'])

file = r"C:\Users\k1767582\Documents\GitHub\Epilepsy-project\20200114medcatoutput.csv"






