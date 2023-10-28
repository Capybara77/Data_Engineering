import requests

url = 'https://jsonplaceholder.typicode.com/posts'
response = requests.get(url)
data = response.json()

html = '<html>'
html += '<head><title>JSON to HTML</title></head>'
html += '<body style="font-family: Arial, sans-serif;">'
html += '<h1>Posts</h1>'
html += '<ul style="list-style-type: none; padding: 0;">'
for item in data:
    html += '<li style="margin: 10px 0; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">'
    html += f'<h2>{item["title"]}</h2>'
    html += f'<p>{item["body"]}</p>'
    html += '</li>'
html += '</ul>'
html += '</body>'
html += '</html>'

with open('result.html', 'w', encoding='utf-8') as file:
    file.write(html)
