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
import logging
import re
import sys
import urllib.error
import urllib.request

from bs4 import BeautifulSoup


def main():
    logger = get_logger('overwrite', carriage_return=True)

    infile_name = sys.argv[1]
    outfile_name = 'wikipedia_answers.csv'

    wiki_urls = get_urls_from_csv(infile_name)
    company_urls = []

    for i, wiki_url in enumerate(wiki_urls):
        try:
            html = get_html_from_url(wiki_url)
            company_url = get_company_url_from_html(html)
            company_url = beautify_url(company_url)
        except (urllib.error.URLError, AttributeError):
            company_url = 'N/A'

        company_urls.append(company_url)
        logger.info('Ready: %d/%d' % (i + 1, len(wiki_urls)))

    # Write blank line to place carriage to right place.
    print()

    write_urls_to_csv(outfile_name, wiki_urls, company_urls)


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
                msg = 'Invalid CSV file: \'{}\'.'.format(filename)
                raise ValueError(msg)
    except OSError:
        msg = 'Cannot read file: \'{}\'.'.format(filename)
        raise OSError(msg)

    return urls


def get_html_from_url(url):
    """Send HTTP request to URL and return response as HTML text.

    Args:
        url (str): URL to website to get HTML from.

    Returns:
        str: HTML text from webpage with passed URL.

    Raises:
        urllib.error.URLError:
            - if URL is not valid;
            - if there is no internet connection.
    """
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html


def get_company_url_from_html(html):
    """Parse HTML text and return URL of the company webpage is about.

    Note:
        There is no CSS-selector to filter only website, because on some pages
        unwanted links have the same structure (tag name, class, hierarchy)
        as wanted ones, so it is impossible to distinguish right one.
        That is why search is made by name of the row ('Website').

    Args:
        html (str): HTML text from webpage.

    Returns:
        str: company website URL.

    Raises:
        AttributeError: if there is no URL on the page.
    """
    def website_row(tag):
        """Tell whether the tag is a website row. Used by BeautifulSoup."""
        row_head = tag.find('th')
        return (tag.name == 'tr'
                and row_head is not None
                and row_head.text == 'Website')

    soup = BeautifulSoup(html, 'html.parser')
    row_tag = soup.find(website_row)

    if row_tag is not None:
        link_tag = row_tag.find('a', class_='external')

        if link_tag is not None:
            return link_tag['href']

    # If row_tag or link_tag is None.
    raise AttributeError('Cannot find URL.')


def beautify_url(url):
    """Convert URL to unified format and return it.

    Note:
        Unified format looks this way:
        http://www.example.com/...

    Arguments:
        url (str): URL to be beautified.

    Returns:
        str: beautified URL.
    """
    pattern = (r'^(?:http:|https:)?'
               r'(?://)?'
               r'(?:www\.)?'
               r'(.*)$')

    raw_url = re.search(pattern, url).group(1)
    return 'https://www.{}'.format(raw_url)


def write_urls_to_csv(filename, wiki_urls, company_urls):
    """Write Wikipedia URLs with matching companies URLs to CSV file.

    Args:
        filename (str): name of the file data will be written to.
        wiki_urls (list): list of companies Wikipedia URLs.
        company_urls (list): list of companies own websites.

    Raises:
        OSError: if data cannot be written to the file.
    """
    try:
        with open(filename, 'w') as outfile:
            writer = csv.writer(outfile,
                                quoting=csv.QUOTE_ALL,
                                lineterminator='\n')

            writer.writerow(['wikipedia_page', 'website'])
            writer.writerows(zip(wiki_urls, company_urls))
    except OSError:
        msg = 'Cannot write to file: \'{}\'.'.format(filename)
        raise OSError(msg)


def get_logger(name, carriage_return=False):
    """Set logger and return it.

    Args:
        name (str): name of the logger.
        carriage_return (bool): False if '\n' should be added after line.

    Returns:
        logging.Logger: logger with stream handler.

    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    if carriage_return:
        ch.terminator = '\r'

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        logging.error(str(error))
