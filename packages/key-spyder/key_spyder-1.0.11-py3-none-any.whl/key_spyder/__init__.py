from key_spyder.crawler import Crawler
from argparse import ArgumentParser
from multiprocessing import Process, log_to_stderr
from logging import INFO

parser = ArgumentParser(
    prog='key-spyder',
    usage='%(prog)s [options]',
    description='Crawl websites for keywords')
parser.add_argument(
    '-u', '--urls',
    action='store',
    dest='urls',
    nargs='+',
    type=str,
    required=True,
    help='URLs to crawl',
    metavar='URLS'
)
parser.add_argument(
    '-p', '--params',
    action='store',
    dest='params',
    nargs='+',
    required=False,
    help='Parameters to crawl',
    metavar='PARAMS'
)
parser.add_argument(
    '-k', '--keywords',
    action='store',
    dest='keywords',
    nargs='+',
    required=True,
    help='Keywords to search for',
    metavar='KEYWORDS'
)
parser.add_argument(
    '-r', '--recursive',
    action='store_true',
    dest='recursive',
    required=False,
    default=True,
    help='Recursively crawl subdomains'
)
parser.add_argument(
    '-o', '--output',
    action='store',
    dest='output',
    help='Output directory',
    default=None,
    metavar='OUTPUT'
)
parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    dest='verbose',
    required=False,
    default=False,
    help='Verbose output'
)


def run_from_cli(url, params, keywords, recursive, output, verbose):
    Crawler(
        urls=url,
        params=params,
        keywords=keywords,
        recursive=recursive,
        output_directory=output,
        verbose=verbose
    ).run()


# Main function
def main():
    args = parser.parse_args()

    processes = []
    for url in args.urls:
        processes.append(Process(name=url,
                                 target=run_from_cli,
                                 args=([url], args.params, args.keywords, args.recursive, args.output, args.verbose)))

    if len(processes):
        if args.verbose:
            log_to_stderr(INFO)
        [process.start() for process in processes]
        [process.join() for process in processes]