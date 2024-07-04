$.noConflict();

var kabe_circle_list = ['A', 'a', 'あ', 'ス']

// boundaries to be cropped on pdf
const x1 = 750
const y1 = 1168
const x2 = 4045
const y2 = 2418

// Find width of container
const tableContainer = $('.table-container');
const tableWidth = tableContainer.width();

// let canvas = $("#map");
// let ctx = canvas.get(0).getContext("2d"); 

// let canvas_plot = $("#plots");
// let ctx_plot = canvas_plot.get(0).getContext("2d"); 

let canvas = document.getElementById("map");
let ctx = canvas.getContext("2d"); 

let canvas_plot = document.getElementById("plots");
let ctx_plot = canvas_plot.getContext("2d"); 


$(document).ready(function(){
    $('#showAllBtn').click();

    const image = new Image();
    image.src = "cropped_rotated.png";
    image.onload = () =>
        {
 
            // canvas.width = tableWidth
            // canvas.height = image.width*tableWidth/image.height;

            canvas.width = tableWidth
            canvas.height = tableWidth/image.width*image.height;

            ctx.drawImage(image, 0, 0, canvas.width, canvas.height);


            // ctx.save();

            // // Translate the context so that the rotation occurs around the center of the canvas
            // ctx.translate(canvas.width / 2, canvas.height / 2);
    
            // // Rotate the context by 90 degrees
            // ctx.rotate(Math.PI / 2);
            
            // // Draw the image onto the canvas
            // ctx.drawImage(image, -canvas.width / 2, -canvas.height / 2, canvas.width, canvas.height);

            // // temp = canvas.width
            // // canvas.width = canvas.height
            // // canvas.height = temp
            // // Restore the original state of the canvas context
            // ctx.restore();


            // Draw the image onto the canvas
            // ctx.drawImage(image, 0, 0, canvas.width, canvas.height)
    
            // Restore the original state of the canvas context
            // ctx.restore();

            canvas_plot.width = canvas.width
            canvas_plot.height = canvas.height

            // ctx_plot.clearRect(0, 0, canvas_plot.width, canvas_plot.height);
            // ctx_plot.beginPath();
            // ctx_plot.arc(10, 50, 5, 0, 2 * Math.PI, false);
            // ctx_plot.fillStyle = '#ff0000';
            // ctx_plot.fill();

        }

    

});


$('#plotBtn').on('click', function(e) {

    e.preventDefault();

    if ($('#myTable').is(':visible'))
    {

        $('#myTable').hide();
        $('#map_div').show();

        // ctx_plot.clearRect(0, 0, canvas_plot.width, canvas_plot.height);
        // ctx_plot.beginPath();
        // ctx_plot.arc(116.00242792109256, 350.967584, 5, 0, 2 * Math.PI, false);
        // ctx_plot.arc(106.24097116843703, 350.967584, 5, 0, 2 * Math.PI, false);
        // ctx_plot.fillStyle = '#ff0000';
        // ctx_plot.fill();


    }

    else
    {
        $('#myTable').show();
        $('#map_div').hide();
    }

});


var IPVAR = "https://fkiemis3-5vu7fnptaq-an.a.run.app"

function presentTable(data) {
	
	// Split the CSV data into rows
	let rows = data.split("\n");
	let table = document.getElementById("myTable");

	// Remove contents in table
	$("#myTable tr:gt(0)").remove();
		
	// Create a new row for each item in the rows
	
	rows.shift()  // Remove first row in csv received
	
	for (let row of rows) {
		let tableRow = document.createElement("tr");

		// Split the row into columns
		let columns = row.split(",");

		// Create a new cell for each item in the columns
		for (let column of columns) {
			let tableCell = document.createElement("td");
			tableCell.textContent = column;
			tableRow.appendChild(tableCell);
		}

		table.appendChild(tableRow);
	}
}


function checkbox_convert() {

    // Find the index of the "購入済み" column
    var boughtColumnIndex = -1;
    $('#myTable th').each(function(i, header) {
        if ($(this).text().trim() === '購入済み') {
            boughtColumnIndex = i;
            return false; // Break the loop once found
        }
    });

    // Change "購入済み" column into checkboxes
    $('#myTable tr').each(function(i, row) {
        if (i > 0) { 
            var cell = $(row).find('td:eq(' + boughtColumnIndex + ')');
            var cellValue = cell.text();
            var checkbox = $('<input type="checkbox">');
         
            if (cellValue === '1') {
              checkbox.prop('checked', true);
            }

            cell.html(checkbox);
        }
    });
};

