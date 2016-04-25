/**
 * @author: yubang
 * 一个自动生成各种前端组件的轮子
 * 我就是喜欢造轮子，每天一轮子，生活更美好O(∩_∩)O
 * codeman 一楼：沙发，o(^▽^)o给邦神点赞
 */

 function TheWheelsOfFrontEnd(){
        
        function pagingComponentLiLinkBind(domObj, html, hrefStr){
            var a = document.createElement("a");
            a.href = hrefStr;
            a.innerHTML = html;
            
            a.style.display = "inline-block";
            a.style.width = "50px";
            a.style.height = "50px";
            a.style.lineHeight = "50px";
            
            domObj.style.display = "inline";
            a.style.border = "1px solid #eee";
            
            domObj.appendChild(a);
            return domObj;
        }
        
        /**
         * 获取分页组件
         * @param linkNumber 要生成的链接数
         * @param pageNumber 总页数
         * @param nowPage 当前页数
         * @param linkData 每一页链接
         * @param firstData 首页链接
         * @param finalData 尾页链接
         * @param otherData 额外参数
         * @return 分页组件dom对象
         */
       this.getPagingComponent = function(linkNumber, pageNumber, nowPage, linkData, firstData, finalData, otherData){
            
            linkNumber = parseInt(linkNumber);
            pageNumber = parseInt(pageNumber);
            nowPage = parseInt(nowPage);
            
            var html = "";
            var ul = document.createElement("ul");
            ul.style.display = "inline-block";
            ul.style.textAlign = "center";
            
            var firstLi = document.createElement("li");
            firstLi = pagingComponentLiLinkBind(firstLi, "首页", firstData);
            var finalyLi = document.createElement("li");
            finalyLi = pagingComponentLiLinkBind(finalyLi, "尾页", finalData);
            
            //处理移过颜色问题
            firstLi.childNodes[0].onmouseover=function(){
                this.style.backgroundColor = "#eee";
            }
            firstLi.childNodes[0].onmouseout=function(){
                this.style.backgroundColor = "white";
            }
            finalyLi.childNodes[0].onmouseover=function(){
                this.style.backgroundColor = "#eee";
            }
            finalyLi.childNodes[0].onmouseout=function(){
                this.style.backgroundColor = "white";
            }
            
            // 算出每一个链接的页数，这是一个可怕的算法
            var tmpArr = [];
            var tmpNum = (linkNumber % 2 == 0) ? linkNumber + 1 : linkNumber;
            for(var i = 0; i<linkNumber; i++ ){
                tmpArr[i] = nowPage;
            }
            for(var i = parseInt(tmpNum/2),index = 0; i>=0; i--,index++){
                tmpArr[i] -= index;
            }
            for(var i = parseInt(tmpNum/2),index = 0; i<linkNumber; i++,index++){
                tmpArr[i] += index;
                
            }
            
            //填充按钮
            var totalButton = 0;
            for(var index=0;index<linkNumber ; index++){
                if(tmpArr[index]<=0){
                    continue;
                }else if(tmpArr[index]>pageNumber){
                    break;
                }
                totalButton++;
            }
            
            if(totalButton < linkNumber){
                var length = linkNumber;
                while(totalButton < length){
                    if(totalButton>pageNumber){
                        break;
                    }
                    
                    
                    if(nowPage < pageNumber/2){
                        //向右填充
                        tmpArr.push(tmpArr[tmpArr.length-1]+1);
                    }else{
                        //向左填充
                        tmpArr.unshift(tmpArr[0]-1);
                    }
                    
                    totalButton++;
                    linkNumber++;
                }
            }
            
            //创建dom对象
            ul.appendChild(firstLi);
            for(var index=0;index<linkNumber ; index++){
                
                if(tmpArr[index]<=0){
                    continue;
                }else if(tmpArr[index]>pageNumber){
                    break;
                }
                
                var li = document.createElement("li");
                //处理特殊变量
                var reg=new RegExp("{{i}}");
                tmpLinkData = linkData.replace(reg, tmpArr[index]);
                
                li = pagingComponentLiLinkBind(li, tmpArr[index], tmpLinkData);
                //处理选中
                if(tmpArr[index]==nowPage){
                    li.childNodes[0].style.backgroundColor = "#337ab7";
                    li.childNodes[0].style.color = "white";
                }else{
                    li.childNodes[0].onmouseover=function(){
                        this.style.backgroundColor = "#eee";
                    }
                    li.childNodes[0].onmouseout=function(){
                        this.style.backgroundColor = "white";
                    }
                }
                
                ul.appendChild(li);
            }
            ul.appendChild(finalyLi);
            
            return ul;
       }
    
 }
