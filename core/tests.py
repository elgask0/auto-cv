from django.test import TestCase


from .utils import extract_job_details, JobDetails

class ExtractJobDetailsTestCase(TestCase):
    def test_extract_job_details(self):
        job_description = """
        We are seeking a Senior Software Engineer at Tech Innovators Inc. The ideal candidate will have experience in Python, Django, and cloud computing. Responsibilities include developing scalable web applications and collaborating with cross-functional teams.
        """
        
        job_details = extract_job_details(job_description)
        
        self.assertIsInstance(job_details, JobDetails)
        self.assertEqual(job_details.job_title, "Senior Software Engineer")
        self.assertEqual(job_details.company, "Tech Innovators Inc.")