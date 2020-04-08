# KBase Report Templates

This repository contains templates for generating KBase HTML reports.

Reports are generated using [Template Toolkit](http://www.template-toolkit.org), a templating library available in both [python](https://github.com/lmr/Template-Toolkit-Python) and perl. Comprehensive documentation for the perl version is [available
online](http://www.template-toolkit.org/docs/manual/index.html) and is easier to access
than looking up methods in the [python
version](https://github.com/lmr/Template-Toolkit-Python).

Data are presented using [DataTables](https://datatables.net), a javascript library for creating flexible, customisable tables. DataTables is very customisable (and can hence be very confusing) so these templates use some sensible defaults. You can customise your tables further if you wish.

## Developing new templates

Creating new templates can often involve trial and error, and setting up a script to allow you to test your templates before you integrate them into a KBase app will save a lot of time and tears. The included script `app.py` launches a lightweight [Bottle](https://bottlepy.org/) server that you can use to test out your new template.

### Install bottle and Template Toolkit

If you are already familiar with using python, you can use the following steps to install bottle and Template Toolkit and start exploring templates:

    $ virtualenv develop                    # Create virtual environment
    $ source develop/bin/activate           # Change default python to virtual env
    (develop)$ pip install -U bottle Template-Toolkit-Python    # Install bottle and TTP to virtual env

More detailed installation instructions are available at the [bottle installation instructions](https://bottlepy.org/docs/0.12/tutorial.html#installation).

Start the bottle server:

    (develop)$ python app.py

and go to [http://localhost:9090/](http://localhost:9090) to see the server index page. A number of example templates used to generate KBase reports are provided to help you get started.


### Rendering a template in your KBase app

Template rendering is performed using the KBaseReport app.

Add code to render templates into your application:

```
from installed_clients.KBaseReportClient import KBaseReport

    # somewhere in your code

    kr = KBaseReport(self.callback_url)

    # Rendering a single report

    template_data = {
        'page_title': 'My KBase Report',
        'tool_output': { ... },
        'list_of_stuff': [ ... ],
    }

    # render a template file (in the scratch directory so can be accessed by the KBaseReport app)
    report_output = kr.create_extended_report({
        'template': {
            'template_file': os.path.join(self.scratch, 'templates', 'report_template.tt'),
            'template_data_json': json.loads(template_data),
        },
        'workspace_name': params['workspace_name'],
        'report_object_name': 'whatever',
    })

    # Rendering a set of templates
    data = {
        'this': { ... },
        'that': { ... },
        ...
    }

    html_links = []
    for item in some_list_of_items:
        output = kr.render_template({
            'template_file': os.path.join(self.scratch, 'templates', 'report_template.tt'),
            'template_data_json': json.loads(data[item]),
            'output_file': os.path.join(self.scratch, 'html_files', item + '.html'),
        })
        html_links.append(output[0].path)


    index_file = kr.render_template({
        'template_file': os.path.join(self.scratch, 'templates', 'index_template.tt'),
        'output_file': os.path.join(self.scratch, 'html_files, 'index.html'),
    })
    html_links.prepend(index_file[0].path)

    # create the extended report
    kr.create_extended_report({
        'html_links': html_links,
        'direct_html_link_index': 0,
        'workspace_name': params['workspace_name'],
        ... (etc.)
    })

```

## Prepare your data for tabulation

If your app already creates output in the form of a TSV or CSV file, these can be used directly to create a table. Similarly, if you can output your data as JSON, DataTables create a table from an array of JSON objects, one table row for each object. If your data needs a little more massaging to be ready for output, you can either do this in your python app, or in javascript, depending on whether you need other data and your comfort working in JS vs python.

## Save your output files

DataTables allows users to download the table content as a CSV file.

If you want users to have access to raw data--e.g. output from a wrapped tool, images, etc.--or anything that isn't contained in the table, make sure that you make all files available using a KBase extended report.

Example code from kb_Msuite:

```
    # snippet from run_checkM_lineage_wf

        # 5) Package results
        output_packages = self._build_output_packages(
            params,
            input_dir,
            removed_bins=removed_bins)

        # 6) build the HTML report
        os.makedirs(html_dir)
        html_files = self.build_html_output_for_lineage_wf(
            html_dir,
            params['input_ref'],
            removed_bins=removed_bins)

        html_zipped = self.package_folder(
            html_dir,
            html_files[0],
            'Summarized report from CheckM')

        # 7) save report
        report_params = {
            'message': '',
            'direct_html_link_index': 0,
            'html_links': [html_zipped],
            'file_links': output_packages,
            'report_object_name': 'kb_checkM_report_' + str(uuid.uuid4()),
            'workspace_name': params['workspace_name']
        }

        kr = KBaseReport(self.callback_url)
        report_output = kr.create_extended_report(report_params)
        return {
            'report_name': report_output['name'],
            'report_ref': report_output['ref']
        }

```

```
    def _build_output_packages(self, params, input_dir, removed_bins=None):

        output_packages = []

        # create bin report summary TSV table text file
        log('creating TSV summary table text file')
        tab_text_dir = os.path.join(self.output_dir, 'tab_text')
        tab_text_file = 'CheckM_summary_table.tsv'
        self.build_summary_tsv_file(
            tab_text_dir,
            tab_text_file,
            removed_bins=removed_bins)

        tab_text_zipped = self.package_folder(
            tab_text_dir,
            tab_text_file+'.zip',
            'TSV Summary Table from CheckM')
        output_packages.append(tab_text_zipped)

        log('packaging full output directory')
        zipped_output_file = self.package_folder(
            self.output_dir,
            'full_output.zip',
            'Full output of CheckM')
        output_packages.append(zipped_output_file)

        # more output packages creation

        return output_packages

    def package_folder(self, folder_path, zip_file_name, zip_file_description):
        ''' Simple utility for packaging a folder and saving to shock '''

        if folder_path == self.scratch:
            raise ValueError("cannot package folder that is not a subfolder of scratch")
        dfu = DataFileUtil(self.callback_url)
        if not os.path.exists(folder_path):
            raise ValueError("cannot package folder that doesn't exist: " + folder_path)
        output = dfu.file_to_shock({
            'file_path': folder_path,
            'make_handle': 0,
            'pack': 'zip'
        })
        return {
            'shock_id': output['shock_id'],
            'name': zip_file_name,
            'description': zip_file_description
        }
```

## Simple Example: Multi-Column Table

url: http://localhost:9090/example/kb_functional_enrichment

source file: http://localhost:9090/static/functional_enrichment.csv



## Simple Example: Attribute-Value Table



## Multi-Column Table with (Fake) Bar Chart: `kb_trimmomatic`





## Page Layout



Create a tabbed layout using the `tabbed_layout` macro. It will parse the `page_content` data structure and use the information to generate a tabbed navigation bar and content in the corresponding panels. `page_content` should be an array of objects, with each object having the keys `name`, which will be the text in the tab, and `name_lc`, a unique, URI-friendly string, which will be used to generate links.

Content for the tab can be created in a couple of different ways: using a helper, or creating HTML content that will be added as-is to the tab.

### Directly rendered content

Add HTML content as a string with the key `rendered_content`:


    page_content = [
        {
            name    => 'Tab One',
            name_lc => 'tab_one',
            rendered_content    => '_

        }



    ]



    page_content = [
        {   name    => "Bacteria",
            name_lc => "bacteria",
            content => 'table',
            file    => "gtdbtk.bac120.summary.tsv.json",
            table_config  => {
              thead => {
                enum => simpleTableCols,
              },
            },
        },
        {   name    => "Archaea",
            name_lc => "archaea",
            content => 'table',
            file    => "gtdbtk.ar122.summary.tsv.json",
            table_config  => {
              thead => {
                enum => simpleTableCols,
              },
            },
        },
        {   name    => "Bacteria Marker Summary",
            name_lc => "bacteria_marker",
            content => 'table',
            file    => "gtdbtk.bac120.markers_summary.tsv.json",
            table_config  => {
              thead => {
                enum => markerTableCols,
              },
            },
        },
        {   name    => "Archaea Marker Summary",
            name_lc => "archaea_marker",
            content => 'table',
            file    => "gtdbtk.ar122.markers_summary.tsv.json",
            table_config  => {
              thead => {
                enum => markerTableCols,
              },
            },
        },
    ];

    tabbed_layout( page_content = page_content );


