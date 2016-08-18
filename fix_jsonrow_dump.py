import sys
import json

# A script to process a psql dump, change certain fields, and convert into a valid json file.  
# First dump from the psql command line via a \copy.
# For example, to extract the first 100 rows where col1 is null:
# \copy (SELECT row_to_json(t) FROM (select * from schema1.table1 where col1 is NULL limit 100) t) to 'file.dump';
# Finally, modify the field and value lists you'd like to alter in this file and run the script.

def convert_rowjson_docjson(line, position='middle'):
    if position == 'start':
        return '[' + line
    elif position == 'end':
        return ']'
    elif position == 'middle':
        return ',' + line
    else:
        raise ArgumentError('position must be start, middle or end: ', position)

def fix_jsonrow_dump(filename, field=[], value=[]):
    skip_count = 0
    with open(filename, 'r') as fp:
        for i,line in enumerate(fp):
            if i//1000 == i/1000.:
                print 'line #:', i
            try:
                line = unicode(line, "utf-8")
                # json_to_row encodes quotes as row: "\\"w\\""
                line = line.replace('\\\\"','')
                obj = json.loads(line)
            except ValueError:
                print 'ValueError:', line 
                print 'continuing without this record for debugging'
                skip_count += 1
            for f,v in zip(field, value):
                obj[f] = v
            yield obj
    print 'skip_count:',skip_count
    assert skip_count == 0


if len(sys.argv) != 3:
    print len(sys.argv)
    print 'usage:'+ sys.argv[0]+' input_file output_file'
    sys.exit(2)

if __name__ == '__main__':
    field = ['source_id']
    value = [-1]
    file_in = sys.argv[1]
    file_out = sys.argv[2]
    with open(file_out, 'w') as fp:
        position = 'start'
        for o in fix_jsonrow_dump(file_in, field, value):
            fp.write(convert_rowjson_docjson(json.dumps(o), position) + '\n')
            position = 'middle'
        position = 'end'
        fp.write(convert_rowjson_docjson('', position))
