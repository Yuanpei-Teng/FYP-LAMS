<template>
  <div class="main">
    <el-header>
      <div class="title">
        <h1>Class List</h1>
        <el-button style="margin-top: 15px" type="danger" @click="batchDel()"
          >Multiple Cancel</el-button
        >
      </div>
    </el-header>
    <el-main>
      <el-card style="width: 100%">
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          @selection-change="handleSelectionChange"
          :header-cell-style="{background:'#eef1f6',color:'#606266',fontSize:'15px'}"
          :cell-style="{color: '#666', fontFamily: 'Arial',fontSize:'15px'}"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="Module name" />
          <el-table-column prop="teacher" label="Teacher" width="120">
          </el-table-column>
          <el-table-column prop="address" label="Classroom"> </el-table-column>
          <el-table-column prop="week" label="Weekly time"> </el-table-column>
          <el-table-column prop="beginTime" label="Class Time"> </el-table-column>
          <el-table-column label="Operate" width="120">
            <template #default="prop">
              <el-button type="success" round size="small" @click="checkInfo(prop.row)"
                >See Details</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      <el-dialog style="text-align:center" title="Class progress" v-model="showCourse" width="30%">
        <el-form
          label-position="left"
          label-width="100px"
          :model="course"
          style="max-width: 460px"
          id= "selectForm"
        >
          <el-form-item label="Course Name" label-width="130px">
            <el-input v-model="course.name" disabled></el-input>
          </el-form-item>
          <el-form-item label="Teacher" label-width="130px">
            <el-input v-model="course.teacher" disabled></el-input>
          </el-form-item>
          <el-form-item label="Classroom" label-width="130px">
            <el-input v-model="course.address" disabled></el-input>
          </el-form-item>
          <el-form-item label="Class time" label-width="130px">
            <el-input v-model="course.beginTime" disabled></el-input>
          </el-form-item>
          <el-form-item label="Total Sign-in Score" label-width="130px">
            <el-input v-model="course.count" disabled></el-input>
          </el-form-item>
          <el-form-item label="Progress" label-width="130px">
            <el-progress
              :text-inside="true"
              :stroke-width="26"
              :percentage="course.score"
              :color="customColors"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-popconfirm
            title="Are you sure to delete this class?"
            @confirm="remove()"
          >
            <template #reference>
              <el-button type="danger">Delete Class</el-button>
            </template>
          </el-popconfirm>

          <el-button type="primary" @click="showCourse = false"
            >Confirm</el-button
          >
        </template>
      </el-dialog>
    </el-main>
  </div>
</template>
<script>
// @ is an alias to /src
import { reactive, toRefs, ref, onMounted } from "vue";
import { toRaw } from "@vue/reactivity";
import { useRouter } from "vue-router";
import { ElMessageBox, ElMessage } from "element-plus";
export default {
  name: "teacherCourse",
  components: {},
  setup() {
    // const router = useRouter();
    const data = reactive({
      id: 0,
      start: false,
      showAdd: false,
      current: 0,
      sid: 0,
      cid: 0,
      base_url: "http://localhost:5000/",
      open: false,
      showCourse: false,
      tableData: [
        {
          id: "4",
          name: "English Class",
          teacher: "Tom",
          address: "No. 189, Grove St, Los Angeles",
          progress: 80,
        },
      ],
      multipleSelection: [],
      course: {},
    });
    const customColors = [
      { color: "#F56C6C", percentage: 20 },
      { color: "#e6a23c", percentage: 40 },
      { color: "#E6A23C", percentage: 60 },
      { color: "#CEF6CE", percentage: 80 },
      { color: "#67C23A", percentage: 100 },
    ];
    return {
      ...toRefs(data),
      customColors,
    };
  },
  methods: {
    info() {},
    add(row) {},
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    remove() {
      var data = { sid: this.id, cids: [this.course.id] };
      this.cancellation(data);
      this.showCourse = false;
    },
    // Delete the course
    cancellation(data) {
      // Send the request to cancel the course
      this.$http
        .post(this.base_url + "api/s/batchRemove", data)
        .then((res) => {
          if (res.data.code == 200) {
            ElMessage({
              type: "success",
              message: "Delete Successfull",
            });
            this.getCourse();
          } else {
            ElMessage({
              type: "error",
              message: res.data.msg,
            });
          }
        })
        .catch((res) => {});
    },
    getCourse() {
      var _than = this;
      this.$http
        .get(this.base_url + "api/s/getCourse/" + _than.id)
        .then(function (res) {
          if (res.data.code === 200) {
            _than.$message({
              type: "success",
              message: "Get Class Lists Successfull",
            });
            _than.tableData = res.data.data;
            console.log(res.data.data);
          } else {
            _than.$message({
              type: "error",
              message: "Failed to get Class Lists ",
            });
          }
        })
        .catch((res) => {
          _than.$message({
            type: "error",
            message: "Network issue, Failure to retreive data",
          });
        });
    },
    checkInfo(row) {
      this.showCourse = true;
      this.course = row;
    },
    batchDel() {
      if (this.multipleSelection === undefined) {
        return;
      }
      ElMessageBox.confirm("Are you sure to delete this class", "Warning", {
        confirmButtonText: "Confirm",
        cancelButtonText: "Cancel",
        type: "warning",
      })
        .then(() => {
          let courseId = [];
          this.multipleSelection.forEach((e) => {
            var course = toRaw(e);
            courseId.push(course.id);
          });
          var data = { sid: this.id, cids: courseId };
          // Send request to delete batch classes at once
          this.cancellation(data);
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "Delete canceled",
          });
        });
    },
  },
  created() {
    this.id = this.$cookies.getCookie("id");
    this.getCourse();
    window.vue = this;
  },
};
</script>
<style scope>
.title {
  width: 100%;
  height: 65px;
  text-align: center;
}

.title h1{
  font-family: 'Lucida Sans';
  color: rgb(7, 107, 153);
  height: 20px;
  font-size: 30px;
}

.el-card {
  width: 100%;
  height: 100%;
}

.el-dialog__header{
  text-align: center;
  
}

.el-dialog__title{
  font-size: 20px;
  font-style: bold;
}

#selectForm .el-form-item__label {
  font-size: 15px;
  font-style: bold;
}
</style>
