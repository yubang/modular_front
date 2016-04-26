var change_func;
function component_init(data, func){

//document.getElementById('ccc').onclick=cli;
console.log(data)
//测试
change_func = func;
    //document.getElementById('ccc').innerHTML = 'vvv11111';
}

this.show_func = function(){
    change_func({"test": '测试'})
}

function cli(){alert(123);}

this.component_init = component_init