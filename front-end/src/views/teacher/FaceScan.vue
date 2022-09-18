<template>
  <el-button style="margin: 0 auto;" type="primary" @click="open_camera">Open Camera</el-button>
  <div id="main">
    <div class="l_v">
      <div>
        <span style="font-size: 1.5em; color: salmon">Scan Screen</span> <!-- Scan Screen-->
      </div>
      <canvas ref="canvas" width="640" height="480"></canvas>
    </div>
    <div class="r_v">
      <div>
        <span style="font-size: 1.5em; color: blue">Live Screen</span> <!-- Live Screen-->
      </div>
      <video ref="video" width="640" height="480" autoplay="autoplay"></video>
      <canvas
        ref="canvas2"
        width="640"
        height="480"
        style="display: none"
      ></canvas>  
    </div>
  </div>
</template>

<script>
import { toRefs, reactive, ref } from "vue";
import { toRaw } from "@vue/reactivity";
import { ElMessage } from "element-plus";
export default {
  name: "faceScan",
  props: ["cid"],
  setup() {
    const data = reactive({
      base_url: "http://localhost:5000/",
      name: "Unknown",
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
    };
  },
  created() {},
  methods: {
    open_camera() {
      // Clear current class sign-in record
      this.$http
      .get(this.base_url+"/sign_record/clear/"+this.cid)
      .then((res)=>{
        console.log(res)
      })
      .catch((res)=>{

      })
      this.photo = null;
      const tracker = new tracking.ObjectTracker("face");
      tracker.setInitialScale(4);
      tracker.setStepSize(2);
      tracker.setEdgesDensity(0.1);
      // Some browser may not be able to use mediaDevices，Therefore created an empty object of mediaDevices
      if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {};
      }
      // Some browsers partially support mediaDevices. We cannot set getUserMedia directly to the object
      // This may overwrite existing attributes. Only add the getUserMedia property if it is not there.
      if (navigator.mediaDevices.getUserMedia === undefined) {
        console.log("No getUserMedia");
        navigator.mediaDevices.getUserMedia = function (constraints) {
          // get Getusermedia if the browser have
          var getUserMedia =
            navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

          // return error if no getUsetMedia
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
      // Empty photo list
      var photos = [];
      var start_up = false;
      var i = 0;
      var _this = this;
      tracking.track(this.video, tracker, { camera: true });
      ElMessage({
        message: "Camera Opened.",
        type: "success",
      });
      tracker.on("track", function (event) {
        var context = toRaw(_this).canvas.getContext("2d");
        var video = toRaw(_this).video;
        context.clearRect(0, 0, 640, 480);
        context.drawImage(video, 0, 0, 640, 480);
        event.data.forEach(function (rect) {
          context.strokeStyle = "#a64ceb";
          context.strokeRect(rect.x, rect.y, rect.width, rect.height);
          context.font = "22px Helvetica";
          context.fillStyle = "#ff471a";
          context.fillText(_this.name, rect.x + rect.width + 5, rect.y + 11);
          // Return small size photo
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
          photos.push(canvas2.toDataURL("image/png").split(",")[1]);
          i++;
          if (i >= 10) {
            if (start_up) return;
            start_up = true;
            ElMessage({
              type: "success",
              message: "Sign-in Process, Please Wait",
            });
            var dt = { photos: photos };
            _this.$http
              .post(_this.base_url + "sign/course/" + _this.cid, dt)
              .then(function (res) {
                // Empty photo list for next sign-in
                photos = [];
                if (res.data.code === 200) {
                  ElMessage({
                    type: "success",
                    message: res.data.name + "Sign-in Successful！",
                  });
                  _this.name = res.data.name;
                  i = 0;
                  start_up = false;
                } else {
                  i = 0;
                  start_up = false;
                  ElMessage({
                    type: "error",
                    message: res.data.msg,
                  });
                }
              });
          }
        });
      });
    },
  },
};
</script>

<style>
.l_v {
  float: left;
  margin-left: 5%;
}

.el-table {
  width: 100%;
  /* margin-left: 30%; */
}
</style>