function drawArrow(x_curr, y_curr, x_next, y_next, radius){

    let fromx = canvas.width/(y2 - y1) * (y2 - y_curr)
    let fromy = canvas.height / (x2 - x1) * (x_curr - x1)

    let tox = canvas.width/(y2 - y1) * (y2 - y_next)
    let toy = canvas.height / (x2 - x1) * (x_next - x1)

    var headlen = 5; // length of head in pixels
    var dx = tox - fromx;
    var dy = toy - fromy;

    if (0 < Math.abs(dx) & Math.abs(dx) < radius*2 | 0 < Math.abs(dy) & Math.abs(dy) < radius*2){
        console.log("run")
        return
    }

    if (dx == 0){

        if (dy < 0){
        fromy -= radius
        toy += radius
        dy = toy - fromy}

        else {
            fromy += radius
            toy -= radius
            dy = toy - fromy
        }
    }
    else if (dy == 0){

        if (dx < 0){
            fromx -= radius
            tox += radius
            dx = tox - fromx
        }

        else {
            fromx += radius
            tox -= radius
            dx = tox - fromx
        }
    }

    var angle = Math.atan2(dy, dx);

    ctx_plot.lineWidth = 2;
    ctx_plot.strokeStyle = '#78C3ED';

    ctx_plot.beginPath();
    ctx_plot.moveTo(fromx, fromy);
    ctx_plot.lineTo(tox, toy);
    ctx_plot.stroke();

    ctx_plot.lineWidth = 3;

    ctx_plot.beginPath();
    ctx_plot.moveTo(tox, toy);
    ctx_plot.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),toy-headlen*Math.sin(angle-Math.PI/7));
    
    //path from the side point of the arrow, to the other side point
    ctx_plot.lineTo(tox-headlen*Math.cos(angle+Math.PI/7),toy-headlen*Math.sin(angle+Math.PI/7));
    
    //path from the side point back to the tip of the arrow, and then again to the opposite side point
    ctx_plot.lineTo(tox, toy);
    ctx_plot.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),toy-headlen*Math.sin(angle-Math.PI/7));

    ctx_plot.strokeStyle = "#78C3ED";
    ctx_plot.stroke();

}


// Toggle menu

$('.fab-button').click(function() {
    $('#menu').toggle();
});


// Show all circles
$('#showAllBtn').on('click', function(e) {

    e.preventDefault();

    fetch("http://127.0.0.1:8000/return_whole_csv",{
        method:"GET",
        // body:formData,
    })
    .then(response => response.text())
    .then(data => 
	{
		console.log(data);
		$('#myTable').html(data.slice(1, -1));
        checkbox_convert();
        // check_kabe();
	
	});

    if ($('#myTable').is(':hidden'))
        {
            $('#myTable').show();
            $('#map_div').hide();
        }

    // // Get the number of rows in the table
    // // var rowCount = $table.find('tr').length;
    
    // // Loop through each row
    // $table.find('tr').each(function(index)
    // {
    //     // Insert a new cell at the beginning of the row
    //     $(this).append('<td>New Cell</td>');
    // });  

    // $('#myTable tbody').find('tr').each(function(){
    //     console.log("asdf")
    //     $(this).append('<td></td>');
    // });

    // $('#myTable tbody').each(function(){
    //     // var trow = $(this);
    //     $(this).insertCell(4);
    //     console.log($(this));
    //     console.log("asdf");
    //     // $(this).append('<td>asdf</td>');

    // });

    // console.log($('#myTable').textContent)



});


// Show all circles
$('#resetBtn').on('click', function(e) {

    e.preventDefault();

    // add row UI
	$("#resetDialog").dialog(
        {
            autoOpen: false,
            
            buttons: [
                {
                    text: "Submit",
                    id: "resetSubmitBtn",
                    click: function() {}
                },
                {
                    text: "Cancel",
                    id: "dialogCancelBtn",
                    click: function() {	
                    $(this).dialog("close");
                    }
                },
                
                ]
        });

    $("#resetDialog").dialog('open');
    $('#menu').toggle();	

    $("#resetSubmitBtn").click(function(e) {

        fetch("http://127.0.0.1:8000/reset_csv",{
            method:"GET",
            // body:formData,
        }).then(response => response.text())
        .then(data => 
        {
            $('#myTable').html(data.slice(1, -1));
            checkbox_convert();
            // check_kabe();
        
        });

        if ($('#myTable').is(':hidden'))
            {
                $('#myTable').show();
                $('#map_div').hide();
            }

        $("#resetDialog").dialog("close")

    })


});



