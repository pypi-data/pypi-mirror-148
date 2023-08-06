from json import dumps


def print_feeds(entries, json_attr, json_results, date_attr, filtered_query):
    """Prints feed into cmd"""
    if len(entries) == 0:
        print('No entries found!')
    else:
        if not json_attr and not date_attr:
            for e in entries:
                title = e.title.text
                link = e.link.get('href')
                date = e.updated.text
                summary = e.summary.text
                res = f"Title : {title} \n\n Link : {link} \n\n Date : " \
                      f"{date} \n\n Summary : {summary}\n\n-----------------"
                print(res)
        elif not json_attr and date_attr:
            for row in filtered_query:
                title = row[0]
                link = row[1]
                date = row[2]
                summary = row[3]
                res = f"Title : {title} \n\n Link : {link} \n\n Date : " \
                      f"{date} \n\n Summary : {summary}\n\n-----------------"
                print(res)
        elif json_attr and not date_attr:
            print(json_results)
        elif json_attr and date_attr:
            my_dict = {}
            i = 0
            for row in filtered_query:
                title = row[0]
                link = row[1]
                date = row[2]
                summary = row[3]
                inner_dict = {'title': title, 'link': link, 'date': date,
                              'summary': summary}
                my_dict[i] = inner_dict
                i += 1
            print(dumps(my_dict, indent=2))
