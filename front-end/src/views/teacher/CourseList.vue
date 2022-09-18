<template>
  <div class="main">
    <el-header>
      <div class="title">
        <h1>Class Manage</h1>
        <el-button type="success" style="  width:12% " @click="show"> Add Class </el-button>
        <el-button type="danger" style="  width:12% " @click="remove"> Remove Selected </el-button>
        <el-button type="primary" style="  width:12% " @click="getCourse"> Refresh Lists </el-button>
      </div>
    </el-header>
    <el-main>
      <el-card style="width: 100%">
        <el-table
          :data="tableData"
          border
          @selection-change="handleSelectionChange"
          :header-cell-style="{background:'#eef1f6',color:'#606266',fontSize:'15px'}"
          :cell-style="{color: '#666', fontFamily: 'Arial',fontSize:'15px'}"
        >
          <el-table-column type="selection" width="55"> </el-table-column>
          <el-table-column prop="id" label="ID" width="60"> </el-table-column>
          <el-table-column prop="createTime" label="Creation Date" width="130">
          </el-table-column>
          <el-table-column prop="name" label="Class Name"> </el-table-column>
          <el-table-column prop="address" label="Class Location"> </el-table-column>
          <el-table-column prop="beginTime" label="Class Time"> </el-table-column>
          <el-table-column prop="week" label="Weekly Time"> </el-table-column>
          <el-table-column prop="count" label="Attendance Score"> </el-table-column>
          <el-table-column label="Operate" width="300">
            <template #default="prop">
              <div class = "btn">
              <el-button
                style="  width:50% " round
                type="primary"
                @click="checkMember(prop.row)"
                >View Members</el-button
              ><br>
              </div>
              <div class ="btn">
              <el-button style="  width:50% " round type="warning" @click="modified(prop.row)"
                >Edit Class Info</el-button
              ><br>
              </div>
              <div class = "btn">
              <el-button style="  width:50% " round type="success" @click="join(prop.row)"
                >Invite to Join </el-button
              > 
              </div>
            </template>

          </el-table-column>
        </el-table>
      </el-card>
      <!-- Add Course dialog -->
      <el-dialog
        draggable="true"
        title="Add Class"
        v-model="showAdd"
        width="30%"
        :before-close="handleClose"
      >
        <el-form
          ref="ruleFormRef"
          :model="courseModel"
          :rules="courseModelRules"
          label-width="120px"
          title="addform"
          class="demo-ruleForm"
        >
          <el-form-item label="Class Name" prop="name">
            <el-input v-model="courseModel.name"></el-input>
          </el-form-item>
          <el-form-item label="Class Location" prop="address" required>
            <el-input v-model="courseModel.address"></el-input>
          </el-form-item>
          <el-form-item label="Class Duration" prop="duration" required>
            <el-input-number
              v-model="courseModel.duration"
              :min="1"
              @change="handleChange1"
            />
          </el-form-item>
          <el-form-item label="Class Time" required prop="beginTime">
            <el-time-picker
              disabled-seconds
              v-model="courseModel.beginTime"
              placeholder="Start Time"
            >
            </el-time-picker>
          </el-form-item>
          <el-form-item label="Weekly Time" required>
            <el-select
              v-model="courseModel.week"
              clearable
              placeholder="Select"
            >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Attendance Score">
            <el-input-number
              v-model="courseModel.count"
              :min="1"
              @change="handleChange"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showAdd = false">Cancel</el-button>
          <el-button type="primary" @click="addCourse">Add</el-button>
        </template>
      </el-dialog>
      <!-- Edit Course info dialog -->
      <el-dialog
        title="Edit Class"
        v-model="showModified"
        width="30%"
        :before-close="handleUpdClose"
      >
        <el-form
          ref="modifiedCourseRef"
          :model="modifiedCourse"
          :rules="courseModelRules"
          label-width="120px"
          class="demo-ruleForm"
        >
          <el-form-item label="Class Name" prop="name">
            <el-input v-model="modifiedCourse.name"></el-input>
          </el-form-item>
          <el-form-item label="Class Location" prop="address" required>
            <el-input v-model="modifiedCourse.address"></el-input>
          </el-form-item>
          <el-form-item label="Class Duration" prop="duration" required>
            <el-input-number
              v-model="modifiedCourse.duration"
              :min="1"
              @change="handleModChange1"
            />
          </el-form-item>
          <el-form-item label="Class Time" required>
            <el-time-picker v-model="time" placeholder="Start Time">
            </el-time-picker>
          </el-form-item>
          <el-form-item label="Weekly Time" required>
            <el-select
              v-model="modifiedCourse.week"
              clearable
              placeholder="Select"
            >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Attendance Score">
            <el-input-number
              v-model="modifiedCourse.count"
              :min="1"
              @change="handleModChange"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showModified = false">Cancel</el-button>
          <el-button type="primary" @click="updCourse">Confirm</el-button>
        </template>
      </el-dialog>
      <!-- View the member lists dialog -->
      <el-dialog
        title="Member Lists"
        v-model="checkMemberShow"
        width="60%"
        :before-close="handleCheckClose"
      >
        <el-card>
          <el-input v-model="keyword" placeholder="Please input">
            <template #prepend>
              <el-select
                v-model="select"
                placeholder="Select"
                style="width: 100px"
              >
                <el-option label="Number" value="number"></el-option>
                <el-option label="FirstName" value="firstName"></el-option>
                <el-option label="LastName" value="lastName"></el-option>
                <el-option label="All" value="all"></el-option>
              </el-select>
            </template>
            <template #append>
              <el-button @click="query">
                <el-icon><search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </el-card>
        <el-table
          :data="memberList"
          border
          style="width: 100%; margin-top: 25px"
          @selection-change="handleMemberSelectionChange"
        >
          <el-table-column type="selection" width="55"> </el-table-column>
          <el-table-column prop="number" label="Student ID" width="90" />
          <el-table-column prop="name" label="Name" width="120" />
          <el-table-column label="Attendance Score">
            <template #default="prop">
              <el-progress
                :percentage="prop.row.progress"
                :color="customColor"
              />
            </template>
          </el-table-column>
          <el-table-column label="Operate">
            <template #default="prop">
              <el-popover
                v-model:visible="visible"
                placement="top"
                :width="180"
              >
                <el-input-number
                  :min="1"
                  v-model="signCount1"
                ></el-input-number>
                <div style="text-align: right; margin: 0">
                  <el-button size="small" round type="text" @click="visible = false"
                    >Cancel</el-button
                  >
                  <el-button size="small" round type="primary" @click="signature"
                    >Sign-in</el-button
                  >
                </div>
                <template #reference>
                  <div class ="btn">
                  <el-button style="  width:50% text-align : center" round type="success" @click="sign(prop.row)"
                    >Help sign-in</el-button
                  ><br>
                  </div>
                </template>
              </el-popover>
              <div class = "btn">
              <el-button style="  width:50%  text-alin : center" round type="danger" @click="delStudent(prop.row)"
                >Delete Student</el-button
              ><!--Delete student-->
              </div>
            </template>
          </el-table-column>
        </el-table>
        <!-- divide page function -->
        <br />
        <el-pagination
          background
          layout="prev, pager, next"
          :current-page="page"
          @current-change="changePage"
          :total="total"
        >
        </el-pagination>
        <template #footer>
          <el-button type="danger" @click="batchDel">Multiple Delete</el-button>
          <el-button type="warning" @click="showBatchSign">Multiple Sign-in</el-button>
          <el-button type="primary" @click="checkMemberShow = false"
            >Close</el-button
          >
        </template>
      </el-dialog>
      <!-- Sign-in score pop-up window -->
      <el-dialog
        title="Set Attendance Score"
        v-model="settingSignCount"
        width="30%"
        :before-close="handleSignSetCountClose"
      >
        <el-input-number :min="1" v-model="signCount"></el-input-number>
        <template #footer>
          <el-button type="warning" @click="batchSignature">Sign-in</el-button>
          <el-button type="primary" @click="settingSignCount = false"
            >Close</el-button
          >
        </template>
      </el-dialog>
      <!-- Invite student to join pop-up window -->
      <el-dialog
        title="Invite student to join"
        v-model="showJoin"
        width="50%"
        :before-close="handleJoinClose"
      >
        <el-card>
          <el-input v-model="JoinKeyword" placeholder="Please input">
            <template #prepend>
              <el-select
                v-model="joinSelect"
                placeholder="Select"
                style="width: 110px"
              >
                <el-option label="Number" value="number" width="55"></el-option>
                <el-option label="FirstName" value="firstName"></el-option>
                <el-option label="LastName" value="lastName"></el-option>
                <el-option label="All" value="all"></el-option>
              </el-select>
            </template>
            <template #append>
              <el-button @click="queryJoin">
                <el-icon><search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </el-card>
        <!-- The table shows the students that can be invited -->
        <el-table
          :data="joinMemberList"
          border
          style="width: 100%; margin-top: 25px"
          @selection-change="handleMemberSelectionChange"
        >
          <el-table-column type="selection" width="55"> </el-table-column>
          <el-table-column prop="number" label="Student Number" width="150" />
          <el-table-column prop="name" label="Name" width="150" />
          <el-table-column prop="email" label="Email" />
          <el-table-column label="Operation">
            <template #default="prop">
              <el-button type="success" @click="sendJoin(prop.row)"
                >Send Invite</el-button
              >
            </template>
          </el-table-column>
        </el-table>
        <!-- pager function -->
        <br />
        <el-pagination
          background
          layout="prev, pager, next"
          :current-page="joinPage"
          @current-change="joinChangePage"
          :total="total"
        >
        </el-pagination>
        <template #footer>
          <el-button type="primary" @click="showJoin = false">Close</el-button>
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
import { ElMessage } from "element-plus";
import { Search } from "@element-plus/icons-vue";
export default {
  name: "teacherCourse",
  components: {
    Search,
  },
  setup() {
    const router = useRouter();
    const data = reactive({
      showAdd: false,
      base_url: "http://localhost:5000/",
      tableData: [],
      select: "",
      keyword: "",
      page: 1,
      total: 0,
      options: [
        {
          value: 1,
          label: "Monday",
        },
        {
          value: 2,
          label: "Tuesday",
        },
        {
          value: 3,
          label: "Wednesday",
        },
        {
          value: 4,
          label: "Thursday",
        },
        {
          value: 5,
          label: "Friday",
        },
        {
          value: 6,
          label: "Saturday",
        },
        {
          value: 7,
          label: "Sunday",
        },
      ],
      courseModel: {
        id: 0,
        address: "",
        name: "",
        teacher: 0,
        beginTime: "",
        count: 1,
        week: "",
        duration: 60,
      },
      courseModelRules: {
        name: [
          { required: true, message: "Class Name cannot be empty！", trigger: "blur" },
        ],
        address: [
          { required: true, message: "Classroom cannot be empty！", trigger: "blur" },
        ],
        beginTime: [
          { required: true, message: "Start time cannot be empty！", trigger: "blur" },
        ],
        week: [
          { required: true, message: "Weekly time cannot be empty！", trigger: "blur" },
        ],
      },
      multipleSelection: [],
      modifiedCourse: {},
      showModified: false,
      checkMemberShow: false,
      memberList: [],
      tableData: [],
      customColor: [
        { color: "#f56c6c", percentage: 20 },
        { color: "#e6a23c", percentage: 40 },
        { color: "#5cb87a", percentage: 60 },
        { color: "#1989fa", percentage: 80 },
        { color: "#6f7ad3", percentage: 100 },
      ],
      // Select Courses
      currentCourse: {},
      // Store selected students
      selectMembers: [],
      settingSignCount: false,
      // Default number of batch sign-in
      signCount: 1,
      visible: false,
      // Default number of single sign-in
      signCount1: 1,
      // Initializes the student to be signed
      member: {},
      time: new Date(),
      showJoin: false,
      selectJoinCourse: {},
      joinNumber: "",
      JoinKeyword: "",
      joinSelect: "",
      joinPage: "",
      // The default student invitation list
      joinMemberList: [],
    });
    return {
      ...toRefs(data),
    };
  },
  methods: {
    changePage(page) {
      this.page = page;
      this.query();
    },
    handleSignSetCountClose() {
      this.settingSignCount = false;
    },
    // Query student information under current course
    query() {
      var _than = this;
      var allCount = this.currentCourse.count;
      // Send a request to get a list of students registered for the current course
      var parms = {
        keyword: this.keyword,
        select: this.select,
        page: this.page,
      };
      this.$http
        .post(this.base_url + "api/t/getMember/" + this.currentCourse.id, parms)
        .then((res) => {
          if (res.data.code == 200) {
            _than.memberList = res.data.data;
            _than.memberList.forEach((e) => {
              e.progress = (e.score / allCount) * 100;
            });
            _than.total = res.data.total;
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
            message: "Request failed, Network  issued",
          });
        });
    },
    showBatchSign() {
      if (this.selectMembers.length != 0) {
        this.settingSignCount = true;
      }
    },
    // Batch sign-in
    batchSignature() {
      this.settingSignCount = false;
      this.signCount;
      var sids = [];
      toRaw(this.selectMembers).forEach((e) => {
        sids.push(toRaw(e).number);
      });
      var data = {
        sids: sids,
        count: this.signCount,
        cid: toRaw(this.currentCourse).id,
      };
      // Send batch sign-in request
      this.$http
        .post(this.base_url + "api/batchSignature", data)
        .then((res) => {
          if (res.data.code === 200) {
            ElMessage({
              type: "success",
              message: "Multiple Sign-in Successfull！",
            });
            this.query();
          } else {
            ElMessage({
              type: "error",
              message: res.data.msg,
            });
          }
        })
        .catch((res) => {});
    },
    // Batch delete students
    batchDel() {
      if (this.selectMembers.length != 0) {
        this.$confirm("This operation will kick student from class, Continue?", "Attention", {
          confirmButtonText: "Confirm",
          cancelButtonText: "Cancel",
          type: "warning",
        })
          .then(() => {
            var sids = [];
            toRaw(this.selectMembers).forEach((e) => {
              sids.push(e.number);
            });
            var _than = this;
            var id = toRaw(this.currentCourse).id;
            var parms = { sids: sids };
            this.$http
              .post(this.base_url + "api/t/batchDelStudent/" + id, parms)
              .then((res) => {
                if (res.data.code == 200) {
                  ElMessage({
                    type: "success",
                    message: "Kicked Successfull！",
                  });
                  _than.query();
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
                  message: "The Request Failed！",
                });
              });
          })
          .catch((res) => {});
      }
    },
    // delete single student
    delStudent(row) {
      this.$confirm("This operation will kick this selected student from class, Continue??", "Warning", {
        confirmButtonText: "Confirm",
        cancelButtonText: "Cancel",
        type: "warning",
      })
        .then(() => {
          var _than = this;
          var id = toRaw(this.currentCourse).id;
          // Send a request to back-end to delete student
          this.$http
            .get(
              this.base_url + "api/t/delStudent/" + toRaw(row).number + "/" + id
            )
            .then((res) => {
              if (res.data.code == 200) {
                ElMessage({
                  type: "success",
                  message: "Kicked Successfull！",
                });
                _than.query();
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
                message: "The Request Failed！",
              });
            });
        })
        .catch((res) => {});
    },
    // Manually sign-in
    sign(obj) {
      //Get the ID from the student object and then resign
      this.member = obj;
    },
    // Send a single manually sign-in request
    signature() {
      // Gets the students to be re-signed
      var member = toRaw(this.member);
      var data = {
        number: member.number,
        count: this.signCount1,
        cid: toRaw(this.currentCourse).id,
      };
      // Send request to perform re-signed request to the back-end
      console.log(data);
      this.$http
        .post(this.base_url + "api/signature", data)
        .then((res) => {
          if (res.data.code === 200) {
            ElMessage({
              type: "success",
              message: "Help Sign-in Successful！",
            });
            this.query();
          } else {
            ElMessage({
              type: "error",
              message: res.data.msg,
            });
          }
          this.visible = false;
        })
        .catch((res) => {});
    },
    info() {},
    handleMemberSelectionChange(rows) {
      this.selectMembers = rows;
    },
    handleChange1(number) {
      this.courseModel.duration = number;
    },
    handleChange(number) {
      this.courseModel.count = number;
    },
    handleJoinClose() {
      this.showJoin = false;
    },
    handleUpdClose() {
      this.$refs.modifiedCourseRef.resetFields();
      this.showModified = false;
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
    remove() {
      var _than = this;
      if (this.multipleSelection.length !== 0) {
        this.$confirm("This operation will delete selected class, Continue?", "Attention", {
          confirmButtonText: "Confirm",
          cancelButtonText: "Cancel",
          type: "warning",
        })
          .then(() => {
            // Delete selected course
            var ids = [];
            toRaw(_than.multipleSelection).forEach((e) => {
              ids.push(e.id);
            });
            _than.$http
              .post(_than.base_url + "api/t/remove", ids)
              .then((res) => {
                if (res.data.code == 200) {
                  _than.$message({
                    type: "success",
                    message: "Delete Successfull",
                  });
                  _than.getCourse();
                }
              })
              .catch((res) => {});
          })
          .catch((res) => {
            console.log(res);
            this.$message({
              type: "info",
              message: "Delete Cancelled",
            });
          });
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleModChange(number) {
      this.modifiedCourse.count = number;
    },
    handleCheckClose() {
      this.checkMemberShow = false;
    },
    handleModChange1(number) {
      this.modifiedCourse.duration = number;
    },
    // View member list under current Course
    checkMember(row) {
      this.checkMemberShow = true;
      this.currentCourse = toRaw(row);
      this.query();
    },
    // modifed the Course
    modified(row) {
      
      this.showModified = true;
      this.modifiedCourse = row;
      this.modifiedCourse.beginTime = beginTime;
    },
    // Edit Course info
    updCourse() {
      var _than = this;
      this.$refs.modifiedCourseRef.validate((value) => {
        if (value) {
          var date = this.time;
          this.modifiedCourse.beginTime =
            date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
          this.$http
            .post(this.base_url + "api/updCourse", this.modifiedCourse)
            .then(function (res) {
              if (res.data.code === 200) {
                _than.$message({
                  type: "success",
                  message: res.data.msg,
                });
                _than.showModified = false;
                _than.getCourse();
              } else {
                _than.$message({
                  type: "error",
                  message: res.data.msg,
                });
              }
              _than.showModified = false;
            })
            .catch((res) => {
              console.log(res);
              _than.$message({
                type: "error",
                message: "Network issue, Failure to change",
              });
            });
        }
      });
    },
    getCourse() {
      var _than = this;
      this.$http
        .get(this.base_url + "api/t/" + this.courseModel.teacher + "/getCourse")
        .then(function (res) {
          if (res.data.code === 200) {
            _than.$message({
              type: "success",
              message: "Get Class Lists Successful！",
            });
            _than.tableData = res.data.data;
          } else {
            _than.$message({
              type: "error",
              message: "Get Class Lists Failure！",
            });
          }
        })
        .catch((res) => {
          _than.$message({
            type: "error",
            message: "Network Issue, Failure to get",
          });
        });
    },
    handleClose() {
      this.showAdd = false;
      this.$refs.ruleFormRef.resetFields();
    },
    addCourse() {
      var _than = this;
      this.$refs.ruleFormRef.validate((value) => {
        if (value) {
          var date = this.courseModel.beginTime;
          console.log(date);
          this.courseModel.beginTime =
            date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
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
            .catch((res) => {});
        }
      });
    },
    joinChangePage(page) {
      this.joinPage = page;
    },
    join(row) {
      this.selectJoinCourse = row;
      this.showJoin = true;
      // Query the list of students who are not registered for the current course
      this.queryJoin();
    },
    sendJoin(row) {
      var id = this.$cookies.getCookie("id");
      var cid = toRaw(this.selectJoinCourse).id;
      var emails = [toRaw(row).email];
      var data = {
        id: id,
        cid: cid,
        emails: emails,
      };
      this.requestJoin(data);
      console.log(data)
    },
    // Send email invitation request
    requestJoin(data) {
      var _than = this;
      this.$http
        .post(this.base_url + "api/t/sendEmail", data)
        .then((res) => {
          if (res.data.code == 200) {
            ElMessage({
              type: "success",
              message: "Invitation sent successful！",
            });
            _than.showJoin = false;
            _than.queryJoin();
          } else {
            ElMessage({
              type: "error",
              message: "Invitation sent Failed！",
            });
          }
        })
        .catch((res) => {
          ElMessage({
            type: "error",
            message: "Request send failed！Please check Network！",
          });
        });
    },
    queryJoin() {
      var _than = this;
      // query students who are not in this course
      var data = {
        keyword: this.JoinKeyword,
        select: this.joinSelect,
        cid: toRaw(this.selectJoinCourse).id,
      };
      this.$http
        .post(this.base_url + "api/t/getMemberNotExists", data)
        .then((res) => {
          if (res.data.code == 200) {
            _than.joinMemberList = res.data.data;
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
            message: "Request Failed！Error Occur！",
          });
        });
    },
    show() {
      this.showAdd = true;
      this.$refs.ruleFormRef.resetFields();
    },
  },
  created() {
    this.courseModel.teacher = this.$cookies.getCookie("id");
    this.getCourse();
  }
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

.el-header{
  margin-bottom: 20px;
  display:block;
  /* position: fixed; */
  /* position: absolute; */
}
.el-table {
  width: 100%;
  /* margin-left: 30%; */
}

#main {
  width: 100%;
  margin: 0 auto;
}

.btn {
  text-align: center;
  margin-top: 5px;
  margin-bottom: 10px;
}

.el-dialog__header{
  text-align: center;
  background-color: #cde0eb;
}

.el-dialog__title{
  font-size: 25px;
  font-style: bold;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}


</style>
