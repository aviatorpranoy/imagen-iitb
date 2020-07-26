$(function (){
    var jArr = [];  //list of json elements
    var hArr = [];  //list of html elements
    var obj = $.getJSON("site/element-info.json", function(){
        
    //Get the list of elemental systems in element-info.json
    for(var i in obj.responseJSON.elementSystems){
        jArr.push(obj.responseJSON.elementSystems[i]);
    }
    //get all div symbol classes
    var x = document.getElementsByClassName("symbol"); 
    for(i = 0; i < x.length; i++){
        //make a list of all elements in elements.html
        hArr.push(x[i].getAttribute('id')); 
    }
    //loop through all elements in elements.html
    for(a = 0; a < hArr.length; a++){
        //loop through all elements in element-sets.json
        for(b = 0; b < jArr.length; b++){
            if( hArr[a] == jArr[b]){
                var sym = document.getElementById(jArr[b]);
                //add onclick attribute to div
                var att = document.createAttribute("onClick");
                //set the attribute to call elementClick and pass in the div id
                att.value = "elementClick(id)";
                sym.setAttributeNode(att);//set the attribute
                //change styling
                var style = document.createAttribute("style");
                style.value = "font-weight:bold; cursor:pointer; text-decoration: underline;";
                sym.setAttributeNode(style);
            }
        }
    }
    })
})

function elementClick(element){
    var url = "system/" + element; //set url to system/divid
    window.open(url, "_self");
   
}