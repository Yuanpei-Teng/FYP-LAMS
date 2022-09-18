<template>
  <el-scrollbar>
    <div class="main">
      <el-header>
        <div class="title">
          <h1>Search Student</h1>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <el-input v-model="keyword" placeholder="Please input">
            <template #prepend>
              <el-select
                v-model="select"
                placeholder="Select"
                style="width: 110px"
              >
                <el-option label="number" value="id"></el-option>
                <el-option label="firstName" value="firstName"></el-option>
                <el-option label="lastName" value="lastName"></el-option>
                <el-option label="all" value="all"></el-option>
              </el-select>
            </template>
            <template #append>
              <el-button @click="query">
                <el-icon><search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </el-card>
        <div v-if="showResult">
          <el-card style="margin-top: 50px" class="resultMain">
            <h1 style="margin: 0 auto">Search Result</h1>
            <br />
            <el-table :data="tableData" border style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="Name" width="120" />
              <el-table-column prop="address" label="Class" width="220">
              </el-table-column>
              <el-table-column label="Operate">
                <template #default="prop">
                  <el-popconfirm
                    title="Are you sure to help this student to sign-in for this class！"
                    @confirm="sign(prop.row)"
                  >
                    <template #reference>
                      <el-button
                        size="small"
                        type="success"
                        v-if="prop.row.id == 1"
                        disabled
                        >Help Sign-in</el-button
                      >
                      <el-button v-else size="small" type="success"
                        >Help Sign-in</el-button
                      >
                    </template>
                  </el-popconfirm>
                  <el-popconfirm
                    title="Are you sure to kicked out this student?"
                    @confirm="confirmDel(prop.row)"
                  >
                    <template #reference>
                      <el-button size="small" type="danger">Kicked</el-button>
                    </template>
                  </el-popconfirm>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              v-model:currentPage="currentPage"
              v-model:page-size="size"
              :page-sizes="[5, 10, 20, 50]"
              :small="small"
              layout="sizes, prev, pager, next"
              :total="1000"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            >
            </el-pagination>
          </el-card>
        </div>
      </el-main>
    </div>
  </el-scrollbar>
