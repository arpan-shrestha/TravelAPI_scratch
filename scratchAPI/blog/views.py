from django.shortcuts import render
from django.http import JsonResponse
from .models import Blog
import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
# Create your views here.

def blogs(request):
    url = "https://www.antholidays.com/blog"
    blog_list = []
    response = requests.get(url)
    if response.status_code ==200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.select('div.hover\\:shadow-lg.bg-white')

        for item in items:
            title = item.find('h2').text.strip() if item.find('h2') else 'No Title'
            description = item.find('p').text.strip() if item.find('p') else 'No Description'
            details_url = item.find('a', href=True)['href'] if item.find('a', href=True) else None
            date_tag = item.find('div', class_='mb-2 text-gray-500 uppercase text-xs')
            if date_tag and date_tag.text.strip():
                try:
                    published_date = datetime.strptime(date_tag.text.strip(), "%b %d, %Y").date()
                except ValueError:
                    published_date = None
            else:
                published_date = None
            if details_url:
                details_url = urllib.parse.urljoin("https://www.antholidays.com", details_url)
            Blog.objects.get_or_create(
                title = title,
                defaults={
                    "description":description,
                    "details_url":details_url,
                    "published_date":published_date,
                }
            )
    blog_list = list(Blog.objects.values('id','title','description','details_url','published_date'))
    return JsonResponse({'Blog':blog_list})

def fetch_blog_details(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return JsonResponse({"error":"Details not found"}, status=404)
    details_data = {
        "title":blog.title,
        "description":blog.description,
        "details_url":blog.details_url,
        "published_date":blog.published_date
    }
    if blog.details_url:
        response = requests.get(blog.details_url)
        if response.status_code ==200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.select_one('div.ckEditor.blog')
            # blog.content = content.get_text(strip=True) if content else ""
            if content:
                # Split content by h2 and h3 headings to structure it
                structured_content = []
                for element in content.find_all(["h2", "h3", "p", "ul"]):
                    if element.name in ["h2", "h3"]:
                        structured_content.append({"heading": element.get_text(strip=True), "content": []})
                    elif element.name == "p":
                        if structured_content:
                            structured_content[-1]["content"].append(element.get_text(strip=True))
                        else:
                            structured_content.append({"heading": None, "content": [element.get_text(strip=True)]})
                    elif element.name == "ul":
                        items = [li.get_text(strip=True) for li in element.find_all("li")]
                        if structured_content:
                            structured_content[-1]["content"].extend(items)
                        else:
                            structured_content.append({"heading": None, "content": items})

                blog.content = structured_content
                blog.save()

            details_data.update({
                "content":blog.content
            })
        else:
            details_data["error"] = "Unable to fetch details"
    else:
        details_data["error"] = "No details URL provided"
    return JsonResponse(details_data)