import asyncio
from pyppeteer import launch

async def create_pdf_from_html(html, pdf_path):
  browser = await launch()
  page = await browser.newPage()

  await page.setContent(html)
  await page.pdf({'path': pdf_path, 'format': 'A4'})
  await browser.close()

# HTML content
html = '''
<html>
  <head>
      <title>PDF Example</title>
  </head>

  <body>
      <h1>Hey, this will turn into a PDF!</h1>
  </body>
</html>
'''

# Run create_pdf_from_html
asyncio.get_event_loop().run_until_complete(create_pdf_from_html(html, 'from_html.pdf'))