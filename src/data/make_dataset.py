# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import os
import json, csv
from urllib.request import urlretrieve


DBLP = 'https://dblp.org/search/publ/api?q=stream%3Astreams%2Fconf%2Fircdl%3A&h=1000&format=json'


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    dblp_path = os.path.join(input_filepath, 'ircdl_dblp.json')
    csv_path = os.path.join(output_filepath, 'ircdl_dblp.csv')
    # if not os.path.exists(dblp_path):
    urlretrieve(DBLP, dblp_path)

    with open(dblp_path) as dblp_file, open(csv_path, 'w') as csv_file:
        dblp = json.load(dblp_file)

        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['key', 'doi', 'url', 'ee', 'year', 'authors', 'title', 'venue', 'pages', 'length', 'type', 'access'])
        for hit in dblp['result']['hits']['hit']:
            paper = hit['info']
            
            if 'authors' in paper:
                # authors = ', '.join([a['text'] for a in paper['authors']['author']]) if isinstance(paper['authors']['author'], list) else paper['authors']['author']['text']
                authors = [a['text'] for a in paper['authors']['author']] if isinstance(paper['authors']['author'], list) else [paper['authors']['author']['text']]
            else:
                authors = []

            key = paper['key'] if 'key' in paper else None
            doi = paper['doi'] if 'doi' in paper else None
            access = paper['access'] if 'access' in paper else None
            ee = paper['ee'] if 'ee' in paper else None
            range = paper['pages'] if 'pages' in paper else None
            venue = paper['venue'] if 'venue' in paper else None
            if range is not None:
                pages = range.split('-')
                length = int(pages[1]) - int(pages[0])
            else:
                length = None
            
            writer.writerow([key, doi, paper['url'], ee, paper['year'], authors, paper['title'], venue, range, length, paper['type'], access])


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
