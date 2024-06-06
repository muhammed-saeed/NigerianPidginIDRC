from flask import Flask, request, jsonify
from simalign import SentenceAligner
app = Flask(__name__)
myaligner = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")
@app.route('/align', methods=['POST'])
def align_sentences():
    try:
        data = request.json
        src_sentence = data['src_sentence']
        trg_sentence = data['trg_sentence']
        alignments = myaligner.get_word_aligns(src_sentence.split(), trg_sentence.split())
        alignment_pairs = alignments["mwmf"]
        formatted_alignments = [f"{src_idx}-{trg_idx}" for src_idx, trg_idx in alignment_pairs]
        formatted_output = " ".join(formatted_alignments)
        return jsonify({'mwmf_alignments': formatted_output})
    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
