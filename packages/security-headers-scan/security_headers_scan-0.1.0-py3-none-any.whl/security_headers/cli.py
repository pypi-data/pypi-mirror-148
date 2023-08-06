#!/usr/bin/env python3
import click
from .security_headers import SecurityHeaders
from .csv import CsvExport
import logging

logger = logging.getLogger('cli_security_headers')

_security_headers_project_mapping = [
    ('url', 'url'),
    ('requirement', 'requirement'),
    ('header', 'header'),
    ('directive', 'directive'),
    ('compliant', 'compliant'),
    ('expected_value', 'expected_value'),
    ('actual_value', 'actual_value')
    ]

@click.group()
def cli():
    pass

@click.command()
@click.argument('urls', nargs=-1)
@click.option('-f', 'filename', help='export filename')
@click.option('-t', 'urls_filename', help='file containing urls to scan')
@click.option('-p', 'policy', help='file containing policy')
def scan(urls=None, filename=None, urls_filename=None, policy=None):
    
    def _urls():
        if urls_filename:
            with open(urls_filename) as f:
                for url in f:
                    if url.startswith('http'):
                        yield url.strip()
        if urls:
            for url in urls:
                yield url
    
    csv_export = CsvExport("security_headers", _security_headers_project_mapping, filename=filename)
    csv_export.index('url')

    sh = SecurityHeaders(policy_file=policy)
    for url in _urls():
        for record in sh.scan(url):
            csv_export.write_record(record)
        
cli.add_command(scan)

if __name__ == "__main__":
    cli()
