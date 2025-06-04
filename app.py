from flask import Flask, render_template, request, send_file, jsonify
import qrcode
from PIL import Image
import io
import base64
import os
from datetime import datetime
from flask import url_for

app = Flask(__name__)

if not os.path.exists('static'):
    os.makedirs('static')
if not os.path.exists('static/qr_codes'):
    os.makedirs('static/qr_codes')


def generate_qr_code(data, fill_color="black", back_color="white", box_size=10, border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=int(box_size),
        border=int(border),
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.form.get('data', '').strip()
        fill_color = request.form.get('fill_color', '#000000')
        back_color = request.form.get('back_color', '#ffffff')
        box_size = request.form.get('box_size', 10)
        border = request.form.get('border', 4)

        if not data:
            return jsonify({'error': 'Please enter data to encode'}), 400

        img = generate_qr_code(data, fill_color, back_color, box_size, border)

        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qr_code_{timestamp}.png"
        filepath = os.path.join('static', 'qr_codes', filename)
        img.save(filepath)

        return jsonify({
            'success': True,
            'image': f"data:image/png;base64,{img_base64}",
            'download_url': f"/download/{filename}",
            'filename': filename
        })

    except Exception as e:
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500


@app.route('/download/<filename>')
def download_qr(filename):
    try:
        filepath = os.path.join('static', 'qr_codes', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return "File not found", 404
    except Exception as e:
        return f"Error downloading file: {str(e)}", 500


@app.route('/api/generate', methods=['POST'])
def api_generate():
    try:
        data = request.json

        qr_data = data.get('data', '').strip()
        if not qr_data:
            return jsonify({'error': 'Data field is required'}), 400

        fill_color = data.get('fill_color', 'black')
        back_color = data.get('back_color', 'white')
        box_size = data.get('box_size', 10)
        border = data.get('border', 4)

        img = generate_qr_code(qr_data, fill_color, back_color, box_size, border)

        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        return jsonify({
            'success': True,
            'image': f"data:image/png;base64,{img_base64}",
            'message': 'QR code generated successfully'
        })

    except Exception as e:
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        print("Генератор QR-кодов (CLI режим)")
        input_data = input("Введите текст или ссылку для кодирования в QR-код: ")
        output_filename = input("Введите имя файла для сохранения QR-кода (или нажмите Enter): ")

        if not output_filename:
            output_filename = "qr_code.png"
        elif not output_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            output_filename += ".png"

        img = generate_qr_code(input_data)
        img.save(output_filename)
        print(f"QR-код успешно создан и сохранен как '{output_filename}'")
    else:
        print("Starting QR Code Generator Web Server...")
        print("Open your browser and go to: http://127.0.0.1:5000")
        app.run(debug=True, host='127.0.0.1', port=5000)