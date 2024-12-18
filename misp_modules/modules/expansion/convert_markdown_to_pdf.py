#!/usr/bin/env python\

import json
import base64
import pandoc

misperrors = {'error': 'Error'}
mispattributes = {'input': ['text'], 'output': ['text']}
moduleinfo = {
    'version': '0.2',
    'author': 'Sami Mokaddem',
    'description': 'Render the markdown (under GFM) into PDF. Requires pandoc (https://pandoc.org/) and wkhtmltopdf (https://wkhtmltopdf.org/).',
    'module-type': ['expansion'],
    'name': 'Markdown to PDF converter',
    'logo': '',
    'requirements': ['pandoc'],
    'features': '',
    'references': [],
    'input': '',
    'output': '',
}

moduleconfig = [
    'margin',
]


def convert(markdown, margin='3'):
    doc = pandoc.read(markdown, format='gfm')
    options = [
        '--pdf-engine=wkhtmltopdf',
        f'-V margin-left={margin}',
        f'-V margin-right={margin}',
        f'-V margin-top={margin}',
        f'-V margin-bottom={margin}',
    ]
    converted = pandoc.write(doc, format='pdf', options=options)
    return base64.b64encode(converted).decode()

def handler(q=False):
    if q is False:
        return False
    request = json.loads(q)
    if request.get('text'):
        data = request['text']
    else:
        return False
    data = json.loads(data)
    markdown = data.get('markdown')
    try:
        margin = '3'
        if 'config' in request['config']:
            if request['config'].get('margin'):
                margin = request['config'].get('margin')
        rendered = convert(markdown, margin=margin)
    except Exception as e:
        rendered = f'Error: {e}'

    r = {'results': [{'types': mispattributes['output'],
                      'values':[rendered]}]}
    return r


def introspection():
    return mispattributes


def version():
    moduleinfo['config'] = moduleconfig
    return moduleinfo