// Filter option
$(function () {

    // add row UI
	$("#filterDialog").dialog(
	{
		autoOpen: false,
		
		buttons: [
            {
                text: "Reset",
                id: "filterResetBtn",
                click: function() {}
            },
			{
                text: "Submit",
                id: "filterSubmitBtn",
                click: function() {}
			},
			{
                text: "Cancel",
                id: "dialogCancelBtn",
                click: function() {	
                $(this).dialog("close");
                }
			},
			
			]
	});

    // When filter button is clicked, open dialog to input information
	$("#filterBtn").click(function(e)
	{
		e.preventDefault();
		$("#filterDialog").dialog('open');
        $('#menu').toggle();		
	});


    // When filter reset button is clicked, check all the checkboxes
    $('#filterResetBtn').click(function() {
        var checkboxes = $("#filterDialog").find(':checkbox');
        checkboxes.prop('checked', true);
        });

	// When dialog submit button is clicked
	
	$("#filterSubmitBtn").click(function(e) {
		
		e.preventDefault();

        // Save the input into variables

        // var checkedDayList = $('input[name="filterDayOption"][type="checkbox"]:checked').map(function() {
        //     return $(this).val();
        //    }).get();
        
        // var checkedHallList = $('input[name="filterHallOption"][type="checkbox"]:checked').map(function() {
        // return $(this).val();
        // }).get();

        var checkedBoughtList = $('input[name="filterBoughtOption"][type="radio"]:checked').map(function() {
            return $(this).val();
           }).get();
           
       $("#filterDialog").dialog("close")

       let formData = new FormData();
    //    formData.append("checkedDayList", checkedDayList.join(','))
    //    formData.append("checkedHallList", checkedHallList.join(','))
       formData.append("checkedBoughtList", checkedBoughtList.join(','))

       fetch("http://127.0.0.1:8000/filter_table/",{
           method:"POST",
           body:formData,
       })
       .then(response => response.json())
       .then(data => 
        {
            console.log(data.df)
            $('#myTable').html(data.df.slice(1, -1));
            checkbox_convert()
            console.log(data.print)
    
        });
    

        
	});
});





 
// Add row function
$(function () {

    // add row UI
	$("#addCircleDialog").dialog(
	{
		autoOpen: false,
		
		buttons: [
			{
			  text: "Submit",
			  id: "addCircleSubmitBtn",
			  click: function() {}
			},
			{
			  text: "Cancel",
			  id: "dialogCancelBtn",
			  click: function() {	
				$(this).dialog("close");
			  }
			},
			
			]
	});

    // When add circle button is clicked, open dialog to input information
	$("#addCircleBtn").click(function(e)
	{
		e.preventDefault();
		$("#addCircleDialog").dialog('open');
        $('#menu').toggle();		
	});
	
	// When dialog submit button is clicked
	
	$("#addCircleSubmitBtn").click(function(e) {
		
		e.preventDefault();

        // Save the input into variables
        var newCircle = $('#newCircle').val();	
        var newRow = $("#newRow").val();
        var newBooth = $("#newNumber").val();

        // if invalid input (no day, no circle name, no row name) is found
        if (newCircle.length == 0 | newRow.length == 0 | newRow.length > 1 | newBooth.length == 0) {
            alert("Missing/invalid input.");

        }

        else

        {
            $("#addCircleDialog").dialog("close")

            // Clear the inputs on the dialog
            $("#newCircle").val("")
            $("#newRow").val("")
            $("#newNumber").val("")

            input = newCircle + "\n" + newRow+ "\n" + newBooth
            console.log(input)

            fetch("http://127.0.0.1:8000/add_circle/",{
                method:"POST",
                headers:
                {
                    'Content-Type': 'text/plain',
                },
                body:　input,
            })

            $('#showAllBtn').click();

            ;
        }
	});
});

// If any checkbox is clicked
$('#myTable').on('click', 'input[type="checkbox"]', function() {
    var checkbox = $(this);
    var row = checkbox.closest('tr');
    var cell = row.find('td:eq(0)'); // find first cell in row
    var cellValue = cell.text();
  
    fetch("http://127.0.0.1:8000/change_bought_status/",{
        method:"POST",
        headers:
        {
            'Content-Type': 'text/plain',
        },
        body: cellValue,
    })
});


// Show closest circle

