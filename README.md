# KBase Report Templates

This repository contains templates for generating KBase HTML reports.

Reports are generated using [Template Toolkit](http://www.template-toolkit.org), a templating library available in both [python](https://github.com/lmr/Template-Toolkit-Python) and perl. Comprehensive documentation for the perl version is [available
online](http://www.template-toolkit.org/docs/manual/index.html) and is easier to access
than looking up methods in the [python
version](https://github.com/lmr/Template-Toolkit-Python).

Data are presented using [DataTables](https://datatables.net), a javascript library for creating flexible, customisable tables. DataTables is very customisable (and can hence be very confusing) so these templates use some sensible defaults. You can customise your tables further if you wish.

See the wiki for more information on developing templates.

## Quickstart

Install bottle and Template Toolkit and start exploring templates:

```sh
$ virtualenv develop                    # Create virtual environment
$ source develop/bin/activate           # Change default python to virtual env
(develop)$ pip install -U bottle Template-Toolkit-Python    # Install bottle and TTP to virtual env
(develop)$ $ python app.py
```
