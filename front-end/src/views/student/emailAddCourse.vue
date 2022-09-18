<template>
  <div id="title">
    <el-card>
      <el-table border :data="course">
        <el-table-column prop="name" label="Module Name"></el-table-column>
        <el-table-column prop="teacher" label="Teacher"></el-table-column>
        <el-table-column prop="address" label="Class Location"></el-table-column>
        <el-table-column prop="week" label="Weekly Time"></el-table-column>
        <el-table-column prop="beginTime" label="Start Time"></el-table-column>
        <el-table-column label="Operation" width="160">
          <template #default="prop">
            <el-button type="success" @click="joinCourse(prop.row)"
              >Add Module</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog
      v-model="dialogVisible"
      title="Account validation"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        ref="studentRef"
        :model="student"
        :rules="studentFormRules"
        label-position="left"
        :label-width="120"
      >
        <el-form-item prop="account" label="Student Number">
          <el-input v-model="student.account"></el-input>
        </el-form-item>
        <el-form-item prop="pwd" label="Password">
          <el-input v-model="student.pwd" type="password"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="confirmJoin">Validate</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { reactive, toRaw, toRefs } from "@vue/reactivity";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
export default {
  setup() {
    const data = reactive({
      base_url: "http://localhost:5000/",
      student: {
        account: "",
        pwd: "",
      },
      dialogVisible: false,
      id: 0,
      course: [
        {
          name: "Math Class",
          teacher: "Michael",
        },
      ],
      studentFormRules: {
        account: [
          { required: true, message: "Student Number cannot be empty!", trigger: "blur" },
        ],
        pwd: [{ required: true, message: "Password cannot be empty！", trigger: "blur" }],
      },
    });
    var router = useRouter();
    return {
      ...toRefs(data),
      router,
    };
  },
  created() {
    this.id = this.router.currentRoute.value.params.id;
    this.getCourseById();
  },
  methods: {
    getCourseById() {
      var _than = this;
      this.$http
        .get(this.base_url + "api/getCourseById/" + this.id)
        .then((res) => {
          if (res.data.code == 200) {
            _than.course = res.data.data;
            console.log(res.data);
            ElMessage({
              type: "success",
              message: "Get class info successed！",
            });
          }
        })
        .catch((res) => {});
    },
    confirmJoin() {
      var _than = this;
      this.$refs.studentRef.validate((value) => {
        if (value) {
          // Allow to enrol this course if passed the account validation
          var date = {
            cid: this.id,
            number: toRaw(this.student).account,
            pwd: toRaw(this.student).pwd,
          };
          this.$http
            .post(this.base_url + "api/s/addCourseByEmail", date)
            .then((res) => {
              if (res.data.code == 200) {
                ElMessage({
                  type: "success",
                  message: "Added successfully, Please Login to check class info",
                });
                setInterval(_than.router.push({ name: "login" }), 1000);
              } else {
                ElMessage({
                  type: "error",
                  message: res.data.msg,
                });
              }
            })
            .catch((res) => {
              console.log(res);
              ElMessage({
                type: "error",
                message: "Network issue！",
              });
            });
        }
      });
    },
    handleClose() {
      this.dialogVisible = false;
    },
    joinCourse(row) {
      this.dialogVisible = true;
      //   Join the course
    },
  },
};
</script>

<style>
#title {
  width: 70%;
  margin: 0 auto;
  margin-top: 20%;
}
</style>