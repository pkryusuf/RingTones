// find selected checkboxes



var values = [];
var checkboxes_input = document.querySelectorAll('input[type=checkbox]');
var checkboxes_text = document.querySelectorAll('.custom-control-label');
var search = document.getElementById('search');
var inputMin = document.getElementById('inputMin');
var inputMax = document.getElementById('inputMax');

function alertFunct() {
    alert("Ringtone added to cart");
}




search.addEventListener('keyup', (event) => {
    var search_value = event.target.value;
    console.log(search_value);
    var new_ringtones = [];
    for (var i = 0; i < ringtones.length; i++) {
        if (ringtones[i].Ringtone_name.toLowerCase().includes(search_value.toLowerCase())) {
            new_ringtones.push(ringtones[i]);
        }
    }
    display_cards(new_ringtones);
    console.log(new_ringtones);


});




// match the checkboxes with the labels
checkboxes_input.forEach((checkbox, index) => {
    checkbox.text = checkboxes_text[index].innerText;
    console.log(checkbox.text);
});

// add event listener to the checkboxes
checkboxes_input.forEach((checkbox,index) => {
    checkbox.addEventListener('change', (event) => {
        values = [];
        if (checkbox.checked) {
            checkboxes_input.forEach((checkbox, index) => {
                if (checkbox.checked) {
                    values.push(checkbox.text);
                }
                
   
            });
        }
       
        fiter_ringtones(ringtones,values);
    });
    fiter_ringtones(ringtones,values);

});

// get a div with id="alllist"

// change the innerHTML of the div

function fiter_ringtones( ringtones,values) {
     // get the values of the selected checkboxes
     console.log(ringtones);   
     console.log(values);
     if (values.length != 0) {
     new_ringtones = [];
     for (var i = 0; i < ringtones.length; i++) {
         for (var j = 0; j < values.length; j++) {
             
             if (ringtones[i].Category_name == values[j]) {
                 new_ringtones.push(ringtones[i]);
                 console.log(ringtones[i].Category_name + " -- " + values[j]);
                 
             }

         }
         console.log(new_ringtones);
         display_cards(new_ringtones);
     };
     }
     else {
         display_cards(ringtones);
     }





};

console.log(ringtones);

// list alllist items in allList div with 3 columns by changing the innerHTML


function display_cards( ringtones_f) {
    var temp = `<div class="row mt-3">`;
    var col = 0;
for (var index = 0; index < ringtones_f.length; index = index+1) {
    console.log("index"+index);
    console.log("length"+ringtones_f.length);
    if (col == 3){
        temp +=`<div class="row mt-3">`;
        
    }
    

    temp += `<div class="col-sm-4"> 
    <div class="card" style="width: 19rem;">
        <img src=${ringtones_f[index].Ringtone_image} class="card-img-top" alt="...">
        <div class="m-auto">
                <audio controls>
                
                <source src=${ringtones_f[index].Ringtone_path} type="audio/mpeg">
                Your browser does not support the audio element.
                </audio>
            </div>
        <div class="card-body">
            <h5 class="card-title">${ringtones_f[index].Ringtone_name}</h5>
            <p class="card-text">Download by Clicking the three dot</p>
            <p class="card-text"> ${ringtones_f[index].Ringtone_description}</p>

        </div>
    </div>
    </div>`

 
    col += 1;






   


    }
    

var alllist = document.getElementById('alllist');
alllist.innerHTML = temp;

}
if (alerts_var[0] == true) {
    alert("Ringtone added to cart");
}
display_cards(ringtones);
console.log("************************");
console.log(alerts_var);




