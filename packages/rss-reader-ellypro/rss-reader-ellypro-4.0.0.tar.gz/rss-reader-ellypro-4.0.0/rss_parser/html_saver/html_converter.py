from os import path


def html_convert(entries, to_html_attr):
    # Creating the path to html file
    save_path = to_html_attr
    name_of_file = 'rss.html'
    complete_name = path.join(save_path, name_of_file)

    # to open/create a new html file in the write mode
    f = open(complete_name, "w")

    html_template = f'''<html>
    <head>
    <title>Title</title>
    </head>
    <body>
    <h2>Welcome To GFG</h2>'''
    for e in entries:
        title = e.title.text
        link = e.link.get('href')
        date = e.updated.text
        summary = e.summary.text
        html_template += f'''
        <div>
            <h3>{title}</h3>
            <a href={link}>{e.link}</a>
            <h5>{date}</h5>
            <p>{summary}</p>
        </div>
        '''
    html_template += f'''
    </body>
    </html>
    '''
    # writing the code into the file
    f.write(html_template)
    # close the file
    f.close()
