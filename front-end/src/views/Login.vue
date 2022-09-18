<template>
  <div class="banner">
    <h1>Lecture Attendance Monitor System</h1>
  </div> 
  <div class="login">
    <el-tabs id="stu_login" v-model="activeName">
      <el-tab-pane label="Student" name="stu">
        <el-card>
          <el-form
            label-position="left"
            label-width="80px"
            v-model="formLabelAlign"
          >
            <el-form-item label="Student ID" class="labeltitle">
              <el-input v-model="formLabelAlign.number"></el-input>
            </el-form-item>
            <el-form-item label="Password" class="labeltitle">
              <el-input v-model="formLabelAlign.password" type="password">
              </el-input>
            </el-form-item>
            <el-button style="width: 182px" type="primary" @click="login"
              >Login</el-button
            >
            <el-button style="width: 182px" type="success" @click="openRegister"
              >Register</el-button
            >
          </el-form>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="Teacher" name="tea">
        <el-card class="loginForm">
          <el-form label-position="left" label-width="80px" :model="teacher">
            <el-form-item label="Work ID" class="labeltitle">
              <el-input v-model="teacher.number"></el-input>
            </el-form-item>
            <el-form-item label="Password" class="labeltitle">
              <el-input v-model="teacher.password" type="password"> </el-input>
            </el-form-item>
            <el-button type="danger" style="width: 380px" @click="teacher_login"
              >Login</el-button
            >
          </el-form>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      title="Student Register"
      v-model="registerVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        ref="studetnRegister"
        label-position="left"
        label-width="120px"
        :model="registerForm"
        :rules="registerRules"
      >
        <el-form-item label="number" prop="number">
          <el-input v-model="registerForm.number"></el-input>
        </el-form-item>
        <el-form-item label="first name" prop="firstName">
          <el-input v-model="registerForm.firstName"></el-input>
        </el-form-item>
        <el-form-item label="last name" prop="lastName">
          <el-input v-model="registerForm.lastName"></el-input>
        </el-form-item>
        <el-form-item label="age" prop="age">
          <el-input v-model="registerForm.age"></el-input>
        </el-form-item>
        <el-form-item label="email" prop="email">
          <el-input v-model="registerForm.email"></el-input>
        </el-form-item>
        <el-form-item label="password" prop="password">
          <el-input v-model="registerForm.password" type="password"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="registerVisible = false">Cancel</el-button>
          <el-button type="primary" @click="register">Confirm</el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog
      title="Please Confirm your Student Number"
      v-model="confirmNumber"
      width="30%"
      :before-close="handleClose"
    >
      <el-input v-model="studentNumber"></el-input>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="confirmNumber = false">Cancel</el-button>
          <el-button type="primary" @click="startFaceRecord">Start</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
