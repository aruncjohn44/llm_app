import os
import pdfkit
import logging
from flask import Flask, request, send_file, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_pdfkit(path_to_wkhtmltopdf):
    """Configure pdfkit with the path to the wkhtmltopdf executable."""
    if not os.path.exists(path_to_wkhtmltopdf):
        logging.error(f"wkhtmltopdf executable not found at {path_to_wkhtmltopdf}")
        raise FileNotFoundError(f"wkhtmltopdf executable not found at {path_to_wkhtmltopdf}")
    return pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

def convert_html_to_pdf(input_html, output_pdf, pdfkit_config):
    """Convert an HTML string to PDF using pdfkit."""
    try:
        pdfkit.from_string(input_html, output_pdf, configuration=pdfkit_config)
        logging.info(f"Successfully converted HTML to {output_pdf}")
    except Exception as e:
        logging.error(f"Failed to convert HTML to {output_pdf}: {e}")
        raise


# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Running"}), 200


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """API endpoint to generate PDF from HTML."""
    # Get JSON data from the request
    data = request.json
    if 'html' not in data:
        return jsonify({"error": "HTML content is required."}), 400

    input_html = data['html']
    
    # Set the path to the wkhtmltopdf executable
    path_to_wkhtmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'  # Update this with your actual path

    # Configure pdfkit
    pdfkit_config = configure_pdfkit(path_to_wkhtmltopdf)

    # Output PDF file name
    output_pdf = 'output.pdf'

    # Convert HTML to PDF
    try:
        convert_html_to_pdf(input_html, output_pdf, pdfkit_config)
        return send_file(output_pdf, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=6000, host='0.0.0.0')
