import os
import pytz
from flask import Flask, request, render_template, Markup, jsonify, send_from_directory
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from monitor import monitor_memory
from analysis import jd_cv_jdf  # 导入analysis.py中的函数


app = Flask(__name__)
# app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)  # 允许所有来源的跨域请求


# 设置后台定时任务
scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Shanghai"))
scheduler.add_job(func=monitor_memory, trigger="interval", seconds=180)
scheduler.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    # 获取表单数据
    job_name = request.form['job_name']
    job_description = request.form['job_description']
    criteria = request.form.getlist('criteria')
    other_details = request.form['other_details']
    additional_info = request.form['additional_info']

    resume_file = request.files['resume_file']
    # resume_files = request.files.getlist('file_name')
    resume_file_path = os.path.join('../storage', resume_file.filename)
    resume_file.save(resume_file_path)

    # 调用analysis.py中的jd_cv_jdf函数
    result = jd_cv_jdf(job_name, job_description, criteria, other_details, resume_file_path, additional_info)
    result = result.replace('\r\n', '<br>').replace('\n', '<br>')
    return result

'''
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    if path != "" and os.path.exists(app.static_folder, path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')'''



@app.route('/api/process', methods=['POST'])
def process():
    try:
        job_name = request.form['JobName']
        job_description = request.form.getlist['JobDescription']
        criteria = request.form('criteria')
        other_details = request.form['otherDetails']
        additional_info = request.form['AdditionalInfo']

        resume_file = request.files['resumeFile']
        resume_file_path = os.path.join('../storage', resume_file.filename)
        resume_file.save(resume_file_path)

        result = jd_cv_jdf(job_name, job_description, criteria, other_details, resume_file_path, additional_info)
        result = result.replace('\r\n', '<br>').replace('\n', '<br>')

        return jsonify({'message': result})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400



if __name__ == '__main__':
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
