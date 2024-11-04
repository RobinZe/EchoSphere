# !/home/share/huadjyin/home/jiangyuze/.conda/envs/hrbp

import io
import os
import re
import docx
# import h5py
import string
import PyPDF2 as pypdf

# import openai
# import ENVIR

# client = openai.OpenAI(api_key=ENVIR.API_KEY)
real_name = set()


'''
### function of chatGPT

def completion(question, model='gpt-3.5-turbo-1106'):
    completion = client.chat.completions.create(model=model, messages=question)
    answer = completion.choices[0].message.content
    return answer



### functions to read existing HDF5 info

def read_resume(x1, x2):
    # x1, x2 = x
    with h5py.File(ENVIR.BASE_PATH + 'resume.h5', 'r') as f:
        att = f[x1][x2][()].decode('utf-8')
        return att

def read_jd(x='item'):
    with h5py.File(ENVIR.BASE_PATH + 'jd_list.h5', 'r') as f:
        att = f['job'][x][()].decode('utf-8')
        return att
'''


### functions to extract characters from PDF/word

def de_name_from_content(text):
    global real_name
    # patt = re.compile(r"\w+\s*[\|\n]\s*[男女]")
    # name1 = patt.findall(text)
    # print(name1)
    # for ni in name1:
    #     ni = re.split('\||\n', ni)[0].strip()
    #     real_name.add(ni)
    
    patt = re.compile(r"姓名\s*[:：\n]\s*\w{2}")
    name2 = patt.findall(text)
    # print(name2)
    for ni in name2:
        ni = re.split(':|：|\n', ni.strip())[-1].strip()
        real_name.add(ni)
    
    patt = re.compile(r"联系人\s*[:：\n]\s*\w{2}")
    name3 = patt.findall(text)
    # print(name3)
    for ni in name3:
        ni = re.split(':|：|\n', ni.strip())[-1].strip()
        real_name.add(ni)


def de_name_from_header(fname):
    global real_name
    fname = os.path.basename(fname)
    
    # for version of 1st file name
    # name_items = fname.split('-')
    # for nii in name_items:
    #     if len(nii) > 3:
    #         name_items.remove(nii)
    # real_name = real_name | set(name_items)

    # for 2nd file names
    fnames = os.path.splitext(fname)[:-1]
    fname = '.'.join(fnames)

    fname = re.sub(r"\s+", '', fname)
    fname = fname.replace('中文简历', '')
    fname = fname.replace('个人简历', '')
    fname = fname.replace('简历', '')
    fname = re.sub(r"\d+", '', fname)
    fnames = re.split('[\s]|[-]|[+]|[【]|[】]', fname)
    for fi in fnames:
        if len(fi) <= 3 and not bool(re.search(r'\d', fi)):
            real_name.add(fi)


def desensitization(text):
    global real_name
    print('name that is desensitaized :\t', real_name)
    for ni in real_name:
        # print(ni)
        if ni == '' or len(ni) > 4:
            continue
        text = re.sub(ni, "***", text)
    real_name = set()

    text = re.sub(r"\d{11}", "********", text)
    text = re.sub(r"\d{3}-\d{4}-\d{4}", "********", text)
    text = re.sub(r"\d{3}\s\d{4}\s\d{4}", "********", text)

    text = re.sub(r"\b\w+@\w+\.\w+\b", "********", text)
    return text


def skip_row(l):
    """ help decide if the row in the resume if useless and to skip. """
    skip_or_not = False
    if '招聘' in l and '严禁' in l:
        skip_or_not = True
    if '我司' in l and '有权' in l and '采取' in l:
        skip_or_not = True
    if ('导出' in l or '到岗' in l) and '时间' in l:
        skip_or_not = True
    if '系统不接收回信' in l or '接收此类邮件' in l:
        skip_or_not = True
    if '联系目标人选' in l or '暂不合适' in l:
        skip_or_not = True
    if '违法' in l and '违规' in l and '活动' in l:
        skip_or_not = True
    if '联系方式' in l:
        skip_or_not = True
    if '期望' in l:
        skip_or_not = True
    # if set_consecutive(l):
        # skip_or_not = True
    # print(l, skip_or_not)
    return skip_or_not


def postprocess(l):
    # i = 0
    for i, li in enumerate(l):
        # li = li.lstrip(string.digits)
        li = re.sub('[{}]'.format(string.punctuation), "", li)
        li = re.sub("\s+", " ", li)
        l[i] = li
        # if len(li) <= 5:
        #     if False:  # set_consecutive(li):
        #         l.remove(li)
        #     else:
        #         l[i-1] = l[i-1] + l[i]
        #         l.remove(li)
        # else:
        #     i += 1
    # print(l)

    return desensitization('\n'.join(l))


def pdf2text(input_file):
    """ extract PDF resume contents that is useful for training and comparison.

    Return : list of useful rows in resume.
    """
    input_file_name = input_file.filename
    input_file_content = input_file.read()
    input_file_content = io.BytesIO(input_file_content)

    # extract text contents from PDF/docx
    
    rsm_text = ''
    # suffx = input_file.split('.')[-1]
    if input_file_name.endswith('.pdf'):
        pdf_reader = pypdf.PdfReader(input_file_content)
        for pi in pdf_reader.pages:
            rsm_text += pi.extract_text()
    elif input_file_name.endswith('.docx') or input_file_name.endswith('.doc'):
        f = docx.Document(input_file_content)
        for pi in f.paragraphs:
            rsm_text += pi.text
    else:
        print('Error file suffix : .{}'.format(input_file_name.split('.')[-1]))
        import sys
        sys.exit(4)
    # print(rsm_text)

    # rsm_str = '\n'.join(rsm_text)
    de_name_from_header(input_file_name)
    de_name_from_content(rsm_text)
    rsm_row = re.split('\n|;|；|\x00', rsm_text)  # list of per row in resume
    # print(rsm_row)

    # filter rows in the list
    # consecutive_or_not = None
    rsm_contents = []
    for ri in rsm_row:
        # consecutive_or_not = set_consecutive(ri, consecutive_or_not)
        if len(ri) > 20 or not skip_row(ri):  # consecutive_or_not and
            rsm_contents.append(ri)
    # print(rsm_contents)
    
    return postprocess(rsm_contents)


'''
### functions to chat and fetch answer

def chat(jd, rsm):
    ctt_id = '你是一位HR，请合理判断候选人能力及性格特征，并判断其是否匹配你负责招聘的岗位。'
    ctt_rm = '你收到一份简历：\n\n' + read_resume(jd, rsm)
    ctt_jd = '你负责的一个岗位职责如下：\n\n' + read_jd(jd)
    # ctt_jd0 = '有一个岗位职责如下：\n\n' + read_jd(cur_job)
    ctt_qr = '为了判断这份简历与岗位是否匹配，首先要提取的信息是'

    ctt_al = [{'role':'system', 'content':ctt_id}, {'role':'user', 'content':ctt_rm}, {'role':'user', 'content':ctt_jd}, {'role':'user', 'content':ctt_qr}]
    ans = completion(ctt_al)
    return ans
'''