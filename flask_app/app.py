from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re

app = Flask(__name__)

def clean_html(raw_html):
    """
    Remove HTML tags from a string.
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def extract_text_from_url(url):
    """
    Extract headings and paragraphs from a URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')

        headings = [clean_html(str(h)) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        paragraphs = [clean_html(str(p)) for p in soup.find_all('p')]
        
        return {
            "url": url,
            "headings": headings,  
            "paragraphs": paragraphs  
        }
    except requests.RequestException as e:
        return {"url": url, "error": str(e)}
    except Exception as e:
        return {"url": url, "error": str(e)}

def filter_content(text, keywords_to_exclude):
    """
    Filter out unwanted content based on keywords.
    """
    filtered_text = "\n".join(
        line for line in text.splitlines() if not any(keyword in line.lower() for keyword in keywords_to_exclude)
    )
    return filtered_text

def preprocess_content(contents):
    """
    Combine headings and paragraphs into a coherent text, then filter it.
    """
    processed_content = []
    keywords_to_exclude = ["advertisement", "sponsored", "promo"]
    
    for content in contents:
        if 'error' in content:
            continue
        combined_text = ""
        headings = content['headings']
        paragraphs = content['paragraphs']
        for heading, paragraph in zip(headings, paragraphs):
            combined_text += f"{heading}\n{paragraph}\n\n"
        filtered_text = filter_content(combined_text, keywords_to_exclude)
        processed_content.append(filtered_text.strip())
    
    return processed_content

@app.route('/search', methods=['GET'])
def search_query():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    urls = list(search(query, num_results=25))
    
    contents = []
    for url in urls:
        result = extract_text_from_url(url)
        if 'error' not in result:
            contents.append(result)

    preprocessed_content = preprocess_content(contents)
    
    return jsonify({
        "urls": urls,
        "preprocessed_content": preprocessed_content
    })

if __name__ == '__main__':
    app.run(debug=True)
