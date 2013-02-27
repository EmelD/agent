# coding: utf-8

import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def render(request, template, context=None, mimetype=None):
    return render_to_response(template, context, context_instance=RequestContext(request), mimetype=mimetype)

def render_json(context=None):
    return HttpResponse(json.dumps(context), mimetype='application/json')

def delattrib(object, vals):
    for val in vals:
        del object[val]
    return object
def createPaginationBlock(page, per_page, list):
    paging_pages = paging_list(page,int(round(list.count() / per_page + 0.5)))
    offset = (page * int(per_page)) - int(per_page)
    pageBackForward = {'back': 1 if page == 1 else page-1,
                       'forward': paging_pages[-1] if page == paging_pages[-1] else page+1}
    result={'pagging_pages': paging_pages,
            'per_page': per_page,
            'pageBackForward': pageBackForward,
            'offset': offset,
            'page': page
    }
    return result

def paging_list(page, total_pages):
    """
    Составление списка номеров страниц вида: 1, 2 .. 8, 9 .. 12, 13, где .. - None.
    """
    list = []
    if total_pages > 2:
        list.append(1)
        if total_pages > 5:
            start = min(max(1, page - 4), total_pages - 5)
            end = max(min(total_pages, page + 4), 6)
            if start - 1 > 1:
                list.append(None)
            for i in range(start + 1, end):
                list.append(i)
            if end + 1 < total_pages:
                list.append(None)
        else:
            if total_pages == 3:
                list.extend([2,3])
            else:
                list.extend([x for x in range(2, total_pages+1)])
    elif total_pages == 2:
        list.extend([1,2])
    else:
        list.append(1)
    return list
