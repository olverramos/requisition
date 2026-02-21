from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.conf import settings


def getPaginator(data_list, page_number, title, verbose_title, page_quantity=None, page_orphans=None, page_range=None):
    element = {}
    if page_quantity is None:
        page_quantity = settings.ITEMS_PER_PAGE
    if page_orphans is None:
        page_orphans = settings.ITEMS_ORPHANS
    if page_range is None:
        page_range = settings.ITEMS_RANGE
    results_paginator_data_list = Paginator(data_list, page_quantity, orphans=page_orphans)
    try:
        page_number = int(page_number)
    except:
        page_number = 1
    
    num_pages = results_paginator_data_list.num_pages

    if page_number > num_pages:
        page_number = num_pages

    min_page = page_number - page_range
    max_page = page_number + page_range

    if min_page < 1:
        min_page = 1
    if max_page > num_pages:
        max_page = num_pages

    page = results_paginator_data_list.page(page_number)

    total = results_paginator_data_list.count
    element['register_start'] = 0
    element['register_end'] = 0
    element['quantity'] = 0
    if len(data_list) > 0:
        element['data_list'] = page.object_list
        element['has_next_page'] = page.has_next()
        element['has_previous_page'] = page.has_previous()
        element['has_first_page'] = page_number != 1
        element['has_last_page'] = page_number != num_pages
        element['page_range'] = range(min_page, max_page + 1)
        element['page_number'] = page_number
        element['page_initial_counter'] = (page_number - 1) * page_quantity
        element['quantity'] = len(page.object_list)
        if page_number > 1:
            element['previous_page'] = page_number - 1
        if page_number < max_page:
            element['next_page'] = page_number + 1
        element['register_start'] = ((page_number - 1) * page_quantity ) + 1
        element['register_end'] = element['register_start'] + element['quantity'] - 1

    element['page_quantity'] = page_quantity
    element['page_quantity_options'] = [10, 20, 30, 50]
    element['total'] = total
    element['registers'] = len(data_list)

    element['verbose_title'] = verbose_title
    element['title'] = title
    return element


def send_basic_mail(message_data, context=None, text_content=None, text_template=None, html_content=None, html_template=None):
    msg = None
    message_sent = False
    if text_content is None:
        text_content = ''
    if text_template is not None and context is not None:
        # First, render the plain text content.
        try:
            text_content = render_to_string(
                text_template,
                context=context,
            )
        except:
            text_content = None

    if html_template is not None and context is not None:
        # Secondly, render the HTML content.
        try:
            html_content = render_to_string(
                html_template,
                context=context,
            )
        except:
            html_content = None

    # Then, create a multipart email instance.
    if text_content is not None:
        msg = EmailMultiAlternatives(
            message_data['subject'],
            text_content,
            message_data['from_email'],
            message_data["to_email"],
        )

    if html_content is not None:
        # Lastly, attach the HTML content to the email instance and send.
        msg.attach_alternative(html_content, "text/html")
        
    if msg is not None:
        try:
            msg.send()
            message_sent = True
        except Exception as e:
            message_sent = False
    return message_sent
    
