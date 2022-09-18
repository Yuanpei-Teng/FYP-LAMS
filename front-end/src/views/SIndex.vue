<template>
  <el-container
    class="layout-container-demo"
    style="height: 750px; border: 2px solid #eee"
  >
    <el-aside :class="tt" style="background-color: rgb(238, 241, 246)">
      <el-scrollbar>
        <el-menu
          unique-opened
          default-active="1"
          ref="menus"
          @select="changeMenu"
        >
          <el-menu-item-group>
            <template #title>
              <el-icon style="font-size:25px;"><management /></el-icon>&nbsp;
              <span style="font-size:15px; color:Black;"><strong>Class Manage</strong></span>
            </template>
            <el-menu-item index="1"
              >&nbsp;&nbsp;
              <el-icon style="font-size:20px;margin-right:5px;"><search /></el-icon>&nbsp;Search Class</el-menu-item
            >
            <el-menu-item index="2">
              &nbsp;&nbsp;
              <el-icon style="font-size:20px;margin-right:5px;"><list /></el-icon>
              Class List
            </el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group>
            <template #title>
              <el-icon style="font-size:25px;"><avatar /></el-icon>&nbsp;
              <span style="font-size:15px; color:Black;"><strong>Person</strong></span>
            </template>
            <el-menu-item index="3">
              &nbsp;&nbsp;
              <el-icon style="font-size:20px;margin-right:2px;"><key /></el-icon>
              Change Password</el-menu-item
            >
            <el-menu-item index="4">
              &nbsp;&nbsp;&nbsp;
              <el-icon style="font-size:15px;margin-right:5px;"><info-filled /></el-icon>
              Edit Profile</el-menu-item
            >
            <el-menu-item index="5">
              &nbsp;&nbsp;&nbsp;
              <el-icon style="font-size:15px;margin-right:5px;"><info-filled /></el-icon>
              Face Model</el-menu-item
            >
          </el-menu-item-group>

          
          <el-button style="text-align:center; margin-top:85px;margin-left:15px;" @click="logout">
            &nbsp;&nbsp;
            <el-icon style="text-align:center;margin-right:15px;"><home-filled /></el-icon>
            <strong>Log Out</strong>
          </el-button>
        </el-menu>
      </el-scrollbar>
    </el-aside>
    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <div class="expand" @click="switchExpand">
          <el-icon v-if="tt == 'tt1'" :size="25"><expand /></el-icon>
          <el-icon v-else :size="25"><fold /></el-icon>
          &nbsp;&nbsp;&nbsp;
          <h1 style="color: black; cursor: pointer">{{ warn }}</h1>
        </div>
        <div class="toolbar">
          <el-dropdown>
            <el-icon style="margin-right: 8px; margin-top: 1px; font-size:25px;"
              ><setting
            /></el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout"><strong>Log Out</strong></el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <span style="font-size:15px;"><strong>{{ loginName }}</strong></span>
        </div>
      </el-header>
      <el-main>
        <el-scrollbar>
          <CourseSearch v-if="activateMenu == 1" />
          <CourseList v-if="activateMenu == 2" />
          <ChangePwd v-if="activateMenu == 3" />
          <ChangeInfo v-if="activateMenu == 4" />
          <FaceRecord v-if="activateMenu == 5" />
        </el-scrollbar>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, toRefs, toRow, reactive, onMounted } from "vue";
import {
  Key,
  Message,
  Menu as IconMenu,
  Setting,
  Expand,
  Fold,
  Avatar,
  Location,
  Management,
  InfoFilled,
  List,
  Search,
  Edit,
  HomeFilled,
} from "@element-plus/icons-vue"; // import the icons from element-plus
import CourseList from "./student/CourseList.vue"; // import CourseList.vue as a component
import CourseSearch from "./student/Search.vue"; // import Search.vue as a component
import FaceRecord from "./student/FaceRecord.vue"; // import FaceRecord.vue as a component
import ChangeInfo from "./student/ChangeInfo.vue"; // import ChangeInfo.vue as a component
import ChangePwd from "./student/ChangePwd.vue"; // import ChangePwd.vue as a component
import { useRouter } from "vue-router"; 
export default {
  name: "studentIndex",
  components: {
    ChangePwd,
    FaceRecord,
    ChangeInfo,
    CourseSearch,
    CourseList,
    Edit,
    Search,
    List,
    InfoFilled,
    Key,
    Management,
    Location,
    Fold,
    Expand,
    Message,
    IconMenu,
    Setting,
    Avatar,
    HomeFilled,
  },
  setup() {
    const router = useRouter();
    const data = reactive({
      base_url: "http://localhost:5000/",
      warn: "",
      loginName: "John",
      isCollapse: false,
      tt: "tt1", //set the side bar open default
      activateMenu: 1, //initialize start page index is 1 which is CourseSearch
    });
    const item = {
      date: "2016-05-02",
      name: "Tom",
      address: "No. 189, Grove St, Los Angeles",
    };
    const tableData = ref(Array(20).fill(item));
    const menus = ref(null);
    onMounted(() => {});
    return {
      ...toRefs(data),
      tableData,
      item,
      router,
    };
  },
  created() {
    // Fixed button misalignment
    var count = window.sessionStorage.getItem("count");
    if (count == null) {
      this.router.go(0);
      window.sessionStorage.setItem("count", 1);
    } else {
    }
    // Get name of student
    this.id = this.$cookies.getCookie("id");
    this.getName();
    window.vue = this;
  },
  methods: {
    getName() {
      this.$http
        .get(this.base_url + "api/s/getName/" + this.id)
        .then((res) => {
          if (res.data.code == 200) {
            window.vue.loginName = res.data.name;
            if (!res.data.feature) {
              window.vue.warn = "You have not upload your face model yet, You cannot perform Class sign-in！";
            }
          }
        })
        .catch((res) => {});
    },
    logout() {
      this.$cookies.delCookie("id");
      window.sessionStorage.removeItem("count");
      window.location.href = "/";
    },
    changeMenu(index) {
      this.activateMenu = index;
    },
    handleOpen() {
      this.tt = "tt1"; //open the side bar
    },
    handleClose() {
      this.tt = "tt";//close the side bar
    },
    switchExpand() {
      this.isCollapse = this.isCollapse ? false : true;
      this.tt = "tt1" == this.tt ? "tt" : "tt1";
    },
  },
};
</script>

<style scoped>
.layout-container-demo{
  height: 100%;
  width: 100%;
}
.layout-container-demo .el-header {
  position: relative;
  background-color: #c3d5f1;
  color: var(--el-text-color-primary);
}
.tt {
  width: 0px;
  color: var(--el-text-color-primary);
  background: #fff !important;
  border-right: solid 1px #e6e6e6;
  box-sizing: border-box;
}
.tt1 {
  width: 200px;
  color: var(--el-text-color-primary);
  background: #fff !important;
  border-right: solid 1px #e6e6e6;
  box-sizing: border-box;
}
.layout-container-demo .el-menu {
  border-right: none;
}
.layout-container-demo .el-main {
  padding: 0;
}
.el-main {
  width: 100%;
  height: 100%;
}
.layout-container-demo .toolbar {
  position: absolute;
  display: inline-flex;
  align-items: center;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
}
.expand {
  position: absolute;
  display: inline-flex;
  align-items: center;
  top: 50%;
  left: 20px;
  transform: translateY(-50%);
}

html{
  height:100%;
}
</style>