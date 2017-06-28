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
        try:
            html = get_html_from_url(wiki_url)
            company_url = get_company_url_from_html(html)
        except (urllib.error.URLError, AttributeError):
            company_url = 'N/A'

        company_urls.append(company_url)
        print('{:<70} {}'.format(wiki_url, company_url))


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


def get_html_from_url(url):
    """Send HTTP request to URL and return response as HTML text.

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
        """Tell whether the tag is a website row. Used by BeatifulSoup."""
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
    raise AttributeError('Cannot find URL')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        print(error)