// @ is an alias to /src
import { reactive, toRefs, ref, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "login",
  components: {},
  setup() {
    const router = useRouter();
    const checkEmail = (rule, value, cb) => {
      const regEmail =
        /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/;
      if (regEmail.test(value)) {
        // valid input
        return cb();
      }
      cb(new Error("Please enter Valid Email Address!"));
    };
    const checkNumber = (rule, value, cb) => {
      let exist = true;
      $.get(this.base_url + "api/checkNumber/" + value, function (data, state) {
        console.log("CheckID");
        if (res.data.code == 200) {
          if (res.data.msg !== "true") {
            cb(new Error("Student ID existed!"));
          } else {
            return cb();
          }
        }
      });
    };
    const checkAge = (rule, value, cb) => {
      const regEmail = /\d/;
      if (regEmail.test(value)) {
        if (parseInt(value) >= 50) return cb(new Error("Please enter age between 15-50!"));
        if (parseInt(value) <= 15)
          return cb(new Error("Please enter age between 15-50"));
        // valid input
        return cb();
      }
      cb(new Error("Please enter Valid Age"));
    };
    const data = reactive({
      activeName: "stu",
      confirmNumber: false,
      dialogVisible: false,
      studentNumber: 0,
      formLabelAlign: {
        number: "",
        password: "",
      },
      teacher: {
        number: "",
        password: "",
      },
      registerForm: {
        number: "",
        age: "",
        email: "",
        firstName: "",
        lastName: "",
        password: "",
        checkPwd: "",
      },
      registerRules: {
        number: [
          { required: true, message: "Please Enter Student Number", trigger: "blur" },
          { validator: checkNumber, trigger: "blur" },
        ],
        age: [
          { required: true, message: "Please Enter Age", trigger: "blur" },
          { validator: checkAge, trigger: "blur" },
        ],
        email: [
          { required: true, message: "Please Enter Email", trigger: "blur" },
          { validator: checkEmail, trigger: "blur" },
        ],
        firstName: [
          { required: true, message: "Please Enter First Name", trigger: "blur" },
          { min: 1, max: 16, message: "Length between 1-16", trigger: "blur" },
        ],
        lastName: [
          { required: true, message: "Please Enter Last Name", trigger: "blur" },
          {
            min: 1,
            max: 16,
            message: "Length between 2-16",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "Please enter password", trigger: "blur" },
          {
            min: 4,
            max: 12,
            message: "Length between 4 - 12",
            trigger: "blur",
          },
        ],
        checkPwd: [
          { required: true, message: "please enter password", trigger: "blur" },
          {
            min: 8,
            max: 50,
            message: "Length between 8 - 12",
            trigger: "blur",
          },
        ],
      },
      url: "",
      base_url: "http://localhost:5000/",
      tigger: false,
      registerVisible: false,
    });
    // ==================================
    return {
      ...toRefs(data),
      router,
    };
  },
  created() {
  },
  methods: {
    teacher_login() {
      if (this.teacher.number == "" || this.teacher.password == "") {
        return this.$message.error("Please enter workId and Password！");
      }
      var _than = this;
      this.$http
        .post(this.base_url + "api/teacher_login", this.teacher)
        .then(function (res) {
          if (res.data.code === 200) {
            _than.$message({
              type: "success",
              message: res.data.msg,
            });
            _than.router.push({
              name: "teacherIndex",
            });
            _than.$cookies.setCookie("id", _than.teacher.number);
          } else {
            _than.$message({
              type: "error",
              message: res.data.msg,
            });
          }
        })
        .catch((res) => {
          _than.$message({
            type: "error",
            message: "Network Issue, Failure to Login",
          });
          console.log(res);
        });
    },
    openRegister() {
      this.registerVisible = true;
    },
    register() {
      var _than = this;
      
      this.$http
        .post(this.base_url + "api/register", this.registerForm)
        .then(function (res) {
          if (res.data.code === 200) {
            _than.registerVisible = false;
            _than.$message({
              type: "success",
              message: "Register Successful！Please check your email to activate the account！",
            });
          } else {
            _than.$message({
              type: "error",
              message: res.data.msg,
            });
          }
        })
        .catch((res) => {
          _than.$message({
            type: "error",
            message: "Network issue,Failure to Register",
          });
        });
    },
    shou() {
      window.location.href = this.url;
    },
    handleClose() {
      this.registerVisible = false;
      this.dialogVisible = false;
      this.confirmNumber = false;
      this.$refs.studetnRegister.resetFields();
      this.$refs.studetnRegister.clearValidate();
      this.studentNumber = "";
    },
    login() {
      let _than = this;
      //stuednt login logic
      if (!this.tigger) {
        this.$http
          .post(this.base_url + "api/login", this.formLabelAlign)
          .then(function (res) {
            if (res.data.code === 200) {
              //login successful
              _than.$cookies.setCookie("id", _than.formLabelAlign.number);
              _than.$message({
                type: "success",
                message: res.data.msg,
              });
              _than.router.push({
                name: "studentIndex",
              });
            } else {
              _than.$message({
                type: "error",
                message: res.data.msg,
              });
            }
          })
          .catch((res) => {
            _than.$message({
              type: "error",
              message: "Network issue,Failure to Login",
            });
          });
      }
    },
  },
};
</script>

<style scope>
.body {
  width: 100%;
  height: 100%;
}
#stu_login {
  margin: 0 auto;
  margin-top: 7%;
  width: 500px;
  height: 250px;
}
.el-button {
  margin-left: 80px;
}
.loginForm {
  width: 99.5%;
  height: 100%;
}
.banner {
  width: 100%;
  height: 20px;
  margin-top: 10%;
  margin-bottom: 10px;
  text-align: center;
  color: rgb(13, 137, 219);
}

.banner h1{
  font-family: 'Lucida Sans';
}

.labeltitle{
  font-weight: bold;
  color:black;
}

html{
  width:100%;
  height:100%;
  background-color: rgb(243, 243, 243);
}

.el-tabs__item {
    padding: 0 20px;
    height: 40px;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    line-height: 40px;
    display: inline-block;
    list-style: none;
    font-size: 20px;
    font-weight: 500;
    color:var(--el-text-color-primary);
    position: relative;
    
}

.el-tabs__nav-wrap::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 3px;
    background-color: var(--el-border-color-light);
    z-index: var(--el-index-normal);
}

</style>
