<template>
  <div>
    <input type="file" @change="onFileChange" />
    <button @click="uploadFile">Upload</button>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: null,
      message: '',
    };
  },
  methods: {
    onFileChange(event) {
      this.file = event.target.files[0];
    },
    uploadFile() {
      const formData = new FormData();
      formData.append('file', this.file);

      axios.post('/api/process', formData)
        .then(response => {
          this.message = response.data.message;
        })
        .catch(error => {
          console.error(error);
          this.message = 'File upload failed';
        });
    },
  },
};
</script>
