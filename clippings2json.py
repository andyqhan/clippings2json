#!/usr/bin/env python3

import argparse
import os
import re
from pprint import pprint

ap = argparse.ArgumentParser(description="""Convert a Kindle clippings file to a JSON.
The JSON will be a list of objects.""")
ap.add_argument('input_location', metavar='input_location', help="The clippings txt file from your Kindle")
ap.add_argument('--output_location', default='./clippings.json')

args = ap.parse_args()
INPUT_LOC = args.input_location
OUTPUT_LOC = args.output_location

def convert():
    out = []
    with open(INPUT_LOC, 'r') as clips:
        # my philosophy is to be very verbose with these things, since
        # performance is hardly ever a problem with such simple scripts 
       lines = clips.read() 
       quotes = lines.split('==========')[:-1]

       bylineRegex = re.compile(r"^(.*) (\(.*\))\n")
       bylineRegex2 = re.compile(r"^(.*) \- (.*)\n")
       locRegex = re.compile(r"Your Highlight on Location (\d+)")
       pageRegex = re.compile(r"Your Highlight on page (\d+)")
       pageAndLocRegex = re.compile(r"\| Location (\d+)")
       dateRegex = re.compile(r"\| Added on (.*)")
       textRegex = re.compile(r"\| Added on (.*)$\n\n(.*)\n")

       for quote in quotes:
           quote = quote.strip()
           print(quote)

           # find title and author
           byline = bylineRegex.match(quote)
           if not byline:
               # sometimes (with authorless works?) it's not in the same format
               byline = bylineRegex2.match(quote)
               author = byline.group(2).strip()
           else:
               author = byline.group(2)[1:-1].strip()
           title = byline.group(1)
           #print(title, author)

           # find location and (sometimes) page
           location_match = locRegex.search(quote)
           location = None
           page = None
           if not location_match:
               page_match = pageRegex.search(quote)
               location_match = pageAndLocRegex.search(quote)
               if page_match:
                   page = page_match.group(1)
               else:
                   # rare (for me) edge case for a bookmark
                   print("found a bookmark; won't add")
                   print(quote)
                   continue
               if location_match:
                   location = location_match.group(1)
           else:
               location = location_match.group(1)

           # find date
           date_match = dateRegex.search(quote)
           date = date_match.group(1)  # will let consumer app do date conversion. it's pretty sane rn

           out.append({
               "title": title,
               "author": author,
               "location": location,
               "page": page,
               "date": date
           })
       #pprint(out)

if __name__ == '__main__':
    convert() 
