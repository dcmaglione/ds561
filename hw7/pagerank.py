#!env python3
# -*- coding: utf-8 -*-
# Author: Dominic Maglione (dcmag@bu.edu)
# Date: 2023-11-10

"""A pagerank workflow."""

# Imports
import argparse
import logging
import re

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.io import fileio
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

# Regex Pattern
LINK_REGEX_PATTERN = r'<a HREF="(\d+).html">'


class CountIncomingLinks(beam.DoFn):
    """Count the incoming links for each file."""

    def process(self, element):
        link_regex = re.compile(LINK_REGEX_PATTERN)
        links = re.findall(link_regex, element)
        for link in links:
            yield (int(link), 1)


class CountOutgoingLinks(beam.DoFn):
    """Count the outgoing links for each file."""

    def process(self, element):
        link_regex = re.compile(LINK_REGEX_PATTERN)
        links = re.findall(link_regex, element)
        yield (int(element[0]), len(links))


def run(argv=None, save_main_session=True):
    """Main entry point; defines and runs the pagerank pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default='gs://bu-ds561-dcmag/files/*.html',
        help='Input file to process.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(
        SetupOptions).save_main_session = save_main_session

    with beam.Pipeline(options=pipeline_options) as p:
        input_files = known_args.input

        incoming_links = (
            p
            | "Read HTML Files as Stream" >> beam.io.ReadFromText(input_files)
            | "Count Incoming Links" >> beam.ParDo(CountIncomingLinks())
            | "Sum Incoming Links" >> beam.CombinePerKey(sum)
        )

        outgoing_links = (
            p
            | "List Files" >> beam.io.fileio.MatchFiles(input_files)
            | "Read Matches" >> beam.io.fileio.ReadMatches()
            | "Read Files" >> beam.Map(lambda x: (x.metadata.path, x.read_utf8()))
            # The CountOutgoingLinks class was meant to be used here but there were some weird errors that resulted in me consulting a classmate and approaching it this way
            | "Count Outgoing Links" >> beam.Map(
                lambda x: (x[0], len(re.findall(LINK_REGEX_PATTERN, x[1])))
            )
            | "Remove File Path"
            >> beam.Map(lambda x: (int(x[0].split("/")[-1].split(".")[0]), x[1]))
        )

        top_incoming_links = (
            incoming_links
            | "Top 5 Incoming Links" >> beam.transforms.combiners.Top.Largest(
                5, key=lambda x: x[1]
            )
        )

        top_outgoing_links = (
            outgoing_links
            | "Top 5 Outgoing Links" >> beam.transforms.combiners.Top.Largest(
                5, key=lambda x: x[1]
            )
        )

        top_incoming_links | "Log Top 5 Incoming Links" >> beam.Map(
            lambda x: logging.info(f"Top 5 Incoming Links: {x}")
        )

        top_outgoing_links | "Log Top 5 Outgoing Links" >> beam.Map(
            lambda x: logging.info(f"Top 5 Outgoing Links: {x}")
        )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
