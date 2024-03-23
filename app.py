from flask import Flask, request, jsonify
import openai
import lancedb
from google.cloud import secretmanager

def access_secret(secret_id):
    # Build the client and the resource name
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/113104351160/secrets/{secret_id}/versions/1"

    # Access the secret version
    response = client.access_secret_version(request={"name": name})

    # Return the decoded payload
    return response.payload.data.decode('UTF-8')

OPENAI_BEARER_KEY = access_secret('OPENAI_BEARER_KEY')


uri = "data_storage"
db = lancedb.connect(uri)

app = Flask(__name__)
client = openai.Client(api_key=OPENAI_BEARER_KEY)

@app.route('/', methods=['GET'])
def index():
    # Return the 'static/index.html' file
    return app.send_static_file('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    query = data['query']

    # Get embeddings for the query
    embeddings_response = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    embeddings = embeddings_response.data[0].embedding

    # Search for similar text in lanceDB
    tbl = db.open_table("my_table")
    similar_text = tbl.search(embeddings).limit(1).to_pandas()
    # Get the most similar text
    similar_text = similar_text['item'].values[0]
    # Augment the query with the most similar text
    aug_prompt = f"<Context>{similar_text}</Context><Query>{query}</Query>"

    # Generate text with gpt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a master at writing optmized SQL queries. Be as helpful as possible to the user by providing a detailed response to their questions"},
            {"role": "user", "content": aug_prompt},
        ],
        max_tokens=100
    )
    return jsonify(
        {
            "text": response.choices[0].message.content.strip()
        }
    )

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8989)
