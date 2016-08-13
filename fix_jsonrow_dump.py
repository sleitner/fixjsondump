import sys
import json

def convert_rowjson_docjson(line, position='middle'):
    if position == 'start':
        return '[' + line + ','
    elif position == 'end':
        return ']'
    elif position == 'middle':
        return line + ','
    else:
        raise ArgumentError('position must be start, middle or end: ', position)

def overwrite_json_element(json_obj, field, value): 
    for i in range(len(json_obj)):
        json_obj[i][field] = value
    return json_obj

def fix_jsonrow_dump(filename):
    json_doc = ''
    position = 'start'
    with open(filename, 'r') as fp:
        for line in fp:
            json_doc += convert_rowjson_docjson(line, position=position)
            position = 'middle'
    json_doc = json_doc.rstrip(',')
    json_doc += convert_rowjson_docjson('', position='end')
    json_obj = json.loads(json_doc)
    return overwrite_json_element(json_obj, field='foo', value=0)


if len(sys.argv) != 3:
    print len(sys.argv)
    print 'usage:'+ sys.argv[0]+' input_file output_file'
    sys.exit(2)

file_in = sys.argv[1]
file_out = sys.argv[2]
with open(file_out, 'w') as fp:
    json.dump(fix_jsonrow_dump(file_in), fp)
