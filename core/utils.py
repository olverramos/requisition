from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def getPaginator(queryset, page=1, items_per_page=None):
    
    if items_per_page is None:
        items_per_page = settings.ITEMS_PER_PAGE
        
    total_registers = queryset.count()
    
    total_pages = (total_registers // items_per_page)
    if total_registers % items_per_page > 0:
        total_pages += 1
    
    paginator = {
        'page': page,
        'items_per_page': items_per_page,
        'total': total_registers,
        'total_pages': total_pages
    }
    
    offset = (page - 1) * items_per_page
    paginator['data'] = queryset.skip( offset ).limit( items_per_page )
    
    return paginator

def send_basic_mail(message_data, context=None, text_content=None, text_template=None, html_content=None, html_template=None):
    if text_content is None:
        text_content = ''
    if text_template is not None and context is not None:
        # First, render the plain text content.
        text_content = render_to_string(
            text_template,
            context=context,
        )

    if text_template is not None and context is not None:
        # Secondly, render the HTML content.
        html_content = render_to_string(
            html_template,
            context=context,
        )

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
        
    msg.send()


