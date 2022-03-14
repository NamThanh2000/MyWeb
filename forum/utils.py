from lxml.html.clean import Cleaner

cleaner = Cleaner(
    page_structure=False,
    links=False,
    style=True,
    safe_attrs_only=False,
    embedded=False,
    host_whitelist=[],
    remove_tags=('html', 'head', 'body'),
    allow_tags=['i', 'em', 'b', 'strong', 'u', 'del', 'ins', 's', 'strike', 'p', 'a', 'br', 'sub', 'sup']
)

def clean_html(text):
    return cleaner.clean_html(text)