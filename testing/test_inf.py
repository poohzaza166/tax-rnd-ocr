import requests
import base64

# Define the base URL for the API
base_url = "http://localhost:8000"

# Sample data for the LLM query
llm_query = {
    "user_id": "I am 4324",
    "doc_id": "4324",
    "type": "image",
    "question": "what is deliver order fee?",
}

# Function to read and encode an image file to base64
def encode_image_to_base64():
    with open("/home/bsabsri/rnd/data/rnd/tax-rnd-ocr/img6.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image

# Make a POST request to the /llm/ endpoint
def ans_question(query):
    endpoint = "/llm/"
    response = requests.post(base_url + endpoint, json=query)
    return response

# Example usage
try:
    # Encode image to base64
    llm_query["image"] = encode_image_to_base64()

    post_response = ans_question(llm_query)
    print("POST Response:", post_response.status_code, post_response.json())

except requests.RequestException as e:
    print(f"Request error: {e}")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
