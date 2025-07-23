import requests
from django.core.management.base import BaseCommand
from monitor.models import Website, StatusCheck


class Command(BaseCommand):
    help ='Check the status of websites and log the results.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting website status check...\n")

        websites_to_check =  Website.objects.all()

        if not websites_to_check:
            self.stdout.write("No websites to check.\n")
            return
        
        for website in websites_to_check:
            self.stdout.write(f"Checking {website.url}...\n")
            is_up = False
            status_code = None
            response_time = None

            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            
            try:
                response = requests.head(website.url, headers=headers, timeout=10, allow_redirects=True)
                if response.status_code < 400:
                    is_up = True
                status_code = response.status_code
                response_time = response.elapsed.total_seconds()
            except requests.RequestException as e:
                pass
            
            StatusCheck.objects.create(
                website=website,
                is_up=is_up,
                status_code=status_code,
                response_time=response_time
            )

            if is_up:
                self.stdout.write(f"{website.url} is UP (Status Code: {status_code}, Response Time: {response_time:.2f}s)\n")
            else:
                self.stdout.write(f"{website.url} is DOWN (Status Code: {status_code})\n")
            
            self.stdout.write("Status check completed.\n")
                