$(function () {
    // Dialog UI
	$("#dialog").dialog(
	{
		autoOpen: false,
		
		buttons: [
			{
			  text: "Submit",
			  id: "dialogSubmitBtn",
			  click: function() {}
			},
			{
			  text: "Cancel",
			  id: "dialogCancelBtn",
			  click: function() {	
				$(this).dialog("close");
			  }
			},
			
			]
	});


    // When closest button is clicked
	$("#closestBtn").click(function(e)
	{
		e.preventDefault();
		$("#dialog").dialog('open');
        $('#menu').toggle();		
	});
	
	// When dialog submit button is clicked
	
	$("#dialogSubmitBtn").click(function(e) {
		
		e.preventDefault();

        // Save the input into variables
        var dialogRow = $("#dialogRow").val();
        var dialogBooth = $("#dialogBooth").val();

        // if no day is selected
        if (dialogRow.length == 0 | dialogRow.length > 1 | dialogBooth.length == 0) {
            alert("Missing/invalid input.");
        }

        else

        {
            $("#dialog").dialog("close")

            // Save the input into variables
            var dialogRow = $("#dialogRow").val();
            var dialogBooth = $("#dialogBooth").val();
            
            // Clear the inputs on the dialog
            $("#dialogRow").val("");
            $("#dialogBooth").val("");

            input = dialogRow + "\n" + dialogBooth
            console.log(input)

            fetch("http://127.0.0.1:8000/closest_circle/",{
                method:"POST",
                headers:
                {
                    'Content-Type': 'text/plain',
                },
                body:　input,
            })
            .then(response => response.json())
            .then(data => 
            {

                $("#myTable").html(data.df.slice(1, -1));
                checkbox_convert()
                $("#map").attr('src','data:image/png;base64,' + data.map)

                var node_list = data.node_list.flat()
                var circle_list = data.circle_points

                console.log(circle_list)
                ctx_plot.clearRect(0, 0, canvas_plot.width, canvas_plot.height);

                radius = 3

                // plot node points
                for (let i = 0; i < node_list.length; i++){

                    x0 = node_list[i][0]
                    y0 = node_list[i][1]

                    let x = canvas.width/(y2 - y1) * (y2-y0)
                    let y = canvas.height / (x2 - x1) * (x0 - x1)

                    ctx_plot.beginPath();
                    ctx_plot.arc(x, y, radius, 0, 2 * Math.PI, false);

                    if  (i == 0 | i == node_list.length -1){
                        ctx_plot.fillStyle = '#6a329f';
                    }
                    else
                    {
                        ctx_plot.fillStyle = '#ff0000';
                    }
                    
                    ctx_plot.fill();

                }

                // Plot circle points
                for (let i = 0; i < circle_list.length; i++){

                    x0 = circle_list[i][0]
                    y0 = circle_list[i][1]

                    let x = canvas.width/(y2 - y1) * (y2-y0)
                    let y = canvas.height / (x2 - x1) * (x0 - x1)

                    ctx_plot.beginPath();
                    ctx_plot.arc(x, y, radius, 0, 2 * Math.PI, false);
                    ctx_plot.strokeStyle = "#ff0000";
                    ctx_plot.stroke();

                    ctx_plot.fillStyle = '#3e8a3e';
                    ctx_plot.fill();

                }

                


                // Plot arrows

                for (let i = 0; i < node_list.length - 1; i++){

                    x_curr = node_list[i][0]
                    y_curr = node_list[i][1]

                    x_next = node_list[i+1][0]
                    y_next = node_list[i+1][1]

                    if (x_curr != x_next | y_curr != y_next){
                        drawArrow(x_curr, y_curr, x_next, y_next, radius)
                    }

                }
                


            });
        }
	});
});



// Setting dialog
$(function() {
    $("#settingDialog").dialog({
        autoOpen: false,
        width: 400,
        height: 300,
        title: '',

        buttons: [
            {
                text: "Amend Texts",
                id: "amendTxtBtn",
                click: function() {}
            },
        ],
        open: function(event, ui) {
            $(this).parent().find('.ui-dialog-titlebar').prepend('<button id="prevTab">◄</button><button id="nextTab">►</button>');
        }       
    });
    $("#settingBtn").click(function(e) {
        e.preventDefault();
        $("#settingDialog").dialog("open");
        $('#menu').toggle();
    });
    var currentTab = 0;
    $("#prevTab").click(function() {
        console.log(currentTab)
        $(".settingtab").eq(currentTab).addClass("hidden");
        currentTab = (currentTab - 1 + 2) % 2;
        $(".settingtab").eq(currentTab).removeClass("hidden");
    });
    $("#nextTab").click(function() {
        console.log(currentTab)
        $(".settingtab").eq(currentTab).addClass("hidden");
        currentTab = (currentTab + 1) % 2;
        $(".settingtab").eq(currentTab).removeClass("hidden");
    });
});


// function check_kabe(){
    
//     $('#myTable tr').each(function(i, row) {
//         if (i > 0){
//             var cellValue = $(row).find('td:eq(2)').text();
            
//             console.log(cellValue);
//             if (kabe_circle_list.includes(cellValue)) {
//                 $(this).addClass('underline-row');
//             }
//         }
//     });
// };