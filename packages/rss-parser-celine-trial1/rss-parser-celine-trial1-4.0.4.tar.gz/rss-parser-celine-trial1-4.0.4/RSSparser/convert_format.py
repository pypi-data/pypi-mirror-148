import json
import logging
import os

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph,Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# doc = SimpleDocTemplate("celine.pdf",pagesize=letter,
#                         rightMargin=72,leftMargin=72,
#                         topMargin=72,bottomMargin=18)


def get_cached_content_paths(cache_path):
    article_path = None
    links_path = None
    images_paths = []
    items = os.listdir(cache_path)
    for item in items:
        if(item.endswith("images")):
            # for element in os.listdir(os.path.abspath(os.path.join(cache_path,  item))):
            #     images_paths.append(element)
            for image in os.listdir(os.path.abspath(os.path.join(cache_path,  item))):
                images_paths.append(os.path.join(cache_path,'images', image))
            # images_paths.append(os.path.abspath(os.path.join(cache_path,  item)))
        elif(item == "links.txt"):
            links_path = os.path.abspath(os.path.join(cache_path, item))
        else:article_path = os.path.abspath(os.path.join(cache_path, item))
    return article_path, images_paths, links_path


def get_conversion_data(item):
    news = item[1]
    directory = news.get("cache_directory")
    article_path, images_paths, links_path = get_cached_content_paths(directory)
    with open(article_path) as f:
        lines = f.read()
    article = lines
    with open(links_path, 'r') as f:
        links_list = json.loads(f.read())
    title = news.get("title")
    date = news.get("date")
    return title, date, article, images_paths, links_list


# def convert_pdf(cache_list,input_path ):
#     doc = SimpleDocTemplate(input_path, pagesize=letter,
#                             rightMargin=72, leftMargin=72,
#                             topMargin=72, bottomMargin=18)
#
#     styles=getSampleStyleSheet()
#     styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
#     news_id = 0
#     Story = []
#     for item in cache_list:
#         news = item[1]
#         news_id += 1
#         directory = news.get("cache_directory")
#         article_path, images_paths, links_path = get_cached_content_paths(directory)
#         with open(article_path) as f:
#             lines = f.read()
#         article = lines
#         with open(links_path, 'r') as f:
#             links_list = json.loads(f.read())
#         title = news.get("title")
#         date = news.get("date")
#
#         Story.append(Spacer(1, 12))
#         Story.append(Spacer(1, 12))
#         ptext = '<b>News Number:  </b>: %s' % news_id
#         Story.append(Spacer(1, 12))
#         Story.append(Paragraph(ptext, styles["Normal"]))
#         ptext = '<b>Title</b>: %s' % title
#         Story.append(Paragraph(ptext, styles["Normal"]))
#         Story.append(Spacer(1, 12))
#         ptext = '<b>Date</b>: %s' % date
#         Story.append(Paragraph(ptext, styles["Normal"]))
#         Story.append(Spacer(1, 12))
#         ptext = '<b>Article</b>: %s' % article
#         Story.append(Paragraph(ptext, styles["Justify"]))
#         Story.append(Spacer(1, 12))
#
#         for pic in images_paths:
#             im = Image(pic, 2 * inch, 2 * inch)
#             Story.append(im)
#         Story.append(Spacer(1, 12))
#         Story.append(Spacer(1, 12))
#         for link in links_list:
#             ptext = '<a href = %s >Link</a>' % link
#             Story.append(Paragraph(ptext, styles["Normal"]))
#
#     doc.build(Story)

def convert_pdf(cache_list,input_path ):
    doc = SimpleDocTemplate(input_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    news_id = 0
    Story = []
    for item in cache_list:
        title, date, article, images_paths, links_list = get_conversion_data(item)
        news_id += 1

        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        ptext = '<b>News Number:  </b>: %s' % news_id
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(ptext, styles["Normal"]))
        ptext = '<b>Title</b>: %s' % title
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        ptext = '<b>Date</b>: %s' % date
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        ptext = '<b>Article</b>: %s' % article
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

        for pic in images_paths:
            im = Image(pic, 2 * inch, 2 * inch)
            Story.append(im)
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        for link in links_list:
            ptext = '<a href = %s >Link</a>' % link
            Story.append(Paragraph(ptext, styles["Normal"]))

    doc.build(Story)


def convert_html(cache_list, input_path):
    news_id = 0
    body = ""
    for item in cache_list:
        news_id += 1
        title, date, article, images_paths, links_list = get_conversion_data(item)
        text = "<h2>News Number {News_id}</h2><p><b>Title: </b>{Title}<br><b>Date: </b>{Date}<br><b>Article: </b>{Article}<br></p>"
        text = text.format(News_id=news_id, Title=title, Date=date, Article=article)
        for image_path in images_paths:
            text = text + '<img src = {Image_Path} width="200" height="250" style="vertical-align:' \
                          'middle;margin:0px 5px">'.format(Image_Path=image_path)
        n = 0
        for link in links_list:
            n += 1
            text = text + "<p><a href={Link}>link number {N}</a></p>".format(Link = link, N = n)
        body = body + text
    text = '''<html><body>{Text}</body></html>'''.format(Text = body)

    if not input_path.endswith(".html"):
        logging.error("Input path is not ending with .html")
        raise SystemExit('ERROR: Path extension must be .html')

    try:
        file = open(os.path.join(input_path),"w")
        file = open(input_path,"w")
        file.write(text)
        file.close()

    except FileNotFoundError:
        logging.error("Provided path is not correct.")
        raise SystemExit('Path is not correct. Please Input a correct Path.')



