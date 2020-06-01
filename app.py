from bottle import route, run, static_file
from template import Template
from template.util import TemplateException
import os
from html import escape
import json

def render_template(template_name, template_data={}):
    template = Template({
        'ABSOLUTE': 1,
        'RELATIVE': 1,
        'INCLUDE_PATH': 'views/:.',
    })

    template_data['tmpl_vars'] = json.dumps(template_data, sort_keys=True, indent=2)
    template_data['template_content'] = read_template(template_name)

    try:
        page = template.process('views/' + template_name + '.tt', template_data)
        return page
    except TemplateException as e:
        print("ERROR: %s" % e)

def read_template(template_name):
    '''
    read in a template file and escape all html content
    '''

    with open('views/' + template_name + '.tt') as file:
        lines = file.read()

    # escape all the html, display the results
    escaped_lines = escape(lines, quote=True)

    return escaped_lines

@route('/test')
def test_route():

    file_suffix = 1
    for datum in [
        [ 'none', {} ],
        [ 'title', { 'page_title': 'My First Template' }, ],
        [ 'content', { 'value': ['this', 'that', 'the other'] }, ],
        ]:

        template_string = render_template('test/test_template', datum[1])

        # ensure any subdirs are created
        output_file = 'tmpl_output_' + datum[0] + '.txt'
        dir_path = os.path.dirname(output_file)
        with open(output_file, 'w') as f:
            f.write(template_string)

        file_suffix += 1

    return render_template('test/test_template')

@route('/narrative/static/style/style.min.css')
def style_min():
    return static_file('css/style.css', root='static')

@route('/narrative/static/kbase/css/kbaseStylesheet.css')
def kbaseStylesheet():
    return static_file('css/kbaseStylesheet.css', root='static')

@route('/static/<filename:path>')
# @route('/narrative/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')

@route('/')
@route('/index')
def index_route():
    return render_template('index')

@route('/view_template/<template_name:path>')
def view_template(template_name):

    tmpl_data = {
        'content': read_template(template_name),
        'page_title': template_name,
    }

    return render_template('starter_templates/template_content', tmpl_data)

def edge_data_cols():
  return [
    { 'data': 'node1',              'title': 'Source node' },
    { 'data': 'node2',              'title': 'Target node' },
    { 'data': 'edge',               'title': 'Edge weight' },
    { 'data': 'edge_descrip',       'title': 'Edge description' },
    { 'data': 'layer_descrip',      'title': 'Layer description' },
  ]

@route('/example/edge_data_object')
def edge_data_object():

    source_file = os.path.join('static', 'data', 'edge_data.json')
    with open(source_file, 'r') as read_fh:
        lines = read_fh.read().rstrip()

    json_data = json.loads(lines)

    tmpl_data = {
        'page_title': 'Edge Data Table, from an array of objects',
        'table_tab_title': 'Edge Data',
        'data_array': json_data,
        # our data is in the form of an array of objects with the key/value pairs that
        # appeared in the original file. To make it more viewer-friendly, remap the
        # names in the object to appropriate column headers
        'cols':       edge_data_cols(),
    }

    return render_template('example/edge_data', tmpl_data)

@route('/example/edge_data_array')
def edge_data_array():

    source_file = os.path.join('static', 'data', 'edge_data.tsv')

    # read in a file, splitting on '\n' and then '\t' to create a list of lists
    with open(source_file, 'r') as read_fh:
        lines = list(map(lambda x: x.split('\t'), read_fh.read().rstrip().split('\n')))

    tmpl_data = {
        'page_title': 'Edge Data Table, from an array of arrays',
        'table_tab_title': 'Edge Data',
        # lines[0] is the header line
        # the rest of the lines are the data points
        'data_array': lines[1:],
        # formatted column header names in the order they appear in the header line
        'cols': [
          { 'title': 'Source node' },
          { 'title': 'Target node' },
          { 'title': 'Edge weight' },
          { 'title': 'Edge description' },
          { 'title': 'Layer description' },
        ],
    }

    return render_template('example/edge_data', tmpl_data)

@route('/example/edge_data_tsv_file')
def edge_data_tsv_file():

    tmpl_data = {
      'page_title':       'Edge Table, data from a TSV file',
      'table_tab_title':  'Edge Data',
      'data_file':        '/static/data/edge_data.tsv',
      'data_file_format': 'tsv',
      'cols':             edge_data_cols(),
    }

    return render_template( 'example/edge_data_external_file', tmpl_data )

