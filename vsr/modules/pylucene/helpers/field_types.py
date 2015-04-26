from org.apache.lucene.document import FieldType
from org.apache.lucene.index import FieldInfo

def doc_id():
    f_type = FieldType()
    f_type.setNumericType(FieldType.NumericType.INT)
    f_type.setIndexed(False)
    f_type.setStored(True)
    f_type.setTokenized(False)
    f_type.setIndexOptions(FieldInfo.IndexOptions.DOCS_ONLY)

    return(f_type)

def abstract():
    f_type = FieldType()
    f_type.setIndexed(True)
    f_type.setStored(False)
    f_type.setTokenized(True)
    f_type.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)   

    return(f_type) 