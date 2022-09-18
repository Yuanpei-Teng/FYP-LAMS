<template>
  <el-scrollbar>
    <div class="banner">
      <h1>Class Attendance</h1>
      <el-card>
        <el-input v-model="keyword" placeholder="Please enter Class Name/ID">
          <template #append>
            <el-button @click="query">
              <el-icon><search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </el-card>
    </div>
    <div class="tabledata" v-if="showResult">
      <el-card>
        <el-table :data="tableData" border :header-cell-style="{background:'#eef1f6',color:'#606266',fontSize:'15px'}"
          :cell-style="{color: '#666', fontFamily: 'Arial',fontSize:'15px'}" style="width: 100%">
          <el-table-column prop="id" label="ID" width="180" />
          <el-table-column prop="name" label="Class Name" width="180" />
          <el-table-column prop="address" label="Classroom" />
          <el-table-column prop="beginTime" label="Start Time" />
          <el-table-column prop="duration" label="Duration" />
          <el-table-column label="Operate">
            <template #default="prop">
              <el-button type="success" @click="sign(prop.row)">Sign-in</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    <el-dialog
      v-model="startSign"
      title="face recognize"
      width="100%"
      :before-close="handleClose"
    > 
      <FaceScan :cid="cid"/>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="startSign = false">Close</el-button>
        </span>
      </template>
    </el-dialog>
  </el-scrollbar>
</template>

<script>
import { toRefs, reactive } from "vue";
import { Search } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import FaceScan from "./FaceScan.vue";
export default {
  name: "signCourse",
  components: {
    Search,
    FaceScan,
  },
  setup() {
    const router = useRouter();
    const data = reactive({
      base_url: "http://localhost:5000/",
      tid: 0,
      keyword: "",
      select: "",
      showResult: false,
      startSign: false,
      tableData: [],
      cid:0,
    });
    return {
      ...toRefs(data),
    };
  },
  created() {
    this.tid = this.$cookies.getCookie("id");
  },
  methods: {
    handleClose() {
      this.startSign = false;
    },
    //   Search for a course
    query() {
      var _than = this;
      var data = { tid: this.tid, keyword: this.keyword, select: this.select };
      this.$http
        .post(this.base_url + "api/t/searchCourse", data)
        .then((res) => {
          if (res.data.code == 200) {
            _than.tableData = res.data.data;
            this.showResult = true;
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
    },
    // Start real-time sign-in
    sign(row) {
      this.cid = row.id;
      this.startSign = true;

    },
  },
};
</script>

<style>
.tabledata {
  margin-top: 120px;
}
.tabledata .el-card {
  width: 100%;
  height: 50%;
}
.l_v {
  float: left;
  margin-left: 5%;
}
#main {
  margin-top: 10px;
}
.banner .el-card {
  width: 50%;
  margin: 0 auto;
}

.banner h1{
  font-family: 'Lucida Sans';
  color: rgb(7, 107, 153);
  height: 20px;
  font-size: 30px;
}
</style>
