import os
import logging
from jinja2 import Environment, FileSystemLoader

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CVGenerator:
    def __init__(self, template_dir: str, template_name: str):
        self.template_dir = template_dir
        self.template_name = template_name
        self.template_env = Environment(loader=FileSystemLoader(searchpath=self.template_dir))
        
    def load_template(self):
        """Load the HTML template."""
        try:
            template = self.template_env.get_template(self.template_name)
            logger.info("Successfully loaded template: %s", self.template_name)
            return template
        except Exception as e:
            logger.error("Failed to load template: %s", e)
            raise

    def generate_cv(self, output_path: str, custom_data: dict):
        """Generate the CV with the provided custom data."""
        try:
            template = self.load_template()
            # Render the template with custom data
            rendered_html = template.render(custom_data)
            
            # Save to output file
            with open(output_path, 'w') as output_file:
                output_file.write(rendered_html)
                logger.info("CV generated successfully at: %s", output_path)
        except Exception as e:
            logger.error("Failed to generate CV: %s", e)
            raise

if __name__ == "__main__":
    # Directory where the template is stored
    template_dir = "templates/"
    template_name = "template_arun_cv.html"

    # Data to fill in the template
    custom_data = {
        'name': 'Arun C John',
        'email': 'aruncjohn@gmail.com',
        'phone': '+1-234-567-890',
        'summary': 'Seasoned AI/ML Specialist with over 15 years of experience...',
        'experience': [
            {
                'job_title': 'AI Solutions Lead',
                'company': 'ChainML Canada Inc.',
                'years': '2022 - Present',
                'description': 'Leading AI initiatives, including GenAI pipeline development and automation...'
            },
            {
                'job_title': 'Principal Scientist',
                'company': 'Accenture Strategy & Consulting',
                'years': '2019 - 2022',
                'description': 'Delivered high-impact AI solutions in insurance, enhancing the claims process...'
            }
        ],
        'education': [
            {
                'degree': 'Master of Science in Computer Science',
                'school': 'University of Toronto',
                'years': '2010 - 2012'
            },
            {
                'degree': 'Bachelor of Engineering in Mechanical Engineering',
                'school': 'University of Mumbai',
                'years': '2005 - 2009'
            }
        ],
        'skills': ['Python', 'Machine Learning', 'Deep Learning', 'NLP', 'Cloud Services (AWS/Azure)', 'MLOps'],
        'certifications': ['AWS Certified Solutions Architect', 'Azure Data Scientist'],
    }

    # Output file
    output_path = "output/custom_cv.html"

    # Ensure the template directory exists
    if not os.path.exists(template_dir):
        logger.error("Template directory not found: %s", template_dir)
    else:
        cv_generator = CVGenerator(template_dir, template_name)
        cv_generator.generate_cv(output_path, custom_data)
