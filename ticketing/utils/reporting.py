import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend suitable for web apps
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import xlsxwriter
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from ticketing.models import Ticket, Tag


def filter_tickets_by_timeframe(timeframe):
    now = timezone.now()
    if timeframe == '7d':
        start_date = now - timedelta(days=7)
    elif timeframe == '30d':
        start_date = now - timedelta(days=30)
    elif timeframe == '1y':
        start_date = now - timedelta(days=365)
    else:  # lifetime or default
        return Ticket.objects.all()
    return Ticket.objects.filter(date_created__gte=start_date)


def get_status_counts(timeframe='lifetime'):
    tickets = filter_tickets_by_timeframe(timeframe)
    return list(tickets.values('status').annotate(count=Count('id')))


def get_tag_counts(timeframe='lifetime'):
    tickets = filter_tickets_by_timeframe(timeframe)
    return Tag.objects.filter(ticket__in=tickets).annotate(count=Count('ticket')).order_by('-count')


def generate_pie_chart(data, label_key, count_key):
    labels = [item[label_key] for item in data]
    counts = [item[count_key] for item in data]

    fig, ax = plt.subplots()
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')


def generate_bar_chart_from_tags(tags_queryset):
    labels = [tag.name for tag in tags_queryset]
    counts = [tag.count for tag in tags_queryset]

    fig, ax = plt.subplots()
    ax.bar(labels, counts)
    ax.set_ylabel('Count')
    ax.set_xticklabels(labels, rotation=45, ha='right')
    plt.tight_layout()
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')


def export_status_to_excel(data):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Ticket Status')

    worksheet.write('A1', 'Status')
    worksheet.write('B1', 'Count')

    for idx, row in enumerate(data, start=2):
        worksheet.write(f'A{idx}', row['status'])
        worksheet.write(f'B{idx}', row['count'])

    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'categories': f'=Ticket Status!$A$2:$A${idx}',
        'values': f'=Ticket Status!$B$2:$B${idx}',
        'name': 'Ticket Status',
    })

    worksheet.insert_chart('D2', chart)
    workbook.close()
    output.seek(0)
    return output


def export_tags_to_excel(tags_queryset):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Ticket Tags')

    worksheet.write('A1', 'Tag')
    worksheet.write('B1', 'Count')

    for idx, tag in enumerate(tags_queryset, start=2):
        worksheet.write(f'A{idx}', tag.name)
        worksheet.write(f'B{idx}', tag.count)

    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'categories': f'=Ticket Tags!$A$2:$A${idx}',
        'values': f'=Ticket Tags!$B$2:$B${idx}',
        'name': 'Ticket Tags',
    })

    worksheet.insert_chart('D2', chart)
    workbook.close()
    output.seek(0)
    return output