@route('/example/edge_data_json_file')
def edge_data_json_file():

    tmpl_data = {
      'page_title':       'Edge Table, data from a JSON file',
      'table_tab_title':  'Edge Data',
      'data_file':        '/static/data/edge_data.json',
      'data_file_format': 'json',
      'cols':             edge_data_cols(),
    }

    return render_template( 'example/edge_data_external_file', tmpl_data )

@route('/example/kb_uploadmethods_import_genbank')
def kb_uploadmethods_import_genbank():

    tmpl_data = {
        'upload_data': [
            ['Name', 'Escherichia_coli_str_K-12_MG1655 (55494/26/3)'],
            ['Date Uploaded', 'Sat Feb 22 19:08:55 2020'],
            ['Source', 'RefSeq'],
            ['ID', 'NC_000913.3'],
            ['Number of Contigs', 1],
            ['Size', 4641652 ],
            ['GC Content', '0.50791'],
            ['Warnings', ''],
            ['gene', 4498],
            ['CDS', 4319],
            ['misc_feature', 11],
            ['mobile_element', 49],
            ['ncRNA', 65],
            ['non_coding_features', 773],
            ['non_coding_genes', 179],
            ['protein_encoding_gene', 4319],
            ['rRNA', 22],
            ['rep_origin', 1],
            ['repeat_region', 355],
            ['tRNA', 89],
            ['tmRNA', 2]
        ],
        'contig_length': [
            ['NC_000913.3', 4641652],
        ]
    }

    return render_template('example/kb_uploadmethods_import_genbank', tmpl_data)


@route('/example/kb_trimmomatic')
def kb_trimmomatic():

    tmpl_data = {
        'page_content': [{
            'reference': '24019/8/1',
            'name': '37A_6437.3.44325.CTTGTA.adnq.fastq.gz_reads',
            'name_lc': 'ref_24019_8_1',
            'data': [
                { 'type': 'Input Read Pairs', 'raw': 47531383, 'perc': "100.0" },
                { 'type': 'Both Surviving', 'raw': 45736308, 'perc': "96.2" },
                { 'type': 'Forward Only Surviving', 'raw': 1095944, 'perc': "2.3" },
                { 'type': 'Reverse Only Surviving', 'raw': 579233, 'perc': "1.2" },
                { 'type': 'Dropped', 'raw': 119898, 'perc': "0.3" },
            ]
        },{
            'reference': '39639/4/1',
            'name': 'test-1.pe.reads',
            'name_lc': 'ref_39639_4_1',
            'data': [
                { 'type': 'Input Read Pairs', 'raw': 12500, 'perc': "100.0" },
                { 'type': 'Both Surviving', 'raw': 12500, 'perc': "100.0" },
                { 'type': 'Forward Only Surviving', 'raw': 0, 'perc': 0 },
                { 'type': 'Reverse Only Surviving', 'raw': 0, 'perc': 0},
                { 'type': 'Dropped', 'raw': 0, 'perc': 0 },
            ],
        }, {
            'reference': '29142/17/12',
            'name': 'doomed_to_fail.fastq.gz_reads',
            'name_lc': 'ref_29142_17_12',
        }]
    }

    return render_template('example/kb_trimmomatic', tmpl_data)


@route('/example/kb_trimmomatic_single')
def kb_trimmomatic_single():

    tmpl_data = {
        'page_content': [{
            'reference': '24019/8/1',
            'name': '37A_6437.3.44325.CTTGTA.adnq.fastq.gz_reads',
            'name_lc': 'ref_24019_8_1',
            'data': [
                { 'type': 'Input Read Pairs', 'raw': 47531383, 'perc': "100.0" },
                { 'type': 'Both Surviving', 'raw': 45736308, 'perc': "96.2" },
                { 'type': 'Forward Only Surviving', 'raw': 1095944, 'perc': "2.3" },
                { 'type': 'Reverse Only Surviving', 'raw': 579233, 'perc': "1.2" },
                { 'type': 'Dropped', 'raw': 119898, 'perc': "0.3" },
            ]
        }],
    }

    return render_template('example/kb_trimmomatic', tmpl_data)

@route('/starter_templates/<template_name>')
def default_route(template_name):
    return render_template( 'starter_templates/' + template_name )

@route('/example/<template_name>')
def default_route(template_name):
    return render_template('example/' + template_name)


run(host='localhost', port=9090, debug=True, reloader=True)
