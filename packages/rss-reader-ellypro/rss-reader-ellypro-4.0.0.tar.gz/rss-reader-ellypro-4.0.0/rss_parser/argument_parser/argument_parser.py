from argparse import ArgumentParser


def arg_parser():
    parser = ArgumentParser(prog='RSS-Reader',
                            usage='rss_reader.py [-h] [--version] [--json] [--verbose] '
                                  '[--limit LIMIT]\n\t\t      source',
                            description='Pure Python command-line RSS reader.',
                            epilog='This project was created by Elyorbek Hamroyev')

    parser.add_argument('source', nargs='?', type=str, help='RSS URL')
    parser.add_argument('--version', help='Print version info', action='version', version='%(prog)s version is 4.0.0')
    parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
    parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    parser.add_argument('--limit', help='Limit news topics if this parameter provided')
    parser.add_argument('--dates', help='Give date in "YearMonthDay" format.For example: --dates 20191206')
    parser.add_argument('--to-pdf', help='Saves rss feed into specified folder in pdf.'
                                         'For example: --to-pdf C:/example/')
    parser.add_argument('--to-html', help='Saves rss feed into specified folder in html.'
                                          'For example : --to-html C:/example/')
    args = parser.parse_args()

    my_dict = {'source': args.source,
               'limit': args.limit,
               'json_attr': args.json,
               'verbose_attr': args.verbose,
               'date_attr': args.dates,
               'to_pdf_attr': args.to_pdf,
               'to_html_attr': args.to_html}
    return my_dict

