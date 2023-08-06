import os

from fpdf import FPDF
from PyPDF2 import PdfFileMerger

from utils import caching


def check_output_dir(output_dir):
    """ Checks existence of given output directory.

        Creates if it does not exist
    """

    dir_name, file = os.path.split(output_dir)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return os.path.join(dir_name, file)


def check_feed_info(feed_info):
    if type(feed_info) == dict:
        # feed_info is dict when it does not come from cache
        feed = feed_info
        news_list = feed_info['news_list']
        return feed, news_list

    elif type(feed_info) == list and len(feed_info) == 1:
        # feed_info is list of one tuple when it comes from cache and source is given
        feed, news_list = feed_info[0]
        return feed, news_list

    else:
        # feed_info is list of tuples when it comes from cache and source is not given
        feed = [feed for feed, news_list in feed_info]
        all_news_list = [news_list for feed, news_list in feed_info]
        return feed, all_news_list


class PDF(FPDF):
    """ Custom PDF class to override footer and add counter """
    counter = 0

    def __init__(self):
        super().__init__()

        PDF.counter += 1

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align='C')


class PdfConverter:
    """ Main class to convert news to pdf files """

    def __init__(self, feed_info, output_dir, is_from_cache):
        self.feed, self.news_list = check_feed_info(feed_info)
        self.news_count = 0
        self.output_dir = check_output_dir(output_dir)
        self.is_from_cache = is_from_cache
        if type(self.feed) != list:
            self.pdf = PDF()
            self.pdf.add_page()
            self.set_header(self.feed)
        else:
            self.all_news_list = self.news_list
            # merger to merge multiple pdf to single one
            self.pdf_merger = PdfFileMerger()

    def set_pdf_page_options(self):
        """ Sets settings for pdf writer """

        self.pdf.set_auto_page_break(auto=True, margin=20)
        self.pdf.set_font('helvetica', 'B', 13)

    def set_header(self, feed):
        """ Sets title for pdf and image of feed """

        self.pdf.set_font("helvetica", "I", 20)
        if self.is_from_cache:
            image_cache = caching.CacheImage(feed)
            image = image_cache.get_image()
        else:
            image = feed['image']

        if image != 'No info':
            self.pdf.image(image['url'], 10, 10, 50,
                           link=image['link'],
                           title=image['title'])

        self.pdf.ln(30)
        self.pdf.cell(0, 10, feed['title'], ln=True, align="C")
        self.pdf.ln(10)

    def to_pdf(self, news):
        """ Writes news info to pdf """

        self.set_pdf_page_options()

        self.pdf.multi_cell(0, 15, f'{self.news_count+1}.{news["title"]}', ln=True)
        self.pdf.cell(0, 10, f'Published at : {news["pubDate"]}', ln=True)
        self.pdf.multi_cell(0, 10, f'Description : {news["description"]}', ln=True)
        self.pdf.set_text_color(0, 0, 255)
        self.pdf.multi_cell(0, 10, f'Link : {news["link"]}',
                            ln=True, link=news['link'])
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(5)

    def convert_pdf(self):
        """ Main method to convert feed info to pdf  """

        for news in self.news_list:
            self.to_pdf(news)
            self.news_count += 1
        self.pdf.output(self.output_dir)

    def convert_pdf_recursively(self):
        """ Patches every feed info to convert_pdf method if there are multiple feeds """

        file_numbers = []
        actual_output_dir = self.output_dir
        for feed in self.feed:
            self.news_list = self.all_news_list.pop(0)
            if self.news_list:
                self.pdf = PDF()
                self.pdf.add_page()
                self.set_header(feed)

                # creates temporary files in home directory for every feed info
                self.output_dir = os.path.join(os.path.expanduser('~'), f'file_{self.pdf.counter}.pdf')

                self.convert_pdf()
                file_numbers.append(self.pdf.counter)

        # adds temporary files to pdf merger and merges to a given output directory
        for number in file_numbers:
            self.pdf_merger.append(os.path.join(os.path.expanduser('~'), f'file_{number}.pdf'))

        with open(actual_output_dir, 'wb') as pdf_file:
            self.pdf_merger.write(pdf_file)

        # removes temporary files
        for number in file_numbers:
            os.remove(os.path.join(os.path.expanduser('~'), f'file_{number}.pdf'))

    def convert(self):
        """ Main method to run class.

            Patches to methods according feed type
        """
        if type(self.feed) == dict:
            self.convert_pdf()
        elif type(self.feed) == list:
            self.convert_pdf_recursively()


class HTMLConverter:
    """ Class that converts data to html file """

    def __init__(self, feed_info, output_dir, is_from_cache):
        self.output_dir = output_dir
        self.feed, self.news_list = check_feed_info(feed_info)
        self.news_count = 0
        self.is_from_cache = is_from_cache

        if type(self.feed) == list:
            self.all_news_list = self.news_list

        self.news_output_format = '''
            <h3>{news_count}.{title}</h3>
            <h3>Published at : {pubDate}</h3>
            <p>Description : {description}</p>
            <a style="color:blue" href="{link}">Link : {link}</a><br>
        '''

    def set_header(self, feed):
        """ Set title and image of feed """

        if self.is_from_cache:
            image_cache = caching.CacheImage(feed)
            image = image_cache.get_image()
        else:
            image = feed['image']

        if image != 'No info':
            link = image['link']
            title = feed['title']
            html_string = f'''
                <a href="{link}">
                  <img src="{image['url']}" style="margin:50px;"/>
                </a>
                <h1 style="margin:50px;">
                 {title}
                </h1>    
            '''
        else:
            title = feed['title']
            html_string = f'''
                <h1 style="margin:50px;">
                 {title}
                </h1>    
            '''

        self.header = html_string

    def convert_html(self, feed):
        self.set_header(feed)
        with open(self.output_dir, 'a') as html_file:
            html_file.write(self.header)
            for news in self.news_list:
                html_file.write(self.news_output_format.format(
                                news_count=self.news_count+1, **news))
                self.news_count += 1

    def convert_html_recursively(self):
        for feed in self.feed:
            self.news_list = self.all_news_list.pop(0)
            if self.news_list:
                self.convert_html(feed)

    def convert(self):
        if type(self.feed) == dict:
            self.convert_html(self.feed)
        elif type(self.feed) == list:
            self.convert_html_recursively()


class FileConverter:
    def __init__(self, feed_info, output_dir, _format, is_from_cache):
        if _format == 'pdf':
            self.converter = PdfConverter(feed_info, output_dir, is_from_cache)
        elif _format == 'html':
            self.converter = HTMLConverter(feed_info, output_dir, is_from_cache)

    def convert(self):
        self.converter.convert()





