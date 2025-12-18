from flask import Flask, request, jsonify
import os
import tempfile
from services.ocr import ocr_image
from services.llm import parse_receipt_text
from services.sheets import append_row

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "message": "receipt-yeet-gsheet is running"}), 200


@app.route('/upload-receipt', methods=['POST'])
def upload_receipt():
    if 'file' not in request.files and 'image' not in request.files:
        return jsonify({"error": "No file provided. Use form field 'file' or 'image'."}), 400

    file = request.files.get('file') or request.files.get('image')
    if file.filename == '':
        return jsonify({"error": "Empty filename."}), 400

    tmp_file = None
    try:
        # Save to a secure temporary file
        suffix = os.path.splitext(file.filename)[1] or ".jpg"
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        file.save(tmp_file.name)

        ocr_text = ocr_image(tmp_file.name) or ""
        parsed = parse_receipt_text(ocr_text)
        append_row(parsed)
        return jsonify({"status": "success", "data": parsed}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if tmp_file and os.path.exists(tmp_file.name):
            try:
                os.unlink(tmp_file.name)
            except Exception:
                pass


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



