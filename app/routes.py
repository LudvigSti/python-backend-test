from flask import Flask, request, jsonify, Blueprint
import requests
from .services import get_openings, get_job_details, extract_text_from_html, get_html_content, find_relevant_links
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from openai import OpenAI

app = Flask(__name__)

routes = Blueprint('routes', __name__)

@routes.route('/jobs', methods=['GET'])
def jobs():
    job_list = get_openings()
    return jsonify(job_list)

@routes.route('/jobs/<int:job_id>', methods=['GET'])
def job_details(job_id):
    job_list = get_openings()
    if job_id < 0 or job_id >= len(job_list):
        return jsonify({"error": "Job not found"}), 404
    job = job_list[job_id]
    detailed_job = get_job_details(job)
    return jsonify(detailed_job)

@routes.route('/extract', methods=['GET'])
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch the website"}), 500

    soup = BeautifulSoup(response.text, "html.parser")
    links = find_relevant_links(soup)
    text_collections = []
    for category in links:
        for link in sorted(links[category], key=len)[:3]:
            full_link = urljoin(url, link)
            html_content = get_html_content(full_link)
            if html_content is None:
                continue
            text_collections.append(extract_text_from_html(html_content).strip())

    unstructured_data = "\n".join(text_collections)

    client = OpenAI(
        api_key="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",
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Format the following data into a consistent JSON structure:\n\n" + unstructured_data
            }
        ],
        model="gpt-4o",
    )

    formatted_data = response['choices'][0]['message']['content'].strip()

    return jsonify({
        "formatted_data": formatted_data,
        "links": {k: list(v) for k, v in links.items()}
    })

if __name__ == "__main__":
    app.run(debug=True)