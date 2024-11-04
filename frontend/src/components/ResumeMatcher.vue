<template>
  <div class="resume-processor">
    <h1>EchoSphere 简历-岗位匹配工具</h1>
    
    <!-- 岗位名称文本框 -->
    <div class="form-group">
      <label for="JobName">岗位名称:</label>
      <textarea id="JobName" name="JobName" v-model="JobName" rows="1" class="form-control"></textarea>
    </div>
    
    <!-- JD 输入框 -->
    <div class="form-group">
      <label for="JobDescription">岗位描述 (JD):</label>
      <textarea id="JobDescription" name="JobDescription" v-model="JobDescription" rows="4" class="form-control"></textarea>
    </div>
    
    <!-- 评估维度选项框 -->
    <div class="form-group">
      <label>评估维度:</label>
      <div class="criteria-container">
        <div v-for="(criterion, index) in criteria" :key="criterion" class="criterion-item">
          <input type="checkbox" :id="`criterion-${index}`" :name="`criterion-${index}`" :value="criterion" v-model="selectedCriteria">
          <label :for="`criterion-${index}`">{{ criterion }}</label>
          <input v-if="criterion === '其它'" type="text" id="otherDetails" name="otherDetails" v-model="otherDetails" placeholder="请输入其它评估维度" class="form-control">
        </div>
      </div>
    </div>

    <!-- 拖入简历文件框 -->
    <div class="form-group">
      <label for="resume">拖入简历文件:</label>
      <input type="file" id="resume" name="resume" @change="onFileChange" class="form-control-file">
    </div>
    
    <!-- 补充其它信息文本框 -->
    <div class="form-group">
      <label for="AdditionalInfo">补充其它信息:</label>
      <textarea id="AdditionalInfo" name="AdditionalInfo" v-model="AdditionalInfo" rows="4" class="form-control"></textarea>
    </div>
    
    <!-- 提交按钮 -->
    <button @click="submit" class="btn btn-primary">提交</button>

    <!-- 输出框 -->
    <div v-if="outputMessage" class="output-box">
      {{ outputMessage }}
    </div>

    <!-- 错误信息显示 -->
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      JobName: '',
      JobDescription: '',
      criteria: ['教育背景', '科研经历', '工作经历', '个性特点', '其它'],
      selectedCriteria: [],
      otherDetails: '',
      resumeFile: null,
      AdditionalInfo: '',
      errorMessage: '', // 用于存储错误信息
      outputMessage: '', // 用于存储输出信息
    };
  },
  methods: {
    onFileChange(event) {
      this.resumeFile = event.target.files[0];
    },
    submit() {
      const formData = new FormData();
      formData.append('JobName', this.JobName);
      formData.append('JobDescription', this.JobDescription);
      formData.append('criteria', JSON.stringify(this.selectedCriteria));
      if (this.selectedCriteria.includes('其它')) {
        formData.append('otherDetails', this.otherDetails);
      }
      formData.append('resume', this.resumeFile);
      formData.append('AdditionalInfo', this.AdditionalInfo);

      axios.post('/api/process', formData)  // 修改了这里的URL路径
        .then(response => {
          console.log(response.data);
          this.outputMessage = response.data.message;  // 显示后端返回的消息
        })
        .catch(error => {
          console.error(error);
          this.errorMessage = error.response ? error.response.data.error : '提交失败';
        });
    },
  },
};
</script>

<style>
body {
  background-color: #f0f8ff; /* 浅色背景 */
}

.resume-processor {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 15px; /* 更加柔和的边缘 */
  background-color: #fcfefe;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
}

.form-control-file {
  margin-top: 5px;
}

.criteria-container {
  display: flex;
  flex-wrap: wrap;
}

.criterion-item {
  margin-right: 10px;
}

.btn {
  display: block;
  width: 100%;
  padding: 10px;
}

.output-box {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #e6f7ff;
}

.alert {
  margin-top: 20px;
}
</style>
