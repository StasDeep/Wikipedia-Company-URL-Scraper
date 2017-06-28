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
import urllib.error
import urllib.request

from bs4 import BeautifulSoup


def main():
    filename = sys.argv[1]
    wiki_urls = get_urls_from_csv(filename)
    company_urls = []
    for wiki_url in wiki_urls:
        html = get_html(wiki_url)
        company_urls.append(get_company_url_from_wiki(html))


def get_urls_from_csv(filename):
    """Read CSV file and return urls from its first column.

    Args:
        filename (str): name of csv file to get urls from.

    Returns:
        list: list of all urls, written in the first column of file.

    Raises:
        OSError: if file with passed filename cannot be opened.
        ValueError: if file with passed filename is not a valid CSV file.
    """
    try:
        with open(filename, 'r') as infile:
            try:
                urls = [row[0] for row in csv.reader(infile)]
            except IndexError:
                msg = 'Invalid CSV file: \'{}\''.format(filename)
                raise ValueError(msg)
    except OSError:
        msg = 'Cannot read file: \'{}\''.format(filename)
        raise OSError(msg)

    return urls


def get_html(url):
    """Send HTTP request and return response as HTML text.

    Args:
        url (str): URL to website to get HTML from.

    Returns:
        str: HTML text from webpage with passed url.

    Raises:
        urllib.error.URLError:
            - if URL is not valid;
            - if there is no internet connection.
    """
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html


def get_company_url_from_wiki(html):
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find('td', class_='url')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        print(error)
