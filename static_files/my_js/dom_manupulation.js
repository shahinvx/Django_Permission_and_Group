let my_item = document.getElementsByClassName('dropdown-item');
console.log(`inner Context : ${my_item.textContent}`)
console.log(`inner Context : ${my_item}`)

function myFunction() {
    console.log(document.getElementsByClassName('dropdown-item'));
}

function toggleOn() {
    //$('#toggle-trigger').bootstrapToggle('on')
    //console.log($(this).prop('checked'))
    console.log(document.getElementById("chk_tgl").checked)

    document.getElementById("btn_tgl").disabled = document.getElementById("chk_tgl").checked;
}

function show_data_2(event) {
    var data = event.closest("tr");
    console.log('Clicked fun', data, data.textContent, data.innerText);

    //console.log('Data -> ', data.querySelector("td"));
    for (var i = 0; i < data.length; i++) {
        console.log(data[i])
    }
};

$('btn_edit').click(function () {
    console.log('Clicked')
    var $item = $(this).closest("tr")   // Finds the closest row <tr> 
        .find(".nr")     // Gets a descendent with class="nr"
        .text();         // Retrieves the text within <td>

    $("#resultas").append($item);       // Outputs the answer
});