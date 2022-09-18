<template>
  <div class="main1">
    <el-container>
      <el-header>
        <div class="title">
          <h1>
            The Student Number <span id="sid" style="color:red">{{ studentNumber }}</span
            > is recording face model...
          </h1>
        </div>
      </el-header>
      <el-main>
        <el-card
          style="width: 50%; height: 100px; margin-top:10px; margin-left:auto; margin-right:auto; text-align: center"
        >
          <div class="btn">
            <el-button type="primary" @click="open_camera()"
              >Open Camera</el-button
            >
            <el-button type="warning" @click="close_camera()"
              >Close Camera</el-button
            >
            <el-button type="success" @click="upload()">Upload</el-button>
          </div>
          <span style="color: #f56c6c"
            >Do not refresh the page when recording the face info, please choose a clear face by click the face image beside the live screen! </span
          >
        </el-card>
      </el-main>
      
    </el-container>

    <video ref="video" width="640" height="480" autoplay="autoplay"></video>
    <canvas
      ref="canvas"
      width="640"
      height="480"
      style="display: none"
    ></canvas>
    <canvas
      class="canvas2"
      ref="canvas2"
      width="250"
      height="250"
      @click="refresh()"
    ></canvas>
  </div>
</template>
<script>
// @ is an alias to /src
import { reactive, toRefs, ref } from "vue";
import { toRaw } from "@vue/reactivity";
import { useRouter } from "vue-router";

export default {
  name: "faceRecord",
  components: {},

  setup() {
    const router = useRouter();
    const data = reactive({
      studentNumber: 0,
      url: "",
      base_url: "http://localhost:5000/",
      tigger: false,
      tracker: null,
    });
    const video = ref(null);
    const canvas = ref(null);
    const canvas2 = ref(null);
    const photo = "";
    return {
      ...toRefs(data),
      video,
      canvas,
      canvas2,
      photo,
      router,
    };
  },
  created() {
    this.studentNumber = this.$cookies.getCookie("id");
  },
  methods: {
    open_camera() {
      const tracker = new tracking.ObjectTracker("face");
      tracker.setInitialScale(4);
      tracker.setStepSize(2);
      tracker.setEdgesDensity(0.1);
      
      if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {};
      }
      if (navigator.mediaDevices.getUserMedia === undefined) {
        ElMessage({
          type: "error",
          message: "Current website is not support camera",
        });
        navigator.mediaDevices.getUserMedia = function (constraints) {
          var getUserMedia =
            navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

          if (!getUserMedia) {
            return Promise.reject(
              new Error("getUserMedia is not implemented in this browser")
            );
          }

          return new Promise(function (resolve, reject) {
            getUserMedia.call(navigator, constraints, resolve, reject);
          });
        };
      }
      tracking.track(this.video, tracker, { camera: true });
      this.$message({
        message: "Camera opened.",
        type: "success",
      });
      var i = 1;
      var _this = this;
      tracker.on("track", function (event) {
        var context = toRaw(_this).canvas.getContext("2d");
        var video = toRaw(_this).video;
        context.clearRect(0, 0, 640, 480);
        context.drawImage(video, 0, 0, 640, 480);
        event.data.forEach(function (rect) {
          if (toRaw(_this).photo !== "") return;
          if (rect.width <= 200 || rect.height <= 200) return;
          const data = context.getImageData(
            rect.x,
            rect.y,
            rect.width,
            rect.height
          );
          var canvas2 = toRaw(_this).canvas2;
          canvas2.width = rect.width;
          canvas2.height = rect.height;
          var context2 = canvas2.getContext("2d");
          context2.clearRect(0, 0, 250, 250);
          context2.putImageData(data, 0, 0);
          toRaw(_this).photo = canvas2.toDataURL("image/png").split(",")[1];
          _this.$message({
            message: "Capture Face Successfully.",
            type: "success",
          });
          i++;
        });
      });
    },
    upload() {
      var _than = this;
      this.$message({
        message: "Start uploading the face model, Do not refresh the page!",
        type: "success",
      });
      var data = { photo: this.photo };
      this.$http
        .post(this.base_url + "upload/" + this.studentNumber, data)
        .then(function (res) {
          if (res.data.code === 200) {
            _than.$message({
              message: "Face model recorded, now you can login",
              type: "success",
            });
            setInterval(window.location.reload(), 1000);
          } else {
            _than.$message({
              type: "error",
              message: res.data.msg,
            });
          }
        });
    },
    refresh() {
      this.photo = "";
      let context = toRaw(this.canvas2).getContext("2d");
      context.clearRect(0, 0, 255, 255);
    },
    close_camera() {
      window.location.reload();
    },
    login() {
      window.location.href = "/";
    },
  },
};
</script>
<style scope>
.title {
  text-align: center;
}

.canvas2 {
  position: absolute;
  bottom: 0px;
}

</style>