</template>
<script>
// @ is an alias to /src
import { reactive, toRefs, ref, onMounted } from "vue";
import { toRaw } from "@vue/reactivity";
import { useRouter } from "vue-router";
import { Search } from "@element-plus/icons-vue";
export default {
  name: "courseSearch",
  components: { Search },
  setup() {
    const router = useRouter();
    const data = reactive({
      keyword: "",
      id: 0,
      select: "",
      count: 10,
      base_url: "http://localhost:5000/",
      currentPage: 1,
      size: 10,
      showResult: false,
      tableData: [
        {
          id: "1",
          name: "Tom",
          address: "No. 189, Grove St, Los Angeles",
        },
        {
          id: "2",
          name: "Tom",
          address: "No. 189, Grove St, Los Angeles",
        },
        {
          id: "3",
          name: "Tom",
          address: "No. 189, Grove St, Los Angeles",
        },
        {
          id: "4",
          name: "Tom",
          address: "No. 189, Grove St, Los Angeles",
        },
      ],
    });
    return {
      ...toRefs(data),
      router,
    };
  },
  created() {
    this.id = this.$cookies.getCookie("id");
  },
  methods: {
    // Search for a student
    query() {
      if (this.keyword != "") {
        this.showResult = true;
        // Send search request
        var data = { id: this.id, keyword: this.keyword, select: this.select };
        this.$http
          .post(this.base_url + "api/t/getStudent", data)
          .then((res) => {
            console.log(res);
          })
          .catch((res) => {
            console.log(res);
          });
      }
    },
    sign(row) {
      console.log(row);
    },
    pickOut(row) {
      console.log(row);
    },
    changeSign(row) {
      var _than = this;
      this.current = row.cid;
      this.start = !this.start;
      if (this.start) {
        var data = { cid: row.cid, enable: row.enable };
        this.$http
          .get(this.base_url + "/sign_record/clear")
          .then(function (res) {
            console.log(res);
          })
          .catch((res) => {});
        open_camera();
      } else {
        close_camera();
      }
    },
    confirmDel(row) {
      console.log(row);
    },
    handleSizeChange(size) {},
    handleCurrentChange(page) {},
    remove() {
      var _than = this;
      if (this.multipleSelection.length !== 0) {
        this.$confirm("This operation will delete selected class, Continue?", "Attention", {
          confirmButtonText: "Confirm",
          cancelButtonText: "Cancel",
          type: "warning",
        })
          .then(() => {
            _than.remove1();
          })
          .catch((res) => {
            console.log(res);
            this.$message({
              type: "info",
              message: "Cancel Delete",
            });
          });
      }
    },
    remove1() {
      var _than = this;
      var cids = "";
      this.multipleSelection.forEach((e) => {
        cids += e.cid + ",";
      });
      var data = { cids: cids };
      this.$http
        .post(this.base_url + "api/t/remove", data)
        .then(function (res) {
          if (res.data.code === 200) {
            _than.$message({
              type: "success",
              message: "Move out Successful！",
            });
            _than.getCourse();
          } else {
            _than.$message({
              type: "error",
              message: "Move our Failed！",
            });
          }
        })
        .catch((res) => {
          console.log(res);
          _than.$message({
            type: "error",
            message: "Network issue,Failure to get",
          });
        });
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    getCourse() {
      var _than = this;
      this.$http
        .post(this.base_url + "api/t/" + _than.id + "/getStudent")
        .then(function (res) {
          if (res.data.code === 200) {
            _than.$message({
              type: "success",
              message: "Get class Lists Successful！",
            });
            _than.tableData = res.data.data;
            console.log(res.data.data);
          } else {
            _than.$message({
              type: "error",
              message: "Get Class Lists Failed！",
            });
          }
        })
        .catch((res) => {
          _than.$message({
            type: "error",
            message: "Network issue, Failure to retrive",
          });
        });
    },
    handleClose() {
      this.showAdd = false;
      this.$refs.courseModelRef.resetFields();
    },
    addCourse() {
      var _than = this;
      this.courseModel.enable = this.courseModel.enable ? 1 : 0;
      this.$http
        .post(this.base_url + "api/addCourse", this.courseModel)
        .then(function (res) {
          if (res.data.code === 200) {
            _than.$message({
              type: "success",
              message: res.data.msg,
            });
            _than.showAdd = false;
            _than.getCourse();
          } else {
            _than.$message({
              type: "error",
              message: res.data.msg,
            });
          }
          this.showAdd = false;
        })
        .catch((res) => {
          _than.$message({
            type: "error",
            message: "Network issue, Add failed",
          });
        });
    },
    show() {
      this.showAdd = true;
    },
    re_login() {
      window.location.href = "/";
    },
    cancel() {
      _than.$message({
        type: "warning",
        message: "Sign-in Cancelled",
      });
      close_camera();
      this.open = false;
    },
    tigger_sign(course) {
      console.log(course);
      _than.$message({
        type: "success",
        message: "Close Sign-in",
      });
    },
  },
};
</script>
<style scope>
.el-card {
  width: 50%;
  margin: 0 auto;
}

.re_success {
  color: red;
  font-size: 1.5em;
}

.title {
  width: 100%;
  height: 65px;
  text-align: center;
}

#main {
  width: 100%;
  margin: 0 auto;
}

.l_v {
  float: left;
  margin-left: 5%;
}

.el-table {
  width: 100%;
  /* margin-left: 30%; */
}

#main {
  width: 100%;
  margin: 0 auto;
}

.l_v {
  float: left;
  margin-left: 5%;
}
.resultMain {
  width: 52%;
  height: 100%;
}
</style>
