from bottle import route, run, static_file
from template import Template
from template.util import TemplateException


def render_template(template_name, template_data={}):
    template = Template({
        ABSOLUTE: 1,
        INCLUDE_PATH: 'views/:.',
        TRIM: 1,
    })
    try:
        page = template.process('views/' + template_name + '.tt', template_data)
        return page
    except TemplateException as e:
        print("ERROR: %s" % e)


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')


@route('/')
@route('/index')
def index_route():
    return render_template('index')


# @route('/starter_templates/<template_name>')
# def default_route(template_name):
#     return render_template( template_name )


@route('/example/kb_uploadmethods_import_genbank')
def kb_uploadmethods_import_genbank():

    tmpl_data = {
        'upload_data': [
            [ "Name", "Escherichia_coli_str_K-12_MG1655 (55494/26/3)" ],
            [ "Date Uploaded", "Sat Feb 22 19:08:55 2020" ],
            [ "Source", "RefSeq" ],
            [ "Number of Contigs", "1" ],
            [ "Size", "4641652" ],
            [ "GC Content", "0.50791" ],
            [ "Warnings", "" ],
            [ "CDS", "4319" ],
            [ "gene", "4498" ],
            [ "misc_feature", "11" ],
            [ "mobile_element", "49" ],
            [ "ncRNA", "65" ],
            [ "non_coding_features", "773" ],
            [ "non_coding_genes", "179" ],
            [ "protein_encoding_gene", "4319" ],
            [ "rRNA", "22" ],
            [ "rep_origin", "1" ],
            [ "repeat_region", "355" ],
            [ "tRNA", "89" ],
            [ "tmRNA", "2" ],
        ],
        'genome_features': [
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
            ['NC_002381.7', 82981],
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


@route('/example/<template_name>')
def default_route(template_name):
    return render_template('example/' + template_name)


run(host='localhost', port=9090, debug=True, reloader=True)
