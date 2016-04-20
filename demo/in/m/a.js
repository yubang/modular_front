    function get_end_args(){
        var url = window.location.pathname
        urls = url.split('/')
        return urls[urls.length - 1]
    }

$.ajax({
  type: 'POST',
  url: '/api/v1/find_blog',
  data: {"blog_id": get_end_args()},
  dataType: 'json',
  timeout: 10000,
  success: function(data){
    if(data.length == 0){
        alert('你访问的博客不存在')
        location.href = '/'
    }else{
        $("#title").html(data['title'])
        document.title = data['title']
        new Vue({
            el: '#content',
            data: {
                "message": data['html']
            }
        })
    }
  },
  error: function(xhr, type){
    alert('服务器无法响应！')
  }
})