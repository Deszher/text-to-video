<script>

export default {
  data() {
    return {
      inputText: '',
      inputImage: '',

      imagePreview: '',
      error: '',
      loading: false,

      outputAudio: '',
      outputVideo: '',
    }
  },
  computed: {
    canProcess() {
      return this.inputText != '' && this.inputImage.length != 0
    },
  },
  watch: {
    inputImage(val) {
      this.imagePreview = URL.createObjectURL(val[0])
    }
  },
  methods: {
    async process() {
      const text = this.inputText
      const image = this.inputImage[0]

      let res
      try {
        this.error = ''
        this.outputAudio = ''
        this.outputVideo = ''
        this.loading = true
        res = await this.apiProcess(text, image)
      } catch (error) {
        console.error("Error:", error);
        this.error = error
        this.loading = false
        return
      }
      this.loading = false

      this.outputAudio = res.speech
      if (res.video != '/') {
        this.outputVideo = res.video
      }
      console.log('success processApi', res)
    },
    async apiProcess(text, image) {
      const formData = new FormData();
      formData.append('text', text)
      formData.append('image', image)

      const response = await fetch('/api/process', {
        method: "POST",
        body: formData
      })
      const data = await response.json();
      return data;
    },
  },
}

</script>

<template>
  <div class="main">
    <h1 class="text-h3 main-title">Text to video - Group 17 project</h1>
    <div>
      <h3 class="text-h4 step-title">Step 1: insert text</h3>
      <v-textarea label="Text to speak" v-model="inputText"></v-textarea>
    </div>
    <div>
      <h3 class="text-h4 step-title">Step 2: Face photo to make a video</h3>
      <v-file-input label="Face photo" v-model="inputImage"></v-file-input>
      <v-img v-if="imagePreview" :src="imagePreview"></v-img>
    </div>
    <div>
      <h3 class="text-h4 step-title">Step 3: Process</h3>
      <v-btn variant="outlined" size="large" class="btn" @click="process" :disabled="!canProcess" :loading="loading">Process</v-btn>
    </div>
    <div>
      <h3 class="text-h4 step-title">Step 4: Enjoy the result</h3>
      <v-alert v-if="error != ''" :text="error" type="error"></v-alert>
      <video v-if="outputVideo" class="video"></video>
      <audio controls v-if="outputAudio" class="audio">
        <source :src="outputAudio" type="audio/wav">
        Your browser does not support the audio element.
      </audio>
    </div>
  </div>
  <!-- Could you give me a cup of tea, please -->
</template>

<style scoped>
.main {
  caret-color: transparent;
}
.main-title {
  padding-bottom: 40px;
}
.step-title {
  text-align: left;
  width: 100%;
  padding-bottom: 30px;
  padding-top: 30px;
}
.btn {
  width: 100%;
}
.video {
  width: 100%;
  margin-bottom: 30px;
}
.audio {
  width: 100%;
}
</style>
<style>
.v-field__field {
  caret-color: white;
}
</style>
