import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# The directory where all our files are.
WORK_DIR = '/data'


@app.route('/compile', methods=['POST'])
def compile_latex():
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({"error": "Missing 'filename' in request body"}), 400

    filename = data['filename']

    # Security check to prevent path traversal
    if '..' in filename or filename.startswith('/'):
        return jsonify({"error": "Invalid filename"}), 400

    base_name, ext = os.path.splitext(filename)
    if ext != '.tex':
        return jsonify({"error": "Filename must end with .tex"}), 400

    tex_filepath = os.path.join(WORK_DIR, filename)

    if not os.path.exists(tex_filepath):
        return jsonify({"error": f"File not found: {tex_filepath}"}), 404

    command = [
        "xelatex",
        "-interaction=nonstopmode",
        "-output-directory=" + WORK_DIR,
        tex_filepath
    ]

    try:
        print(f"Executing command: {' '.join(command)}")
        # Run the command but DO NOT check the exit code automatically (check=False)
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=WORK_DIR
        )

        pdf_path = os.path.join(WORK_DIR, base_name + '.pdf')

        # NEW LOGIC: The true test of success is whether the PDF was created.
        if os.path.exists(pdf_path):
            print("PDF successfully created, ignoring minor LaTeX warnings.")
            return jsonify({
                "status": "success",
                "pdf_path": pdf_path,
                "warnings": process.stdout  # Optionally return warnings
            }), 200
        else:
            # This is a true failure - no PDF was made.
            print("Command ran, but PDF not found. This is a critical error.")
            return jsonify({
                "error": "PDF file not created. Check logs for critical errors.",
                "logs": process.stdout
            }), 500

    except Exception as e:
        # This catches errors if the subprocess command itself fails to run.
        print(f"An unexpected server error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)