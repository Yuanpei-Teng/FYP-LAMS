import router from './index'
router.beforeEach((to, from, next) => {
    // If the request is enrol the class, then allow the request and give the permission
    var paths = to.path.split("/")
    if (paths.length == 5) {
        if (paths[1] == "customer" && paths[2] == "add" && paths[3] == "course") next()
    } else {
        var id = ""
        var arr, reg = new RegExp("(^| )" + "id" + "=([^;]*)(;|$)");
        if (arr = document.cookie.match(reg)) {
            id = unescape(arr[2])
        }
        if (id == "" || id == undefined || id === null) {
            if (to.path == "/") {
                next()
            } else {
                next("/")
            }
        } else {
            next()
        }

    }

})