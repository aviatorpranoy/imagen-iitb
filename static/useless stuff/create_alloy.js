$(function(){
    var jArr = []; //list of json elements
    var obj = $.getJSON("site/element-info.json", function(){
        
        for(var i in obj.responseJSON.otherSystems){
            jArr.push(obj.responseJSON.otherSystems[i]);
        }

        //var jIterator = jSet.values();
        var div = document.getElementsByClassName("elem-group");
        console.log(div);
        var table = document.createElement("table");
        div[0].appendChild(table);
        //table.style.width = "100%";
       
        for(i = 0; i < jArr.length; i++){
            //console.log(i%5);
            if(i % 5 == 0){
                var tr = table.insertRow();
            }
            var td = tr.insertCell();
            
            //td.innerHTML = jIterator.next().value;
           td.innerHTML = jArr[i];
           td.id = jArr[i];
           var sym = document.getElementById(jArr[i]);
           var att = document.createAttribute("onClick");
           att.value = "elementClick(id)";
           sym.setAttributeNode(att);
           var style = document.createAttribute("style");
           style.value = "cursor:pointer; color:#337AB7;";
           sym.setAttributeNode(style);
        }
    })
})