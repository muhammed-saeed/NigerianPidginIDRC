import requests
api_url = 'https://dcc9-134-96-105-142.ngrok-free.app/align'
src_sentence = "This is a test ."
trg_sentence = "Das ist ein Test ."
data = {
    "src_sentence": src_sentence,
    "trg_sentence": trg_sentence
}
response = requests.post(api_url, json=data)
if response.status_code == 200:
    result = response.json()
    mwmf_alignments = result.get('mwmf_alignments')
    print("MWMF Alignments:", mwmf_alignments)
else:
    print("Error:", response.text)
