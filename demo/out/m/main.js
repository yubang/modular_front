var a=1;var b=new Array();var c=false;var d=new Vue({el:'#blogs',data:{objs:[]},ready:function(){$("#button").trigger('click');}});function e(){if(c)return;c=true;$.ajax({type:'GET',url:'/api/v1/get_a_page_of_blog',data:{page:a},dataType:'json',timeout:10000,success:function(e){if(e.blogs.length==0)$("#button").hide();b=b.concat(e.blogs);d.$set('objs',b);a++;c=false;},error:function(a,b){c=false;alert('服务器无法响应！');}});}function f(){var a=window.location.pathname;urls=a.split('/');return urls[urls.length-1];}$.ajax({type:'POST',url:'/api/v1/find_blog',data:{"blog_id":f()},dataType:'json',timeout:10000,success:function(a){if(a.length==0){alert('你访问的博客不存在');location.href='/';}else{$("#title").html(a.title);document.title=a.title;new Vue({el:'#content',data:{"message":a.html}});}},error:function(a,b){alert('服务器无法响应！');}});