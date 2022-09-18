<template>
  <div class="banner">
    <h1>Change Password</h1>
  </div>
  <el-card style="width:50%; margin:0 auto;">
    <el-form
      ref="pwdModelRef"
      :model="pwdModel"
      :rules="pwdModelRules"
      label-width="150px"
      class="demo-ruleForm"
      label-position="left"
    >
      <el-form-item label="Old Password" prop="oldPwd" required>
        <el-input v-model="pwdModel.oldPwd" type="password"></el-input>
      </el-form-item>
      <el-form-item label="New Password" prop="newPwd" required>
        <el-input v-model="pwdModel.newPwd" type="password"></el-input>
      </el-form-item>
      <el-form-item label="Confirm Password" prop="secondayPwd" required>
        <el-input v-model="pwdModel.secondayPwd" type="password"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="info" @click="clear">Clear</el-button>
        <el-button type="primary" @click="modifiedPwd">Confirm</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import { toRaw, toRefs, reactive } from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
export default {
  setup() {
    const router = useRouter();
    const data = reactive({
      base_url: "http://localhost:5000/",
      pwdModel: {
        id: 0,
        oldPwd: "",
        newPwd: "",
        secondayPwd: "",
      },
      pwdModelRules: {
        oldPwd: [
          { required: true, message: "Old password cannot be empty！", trigger: "blur" },
        ],
        newPwd: [
          { required: true, message: "New password cannot be empty！", trigger: "blur" },
        ],
        secondayPwd: [
          { required: true, message: "Confirm password cannot be empty！", trigger: "blur" },
        ],
      },
    });
    return {
      ...toRefs(data),
      router,
    };
  },
  methods: {
    clear() {
      this.$refs.pwdModelRef.resetFields();
    },
    modifiedPwd() {
      var _than = this;
      this.$refs.pwdModelRef.validate((value) => {
        if (value) {
          if (this.pwdModel.newPwd == this.pwdModel.secondayPwd) {
            this.$confirm("This Operation will change the user info, Continue?", "Attention", {
              confirmButtonText: "Confirm",
              cancelButtonText: "Cancel",
              type: "warning",
            })
              .then(() => {
                this.$http
                  .post(this.base_url + "api/s/pwd/update", this.pwdModel)
                  .then((res) => {
                    if (res.data.code == 200) {
                      ElMessage({
                        type: "success",
                        message: "Change Password Successfully！",
                      });
                      _than.$cookies.delCookie("id");
                      _than.router.go(0);
                    }else{
                       ElMessage({
                        type: "error",
                        message: res.data.msg,
                      });
                    }
                  })
                  .catch((res) => {});
              })
              .catch((res) => {});
          } else {
            ElMessage({
              type: "error",
              message: "Two passwords are not match！",
            });
          }
        }
      });
    },
  },
  created() {
    this.pwdModel.id = this.$cookies.getCookie("id");
  },
};
</script>

<style>
.banner {
  width: 100%;
  height: 50px;
  text-align: center;
}

.banner h1{
  font-family: 'Lucida Sans';
  color: rgb(7, 107, 153);
  height: 20px;
  font-size: 30px;
}

</style>