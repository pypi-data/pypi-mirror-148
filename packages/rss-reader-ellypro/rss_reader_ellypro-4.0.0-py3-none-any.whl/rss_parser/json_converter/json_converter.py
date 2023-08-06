from json import dumps


def json_converter(entries):
    my_dict = {}
    for i, en in enumerate(entries):
        inner_dict = {'title': en.title.text, 'link': en.link.get('href'), 'date': en.updated.text,
                      'summary': en.summary.text}
        my_dict[i] = inner_dict
    res = dumps(my_dict, indent=2)
    return res
