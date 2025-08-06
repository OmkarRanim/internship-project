from flask import Flask, render_template, request, send_file
import pdfkit
import tempfile

app = Flask(__name__)

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview-frame', methods=['POST'])
def preview_frame():
    data = request.form.to_dict()
    template = data.get('template', 'resume_template1')
    return render_template(f"{template}.html", data=data)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.to_dict()
    template = data.get('template', 'resume_template1')
    html_out = render_template(f"{template}.html", data=data)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        pdfkit.from_string(html_out, pdf_file.name, configuration=config)
        return send_file(pdf_file.name, as_attachment=True, download_name="resume.pdf")

if __name__ == "__main__":
    app.run(debug=True)
