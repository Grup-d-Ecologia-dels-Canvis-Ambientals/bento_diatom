<template>
  <div class="app">
    <h1>Identify diatom</h1>

    <input type="file" accept="image/*" @change="handleFileChange" />
    <!--<FileUpload ref="fileupload" mode="basic" name="demo[]" accept="image/*" :maxFileSize="1000000" @change="handleFileChange"/>-->
    
    <div v-if="response">
      <h2>API says:</h2>
      <pre>{{ response }}</pre>
    </div>
    
    <!--<img width="200px" :src="fileurl" alt="Image goes here" />-->

    <div class="card flex justify-center">
        <Image :src="fileurl" alt="Image" width="200" />
    </div>
    
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FileUpload from 'primevue/fileupload';
import Image from 'primevue/image';



const file = ref(null)
const response = ref('')
const fileurl = ref(null)

function createImage(file) {
  const reader = new FileReader();

  reader.onload = e => {
    fileurl.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

function handleFileChange(event) {
  file.value = event.target.files[0]
  createImage(file.value)
  uploadFile()
}

async function uploadFile() {
  if (!file.value) return

  const formData = new FormData()
  formData.append('image', file.value)

  try {
    const res = await fetch('http://127.0.0.1:3000/classify_both', {
      method: 'POST',
      body: formData
    })

    if (!res.ok) throw new Error('Upload failed')
    response.value = await res.text()    
  } catch (err) {
    response.value = `Error: ${err.message}`
  }
}
</script>

<style scoped>
.app {
  max-width: 600px;
  margin: auto;
  padding: 2rem;
  font-family: Arial, sans-serif;
}
</style>
