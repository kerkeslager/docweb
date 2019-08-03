import collections

RenderResult = collections.namedtuple(
    'RenderResult',
    (
        'html',
        'css',
        'javascript',
    ),
)

def as_page(render_result):
    return '''
        <html>
            <head>
                <title></title>
                <style>{}</style>
                <script type="javascript">{}</script>
            </head>
            <body>{}</body>
        </html>
    '''.format(
        render_result.css or '',
        render_result.javascript or '',
        render_result.html,
    )

def render_bibliography_entry_book(source_json):
    html = '''
        <div class='wd-bibliography-entry-book'>
          <span class='wd-author'>{}</span>
          <span class='wd-title'>{}</span>
          <span class='wd-publisher'>{}</span>,
          <span class='wd-publication-date-year'>{}</span>.
        </div>
    '''.format(
        source_json['author'],
        source_json['title'],
        source_json['publisher'],
        source_json['publication_date']['year'],
    )

    css = '''
    .wd-bibliography-entry-book .wd-title {
        font-style: italic;
    }
    '''

    return RenderResult(
        html=html,
        javascript=None,
        css=css,
    )

def content_type_router(source_json, content_type):
    return {
        'bibliography/entry/book': render_bibliography_entry_book,
    }[content_type](source_json)

def render(source_json, full_page=False):
    return content_type_router(
        source_json,
        source_json['__meta__']['content_type'],
    )
