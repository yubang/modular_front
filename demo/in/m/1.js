    var page = 1
    var datas = new Array()
    var lock = false
    var vm = new Vue({
        el: '#blogs',
        data: {
            objs: []
        },
        ready: function(){
            $("#button").trigger('click')
        }
    })

    function get_a_page_data(){

        if(lock){
            return
        }
lock = true
$.ajax({
  type: 'GET',
  url: '/api/v1/get_a_page_of_blog',
  data: {page: page},
  dataType: 'json',
  timeout: 10000,
  success: function(data){
  if(data['blogs'].length == 0){
            $("#button").hide()
        }

        datas = datas.concat(data['blogs'])

        vm.$set('objs', datas)

        page++
        lock = false
  },
  error: function(xhr, type){
  lock = false
    alert('服务器无法响应！')
  }
})

}