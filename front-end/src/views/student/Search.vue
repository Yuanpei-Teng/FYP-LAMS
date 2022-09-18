<template>
  <div class="main">
    <el-header>
      <div class="title">
        <h1>Search Class</h1>
      </div>
    </el-header>
    <el-main>
      <el-card class="searchTable">
        <el-input v-model="search" placeholder="Please enter Class/ID" clearable>
          <template #append>
            <el-button @click="query">
              <el-icon><search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </el-card>
      <el-card v-if="show" style="margin-top: 50px" class="resultMain">
        <h1 style="margin: 0 auto; text-align:center;">Search Result</h1>
        <div style="float: right; margin-top: -30px">
          <el-popconfirm title="Are you sure to add this class?" @confirm="batchAdd">
            <template #reference>
              <el-button style="margin-right: 55px;" size="small" type="success">Add</el-button>
            </template>
          </el-popconfirm>
        </div>
        <br />
        <el-table
          ref="studentRef"
          :data="tableData"
          border
          @selection-change="handleSelectionChange"
          @select="selectRow"
          :header-cell-style="{background:'#eef1f6',color:'#606266',fontSize:'15px'}"
          :cell-style="{color: '#666', fontFamily: 'Arial',fontSize:'15px'}"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="Class Name" />
          <el-table-column prop="teacher" label="Teacher" width="120">
          </el-table-column>
          <el-table-column prop="address" label="Classroom"> </el-table-column>
          <el-table-column prop="beginTime" label="Class Time"> </el-table-column>
          <el-table-column label="Operate" width="120">
            <template #default="prop">
              <el-popconfirm
                v-if="!prop.row.exists"
                title="Are you sure to add this class！"
                @confirm="add(prop.row)"
              >
                <template #reference>
                  <el-button size="small" type="success">Add</el-button>
                </template>
              </el-popconfirm>
              <el-button v-else size="small" type="info" disabled
                >Added</el-button
              >
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          v-model:currentPage="currentPage"
          v-model:page-size="size"
          :page-sizes="[5, 10, 20, 50]"
          :small="small"
          layout="sizes, prev, pager, next"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
        </el-pagination>
      </el-card>
    </el-main>
  </div>
</template>
<script>
// @ is an alias to /src
import { reactive, toRefs, ref, onMounted } from "vue";
import { toRaw } from "@vue/reactivity";
import { useRouter } from "vue-router";
import { Search } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
export default {
  name: "courseSearch",
  components: { Search },
  setup() {
    const router = useRouter();
    const data = reactive({
      search: "",
      id: 0,
      count: 10,
      base_url: "http://localhost:5000/",
      currentPage: 1,
      total: 0,
      size: 10,
      show: false,
      tableData: [],
    });

    onMounted(() => {
    });
    return {
      ...toRefs(data),
    };
  },
  created() {
    this.id = this.$cookies.getCookie("id");
  },
  methods: {
    info() {},
    query() {
      var _than = this;
      // Send Search Course request
      var data = {
        keyword: this.search,
        id: this.id,
        page: this.currentPage,
        size: this.size,
      };
      this.$http
        .post(this.base_url + "api/s/searchCourse", data)
        .then((res) => {
          if (res.data.code == 200) {
            _than.tableData = res.data.data;
            _than.total = res.data.total;
            _than.showResult = true;
          } else {
            ElMessage({
              type: "error",
              message: res.data.msg,
            });
          }
        })
        .catch((res) => {});
      this.show = true;
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
    batchAdd() {
      if (this.multipleSelection === undefined) {
        return;
      }
      let courseId = [];
      this.multipleSelection.forEach((e) => {
        var course = toRaw(e);
        courseId.push(course.id);
      });
      var data = { id: this.id, cids: courseId };
      // Send request to add multiple Courses at once
      this.addCourse(data);
    },
    add(row) {
      //Add a single class
      var course = toRaw(row);
      console.log(course);
      if (!course.exists) {
        var data = { id: this.id, cids: [course.id] };
        // Send add Course Request
        this.addCourse(data);
      }
    },
    addCourse(data) {
      this.$http
        .post(this.base_url + "api/s/batchAddCourse", data)
        .then((res) => {
          if (res.data.code == 200) {
            ElMessage({
              type: "success",
              message: "Add Class Success！",
            });
            this.query();
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
            message: "The request went Wrong！",
          });
        });
    },
    handleSizeChange(size) {
      //This function is triggered when the current number of pages in the web changes
      this.size = size;
      this.query();
    },
    handleCurrentChange(page) {
      //The pager function
      this.page = page;
      this.query();
    },
    selectRow(selection, row) {
      if (!toRaw(row).exists) {
        this.$refs.studentRef.toggleRowSelection(row, true);
      } else {
        ElMessage({
          type: "info",
          message: "You already added this class, do not add repeatly",
        });
      }
    },
    handleSelectionChange(val) {
      var temp = [];
      val.forEach((e) => {
        if (!toRaw(e).exists) {
          temp.push(e);
        } else {
          this.$refs.studentRef.toggleRowSelection(e,true);
        }
      });
      this.multipleSelection = temp;
    },
  },
};
</script>
<style scope>
.searchTable {
  width: 50%;
  margin: 0 auto;
}
</style>
