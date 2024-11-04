from flask import Flask, request
# import analysis

app = Flask(__name__)
# STORE_PATH = ''

### analysis function

import re
import ENVIR
from Chat import pdf2text  # read_jd, read_resume
# import openai
# client = openai.OpenAI(api_key=ENVIR.API_KEY)


if ENVIR.API_KEY:
    import openai
    model = openai.OpenAI(api_key=ENVIR.API_KEY)
else:
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_openai import AzureChatOpenAI
    model = AzureChatOpenAI(
        openai_api_version="2023-07-01-preview",
        azure_deployment="gpt-35-turbo",
    )

def completion_batch(job_name, jd_text, resume_path, crit_dims, addinfo):
    st = '你是一位HR，你正在为职位“{}”招募合适的候选人。'.format(job_name)
    jd = job_name + '岗位职责与任职资格如下+\n\n' + jd_text

    q1 = '请从"{}"{}个方面提取岗位要求，要求中未涉及的方面则忽略'.format(' '.join(crit_dims), len(crit_dims))
    q2 = '请结合岗位要求，分析简历在各项上匹配与否，逐项进行匹配程度的5分制打分，其中未提及要求的项忽略不打分'
    q3 = '请计算上述各项得分的平均分（百分制）作为这份简历的整体匹配度得分，并在“推荐、不推荐”2个建议中选择一个作为简历-岗位匹配的判断结果，如果推荐则给出面试时需要关注的信息，如果不推荐则给出不推荐的理由'
    
    question = [SystemMessage(content=st), SystemMessage(content=jd), HumanMessage(content=q1)]
    completion_1 = model(question)
    print(completion_1)
    answer_1 = completion_1.content

    question.append(AIMessage(content='经提炼的岗位要求如下：{}'.format(answer_1)))
    
    if type(resume_path) == str:
        resume_path = [resume_path]
    if len(resume_path) > 1:
        addit = None

    all_rst = dict()
    for rpi in resume_path:
        if rpi.split('.')[-1] != 'pdf':
            continue
        question_rpi = question.copy()
        print('***', rpi, '***')
        rm = '有一份简历：\n\n' + pdf2text(rpi) + '\n\n简历中未提及的技能视作候选人不具备'
        if addinfo:
            rm += '。另有额外信息，'+addinfo
        
        question_rpi.append(HumanMessage(content=rm))
        question_rpi.append(HumanMessage(content=q2))
        completion_2 = model(question_rpi)
        # print(completion_2)
        answer_2 = completion_2.content

        question_rpi.append(AIMessage(content=answer_2))
        question_rpi.append(HumanMessage(content=q3))
        completion_3 = model(question_rpi)
        # print(completion_3)
        answer_3 = completion_3.content

        all_rst[rpi] = '\n——————\n'.join([answer_1, answer_2, answer_3])
    return all_rst



def jd_cv_jdf(jd_name, jd_text, crit, other_details, rsm_path, addit=None):
    crit.extend(re.split('[ ]|[\t]|[、]|[,]|[，]|[.]|[。]|[;]|[；]|[_]', other_details))
    if len(addit) < 4:
        addit = None
    ans = completion_batch(jd_name, jd_text, rsm_path, crit, addit)

    out_ans = ''
    for ai in ans.keys():
        # out_ans += '\n\n\n\n\t*** {} ***\n\n'.format(ai)
        out_ans += ans[ai]
    return out_ans.strip('\n')
