//////////////////////////////
// Profile Image Upload Input
//////////////////////////////
var loadFile = function (event) {
  var image = document.getElementById("output-img");
  image.src = URL.createObjectURL(event.target.files[0]);
};

// loader
$(window).on('load', function(){
  $('.cs-loader').fadeOut(1000) 
})

$(document).ready(function() {


// Sidebar JS
if (Cookies.get('toggle')  != '' ){
  $('#wrapper').addClass('toggled-2')
}
$("#menu-toggle").click(function(e) {
  e.preventDefault();
$("#wrapper").toggleClass("toggled");
});
$("#menu-toggle-2").click(function(e) {
  if(Cookies.get('toggle') != ''){
    Cookies.set('toggle', '');
  }else{
    Cookies.set('toggle', 'toggled-2');
  }  
  e.preventDefault();
  $("#wrapper").toggleClass("toggled-2");
  $('#menu ul').hide();
});
// Tooltop Init
  $(function () {
    $('[data-bs-toggle="tooltip"]').tooltip()
  })
// Menue Init
function initMenu() {
  $('#menu ul').hide();
  $('#menu ul').children('.current').parent().show();
  //$('#menu ul:first').show();
  $('#menu li a').click(
     function() {
        var checkElement = $(this).next();
        if ((checkElement.is('ul')) && (checkElement.is(':visible'))) {
           return false;
        }
        if ((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
           $('#menu ul:visible').slideUp('normal');
           checkElement.slideDown('normal');
           return false;
        }
     }
  );
}
initMenu();

});


$(document).ready(function () {
////////////////////////////
// ADD WFH PC Form Ajax Code
////////////////////////////
  // var toast = new bootstrap.Toast(liveToast)
  // $('#add_pc').on('submit', function (event) {
  //   req = $.ajax({
  //     type: 'POST',
  //     url: '/wfh-pcs',
  //     data: {
  //       editpc: $('#editpc'),
  //       pc_no: $('#pc_number').val(),
  //       pc_host: $('#pc_host').val(),
  //       pbxuser: $('#pbxuser').val(),
  //       ciscodid: $('#ciscodid').val()
  //     },
  //     beforeSend: function () {
  //       // $('.aj-spinner').fadeIn(1000)
  //     },
  //     success: function () {
  //       $('#pcs_table').fadeOut(100)
  //       $('#pcs_table').load(' #pcs_table >*', ' #req-msg >*')
  //       $('#pcs_table').fadeIn(1000)
  //       $('#add_pc')[0].reset();
  //       // $('#pc_number','#pc_host','#pbxuser','#ciscodid').val('')
  //       // $('.aj-spinner').fadeOut(1000)
  //     },
  //   })

  //   req.done(function (data) {
  //     if (data.error) {
  //       $('.toast-body').text(data.error)
  //       $('#liveToast').toast('show');
  //       $('.msg-title').text('Error!');
  //     } else {
  //       $('.toast-body').text(data.success)
  //       $('#liveToast').toast('show');
  //       $('.msg-title').text('Sucsess!');
  //     }
  //   });
  //   event.preventDefault();
  // })
//////////////////////////////
// ADD Agent To WFH PC Form Ajax Code
//////////////////////////////
  //   $('#add_wfh_pc').on('submit', function (event) {
  //     window.onbeforeunload = function() {
  //       return "Dude, are you sure you want to leave? Think of the kittens!";
  //   }
  //     token = new FormData(document.getElementById("rsa-token"))
  //     req = $.ajax({
  //       type: 'POST',
  //       url: '/wfhtracker',
  //       data: {
  //         pc_no: $('#pc_no').val(),
  //         agentbio: $('#agent-bio').val(),
  //         agent_tl: $('#agent-tl').val(),
  //         rsa : token
  //       },
  //       beforeSend: function () {
  //         // $('.aj-spinner').fadeIn(1000)
  //         $('.tb-body').fadeOut(300)
  //       },
  //       success: function () {
  //         $('.tb-body').load(' .tb-body >*').fadeIn(300)
  //         // $('#add_pc')[0].reset();
  //         // $('.aj-spinner').fadeOut(1000)
  //       },
  //     })

  //   req.done(function (data) {
  //     if (data.error) {
  //       $('.toast-body').text(data.error)
  //       $('#liveToast').toast('show');
  //       $('.msg-title').text('Error!');
  //     } else {
  //       $('.toast-body').text(data.success)
  //       $('#liveToast').toast('show');
  //       $('.msg-title').text('Sucsess!');
  //     }
  //   });
  //   event.preventDefault();
  // })

//////////////////////////////
// ADD TODOs Ajax Code
//////////////////////////////
$('#todo-form').on('submit', function (event) {
  req = $.ajax({
    type: 'POST',
    url: '/todo',
    data: {
      todo_task: $('#add-todo').val(),
    },
    beforeSend: function () {
    },
    success: function (data) {
      $('.ps-content').load(' .ps-content >*')
      $('.tasks-badg').html(data)
    },
  })

req.done(function (data) {

});
event.preventDefault();
})

// Todo Side
$('#tasks-btn').on('click', function(){
  $('.todo-side, .todo-overflow').toggleClass('todo-active')
});
$('.todo-overflow').on('click', function(){
  $('.todo-side, .todo-overflow').removeClass('todo-active')
})
//////////////////////////////
// Mark TODOs Ajax Code
//////////////////////////////
$(document).on("click",".addTaskBtn",function(){
  var taskId = $(this).data('rep');
   $.ajax({
    url: "/mark-todo",
    type: "GET",
    data: {taskId: taskId},
    success: function(data) {
      $('.ps-content').load(' .ps-content >*')
      $('.tasks-badg').html(data)
    },
   });   
});
//////////////////////////////
// Delete TODOs Ajax Code
//////////////////////////////
$(document).on("click",".delete-task",function(){
  var taskId = $(this).data('rep');
   $.ajax({
    url: "/delete-todo",
    type: "GET",
    data: {taskId: taskId},
    success: function(data) {
      $('.ps-content').load(' .ps-content >*')
      $('.tasks-badg').html(data)
    },
    
   });   
});
//////////////////////////////
// TODOs Count Ajax Code
//////////////////////////////
function getCount(){
  $.ajax({
    url: "/todo",
    type: "GET",
    data: {},
    success: function(data) {
      $('.tasks-badg').html(data)
    },
   }); 
}
getCount()


//////////////////////////////
// Import PCs From Excel Sheet Ajax Code
//////////////////////////////
$('.spinner-border').hide()
$('#add-pc-exc').on('submit', function (event) {
  $('.spinner-border').show()
});
//////////////////////////////
// Print Labels
//////////////////////////////
$(document).on("click",".print",function(){
$(".print-el").print({
  globalStyles: true,
  mediaPrint: false,
  stylesheet: null,
  noPrintSelector: ".no-print",
  iframe: true,
  append: null,
  prepend: null,
  manuallyCopyFormValues: true,
  deferred: $.Deferred(),
  timeout: 750,
  title: null,
  doctype: '<!doctype html>'
});
});
// Labels Js
$('.floor').load(' .floor >*')
$('.pro, .wfh').click(function() {
  if($('.pro').is(':checked')) {
    $('.floor').prop("disabled", false)
    } 
  else if ($('.wfh').is(':checked')){
      $('.floor').prop("disabled", true)
    }
});


//////////////////////////////
// Search Ajax Code
//////////////////////////////
// load_data()
// function load_data(search){
//   $.ajax({
//     url: "/search",
//     method: "POST",
//     data:{search:search},
//     success: function(data){
//       // $('tbody').html(data)
//       // $('tbody').append(data.headcounts)
//     }
//   })
// }
// $('#search').keyup(function () {
//   var search = $(this).val()
//   if (search != ''){
//     load_data(search)
//   }else{
//     load_data()
//   }
// })

$('#search').keyup(function(event){
  var query = $('#search').val();
  if( query != ''){
    $.ajax({
      url:"/search",
      method:"POST",
      data:{query:query},
      success:function(data)
      {
        $('tbody').html(data);
        $("tbody").append(data.headcounts);
      }
     });
  }else{
    $('tbody').load(' tbody >*')
  }
 
   event.preventDefault()
})

// load_data();
// function load_data(query)
// {
//  $.ajax({
//   url:"/search",
//   method:"POST",
//   data:{query:query},
//   success:function(data)
//   {
//     $('tbody').html(data);
//     $("tbody").append(data.headcounts);
//   }
//  });
// }
// $('#search_text').keyup(function(){
//   var search = $(this).val();
//   if(search != ''){
//   load_data(search);
//  }else{
//   load_data();
//  }
// });

  
  $('#upload-leavers').on('submit', function (event) {
      var lvexcel = new FormData($(this)[0]);
      $.ajax({
          type: 'POST',
          url: '/headcount/leavers',
          data: lvexcel,
          contentType: false,
          cache: false,
          processData: false,
          beforeSend: function (data){
            $('.spinner-border').show()
          },
          success:function(data)
          { 
            $('#upload-leavers')[0].reset();
            $('.spinner-border').hide()
            $('#success-msg').modal('show'); 
          },
      });
      
      event.preventDefault()
  });

  $('#field_service_id_6227234e33d34').on('change', function (event) {
    var cate = $(this).val();
    console.log(cate)
    $.ajax({
        type: 'POST',
        url: '/request/details',
        data: {"data":cate},
        success:function(sub_cat)
        { 
          console.log(sub_cat)
            $('#field_servicesubcategory_id_6227235100e1e').empty()
            $.each(sub_cat, function(id,item) {
            $('#field_servicesubcategory_id_6227235100e1e').append('<option value="' + id + '">' + item+'</option>');
          })
         
        },
    });
    
    event.preventDefault()
});     
 
//////////////////////////////
// Progress Ajax Code
//////////////////////////////
// function Count(){
//   $.ajax({
//     url: "/headcount/leavers",
//     type: "GET",
//     data: {},
//     success: function(data) {
//       $('.progress-bar').css('width', data + '%')
//       console.log(data)
//     },
//    }); 
// }
// Count()

$('.table').DataTable({
  "paging":   true,
  "ordering": true,
  "info":     true,
  "pagingType": "full_numbers"
});



// $.fn.editable.defaults.mode = 'inline';
// $('.hc-bio').editable();
// $('.table').editable({
//   container:'body',
//   selector:'td.bio',
//   url:'/headcount-update',
//   title:'bio',
//   type:'POST',
//   validate:function(value){
//       if($.trim(value) == '')
//       {
//           return 'This field is required';
//       }
//   }
// });
  // $('.bio').editable('save.php', {
  //   type      : 'input',
  //   cancel    : 'Cancel',
  //   submit    : 'OK',
  //   tooltip   : 'Click to edit…'
  // });


  var submitdata = {}
/* this will make the save.php script take a long time so you can see the spinner ;) */
// submitdata['slow'] = true;
$(".bio").on('click', function(){
  id = $(this).attr("data-pk")
  bio = $(this).find('input').val()
  return submitdata['bio'] = bio,  submitdata['id'] = id;
})


$(".bio").editable("/headcount", {
    type : "text",
    // only limit to three letters example
    //pattern: "[A-Za-z]{3}",
    onedit : function() { console.log('If I return false edition will be canceled'); return true;},
    before : function() { console.log('Triggered before form appears')},
    callback : function(result, settings, submitdata) {
        console.log('Triggered after submit');
        console.log('Result: ' + result);
        console.log('Settings.width: ' + settings.width);
        console.log('Submitdata: ' + submitdata.pwet);
        $(".table-wrapper").html($(result).find(".table-wrapper"))
    },
    cancel : 'Cancel',
    onblur : false,
    cssclass : 'form-control',
    cancelcssclass : 'btn btn-danger',
    submitcssclass : 'btn btn-success',
    maxlength : 200,
    style   : 'display: inline',
    // select all text
    select : true,
    onreset : function() { console.log('Triggered before reset') },
    onsubmit : function() { console.log('Triggered before submit') },
    showfn : function(elem) { elem.fadeIn('slow') },
    submit : 'Save',
    submitdata : submitdata,
    /* submitdata as a function example
    submitdata : function(revert, settings, submitdata) {
        console.log("Revert text: " + revert);
        console.log(settings);
        console.log("User submitted text: " + submitdata.value);
    },
    */
    tooltip : "Click to edit...",
});


// var socket = io.connect('http://127.0.0.1:8000');

// var socketms = io('http://127.0.0.1:8000/messages')

// $('.btn-custom').on('click', function() {
//     var message = $('.form-control').val();

//     socket_messages.emit('message from user', message);

// });

// socket_messages.on('from flask', function(msg) {
//     alert(msg);
// });

// socketms.on('connect_res', function(msg) {
//     $('.user-' + msg).addClass('bg-success')
// });

// var private_socket = io('http://127.0.0.1:8000/private')

// $('.btn-custom').on('click', function() {
//     private_socket.emit('username', 9);
// });

// $('.btn-custom').on('click', function() {
//     var recipient = 9;
//     var message_to_send = $('.form-control').val();

//     private_socket.emit('private_message', {'username' : recipient, 'message' : message_to_send});
// });

// private_socket.on('new_private_message', function(msg) {
//     alert(msg);
// });

/*

socket.on('connect', function() {

    socket.send('I am now connected!');

    socket.emit('custom event', {'name' : 'Anthony'});

    socket.on('from flask', function(msg) {
        alert(msg['extension']);
    });

    socket.on('message', function(msg) {
        alert(msg);
    });
    
});

*/
  // var namespace = '/notifs';

  // var socket = io.connect(location.protocol + "//" + location.host + namespace, {reconnection: false});

  // socket.on('response', function(msg) {
  //     console.log(msg.meta);
  //     // If `msg` is a notification, display it to the user.
  // });


// Add New Item

$('#add-item-btn').click(function(e) {
  var category_value = $("#order-item-category").val();
  var item_name_value = $("#order-item-name").val();		
  var serial_value = $('#order-item-serial').val();
  var quantity_value = $('#order-item-quantity').val();
  $('.dataTables_empty').hide()
  $('#order_items_table tbody').append(
    '<tr>' + '<td>' + $("#order-item-category option:selected").text() +'<input name="item-category" type ="hidden" value="' + category_value  + '">' + '</td>\
  <td>' + '<input name="item-name" value="' + item_name_value + '">' + '</td>\
  <td>' + '<input name="item-serial" value="' + serial_value + '">' + '</td>\
  <td>' + '<input name="item-quantity" value="' + quantity_value + '">' + '</td>\
                            </tr>' + '</tr>');

});

$('#date').val(new Date())



// Orders Table add abd remove Rows function

}); // End Document 
//###############################
//###############################


// Add inputs to form
$('input[name="select-wfh"]').click(function(){
  //console.log(this.value)
  var list = []
  $('input[name="select-wfh"]:checked').each(function(){
    // console.log(this.value)
    list.push(this.value)   
  });
  console.log(list)
  $('#selected-wfh-items').val(list)

})

