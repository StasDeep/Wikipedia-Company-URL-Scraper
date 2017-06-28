#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Name:     Wikipedia Company URL Scraper
# Purpose:  Easy URL retrieval from Wikipedia
#
# Created:  28th of June 2017
# Author:   StasDeep
#------------------------------------------------------------------------------

"""Retrieves websites of companies from Wikipedia.

Usage:
  $ python script.py wikipedia_links.csv
"""

import csv
import sys


def main():
    filename = sys.argv[1]
    urls = get_urls_from_csv(filename)
    for url in urls:
        html = get_html(url)


def get_urls_from_csv(filename):
    """Read CSV file and return urls from its first column.

    Args:
        filename (str): name of csv file to get urls from.

    Returns:
        list: list of all urls, written in the first column of file.

    Raises:
        FileNotFoundError: if file with passed filename does not exist.
        ValueError: if file with passed filename is not a valid CSV file.
    """
    try:
        with open(filename, 'r') as infile:
            try:
                urls = [row[0] for row in csv.reader(infile)]
            except IndexError:
                msg = 'Invalid CSV file: \'{}\''.format(filename)
                raise ValueError(msg)
    except FileNotFoundError:
        msg = 'No such file: \'{}\''.format(filename)
        raise FileNotFoundError(msg)

    return urls


def get_html(url):
    pass


if __name__ == '__main__':
    try:
        main()
    except (FileNotFoundError, ValueError) as error:
        print(error)
