# import asyncio
# from pyppeteer import launch
import os

os.chdir(r'flask-app\docker\docker_cv_builder_agent')


# async def create_pdf_from_html(html, pdf_path):
#   browser = await launch()
#   page = await browser.newPage()

#   await page.setContent(html)
#   await page.pdf({'path': pdf_path, 'format': 'A4'})
#   await browser.close()

# if __name__ == "__main__":

#   with open('template_cv.html', 'r') as file:
#     html = file.read()
#   asyncio.get_event_loop().run_until_complete(create_pdf_from_html(html, 'from_html.pdf'))

import pdfkit

# Path to the wkhtmltopdf executable (if it's not in your system's PATH)
path_to_wkhtmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
# Update this with your actual path
pdfkit_config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Convert HTML file with CSS to PDF
pdfkit.from_file('template_cv.html', 'output.pdf', configuration=pdfkit_config)

