<template>
  <div class="banner">
    <h1>Edit Profile</h1>
  </div>
  <el-card style="width:50%; margin:0 auto;">
    <el-form
      ref="teacherRef"
      :model="teacher"
      :rules="teacherRules"
      label-width="120px"
      class="demo-ruleForm"
      label-position="left"
    >
      <el-form-item label="First Name" prop="firstName">
        <el-input v-model="teacher.firstName"></el-input>
      </el-form-item>
      <el-form-item label="Last Name" prop="lastName">
        <el-input v-model="teacher.lastName"></el-input>
      </el-form-item>
      <el-form-item label="Email" prop="email">
        <el-input v-model="teacher.email"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="info" @click="clear">Clear</el-button>
        <el-button type="primary" @click="submit">Confirm edit</el-button>
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
      teacher: {
        id: 0,
        firstName: "",
        lastName: "",
        email: "",
      },
    });
    return {
      ...toRefs(data),
      router,
    };
  },
  methods: {
    forgetPwd() {
      ElMessage({
        type: "info",
        message: "Please contact Admin to change password！",
      });
    },
    clear() {
      this.$refs.teacherRef.resetFields();
    },
    submit() {
      var email = this.teacher.email;
      var net = true;
      if (email != "") {
        const regEmail =
          /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/;
        if (regEmail.test(email)) {
          // Valid input
        } else {
          net = false;
        }
      }
      if (net) {
        if (
          this.teacher.firstName == "" &&
          this.teacher.lastName == "" &&
          this.teacher.email == ""
        ) {
          ElMessage({
            type: "error",
            message: "Please enter data！",
          });
          return;
        }
        var _than = this;
        this.$confirm("This operation will change user info, Continue?", "Attention", {
          confirmButtonText: "Confirm",
          cancelButtonText: "Cancel",
          type: "warning",
        })
          .then(() => {
            this.$http
              .post(this.base_url + "api/t/update", this.teacher)
              .then((res) => {
                if (res.data.code == 200) {
                  ElMessage({
                    type: "success",
                    message: "Edit successfull！",
                  });
                  _than.router.go(0);
                } else {
                  ElMessage({
                    type: "error",
                    message: res.data.msg,
                  });
                }
              })
              .catch((res) => {
                ElMessage({
                  type: "error",
                  message: "Network Issue！",
                });
              });
          })
          .catch((res) => {});
      }
    },
  },
  created() {
    this.teacher.id = this.$cookies.getCookie("id");
  },
};
</script>

<style>
.banner {
  width: 100%;
  height: 50px;
  text-align: center;
}

.el-form-item__label {
  font-size: 15px;
  font-style: bold;
}
</style>