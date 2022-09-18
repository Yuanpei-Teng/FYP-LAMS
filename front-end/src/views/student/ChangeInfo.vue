<template>
  <div class="banner">
    <h1>Edit Profile</h1>
  </div>
  <el-card style="width: 50%; margin: 0 auto">
    <el-form
      ref="studentRef"
      :model="student"
      :rules="studentRules"
      label-width="120px"
      class="demo-ruleForm"
      label-position="left"
    >
      <el-form-item label="FirstName" prop="firstName">
        <el-input v-model="student.firstName"></el-input>
      </el-form-item>
      <el-form-item label="LastName" prop="lastName">
        <el-input v-model="student.lastName"></el-input>
      </el-form-item>
      <el-form-item label="Email" prop="email">
        <el-input v-model="student.email"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="info" @click="clear">Clear</el-button>
        <el-button type="primary" @click="submit">Confirm Edit</el-button>
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
      student: {
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
    clear() {
      this.$refs.studentRef.resetFields();
    },
    submit() {
      var email = this.student.email;
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
          this.student.firstName == "" &&
          this.student.lastName == "" &&
          this.student.email == ""
        ) {
          ElMessage({
            type: "error",
            message: "Please Enter data !",
          });
          return;
        }
        var _than = this;
        this.$confirm("This Operation will change the user info, Continue?", "Attention", {
          confirmButtonText: "Confirm",
          cancelButtonText: "Cancel",
          type: "warning",
        })
          .then(() => {
            this.$http
              .post(this.base_url + "api/s/update", this.student)
              .then((res) => {
                if (res.data.code == 200) {
                  ElMessage({
                    type: "success",
                    message: "Change successfully",
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
                  message: "Network failure ！",
                });
              });
          })
          .catch((res) => {});
      }
    },
  },
  created() {
    this.student.id = this.$cookies.getCookie("id");
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