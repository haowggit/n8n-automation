import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Das Arbeitsverzeichnis innerhalb des Containers
WORK_DIR = '/data'


@app.route('/compile', methods=['POST'])
def compile_latex():
    # Holt den Dateinamen aus der ankommenden Anfrage
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({"error": "Missing 'filename' in request body"}), 400

    filename = data['filename']

    # Sicherheitsprüfung: Erlaube keine Pfad-Manipulationen
    if '..' in filename or filename.startswith('/'):
        return jsonify({"error": "Invalid filename"}), 400

    base_name, ext = os.path.splitext(filename)
    if ext != '.tex':
        return jsonify({"error": "Filename must end with .tex"}), 400

    tex_filepath = os.path.join(WORK_DIR, filename)

    if not os.path.exists(tex_filepath):
        return jsonify({"error": f"File not found: {tex_filepath}"}), 404

    # Der Befehl zum Kompilieren des PDFs
    command = [
        "xelatex",
        "-interaction=nonstopmode",
        "-output-directory=" + WORK_DIR,
        tex_filepath
    ]

    try:
        print(f"Executing command: {' '.join(command)}")
        # Führt den Befehl aus
        process = subprocess.run(command, capture_output=True, text=True, check=True)

        pdf_path = os.path.join(WORK_DIR, base_name + '.pdf')
        if os.path.exists(pdf_path):
            print("PDF successfully created.")
            return jsonify({"status": "success", "pdf_path": pdf_path}), 200
        else:
            print("Command ran, but PDF not found. Check LaTeX logs.")
            return jsonify({"error": "PDF file not created.", "logs": process.stdout}), 500

    except subprocess.CalledProcessError as e:
        # Fängt Fehler vom xelatex-Prozess ab
        print(f"Error during LaTeX compilation: {e.stderr}")
        return jsonify({"error": "LaTeX compilation failed", "logs": e.stderr}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)