//$(document).ready(function() {
    var $chatInput = $('#alme-input-field'),
        $loading = $('.loader');
var dialog = "initial"; // initial-0 is for greeting 

 function converse(val) {

	    
	    	var query = ($chatInput.val());
	    
        
        if (query=='' || query==' ') {
            alert('give some text');
        }
        else{
            showUserQuery(query);
            scrollChatToBottom();
        $.ajax({
            url: "http://127.0.0.1:8000/getAnswer",
            method: 'GET',
            
            data: { query: query,dialog:dialog },
            success: function(data) {
                //console.log(data);
                var $chatBox = $('#botReplyDiv').clone().prop('id',"botdiv"+data.id);
                var $loading = $('.loader');
                $chatBox.css("display", "block");
                var ul  = document.createElement('ul');
                       console.log(data.response)
                       var li=document.createElement('li');
                       	li.appendChild(document.createTextNode(data.response));
                       
                       ul.appendChild(li);
		        $chatBox.find('p').html($('<p/>').html(ul));
		        $('#alme-chat-history').append($chatBox);
                      $chatBox.insertBefore($loading);
		                //speak(data.response);
		                if(data.dialog=='link'){
		                	dialog="initial"
		                }
		                else if (data.dialog=='pdf') {
		                	dialog="initial"
		                }
		                else{
		                	dialog = data.dialog;
		                }
		                
		               /* if(data.status ==true){
		                    collectFeedback(data.id);
		                }*/
                $( "#Most Recent" ).click(function() {
                    converse('Most Recent');
	            });
                $( "#Largest" ).click(function() {
                    converse('Largest');
	            });
                $( "#DirectSearch" ).click(function() {
                    converse('Direct Search');
	            });
                $( "#ByValueDate" ).click(function() {
                    converse('By Value Date');
	            });
                $( "#InputData" ).click(function() {
                    converse('Input Data');
	            });
		  

               // }
                
                
            }
        });
        scrollChatToBottom();
        
        $chatInput.val("");
        return true;
    }
    }

function showHotel(id){  

        var $hotelDiv = "<img src='"+hotel_image+"'><h3 class='text-center'>Hotel Bedrock</h3><h4 class='text-center'>30% Discount</h4><p class='text-center'>2 Hours and 25 minutes remaining for the offer</p>";
        $hotelDiv+="<p style='background-color:whit;padding-top:3px;padding-bottom:3px;'><span style='margin-right:10px' class='glyphicon glyphicon-star' aria-hidden='true'></span><span>3.5</span></p>";
        $hotelDiv+="<p style='background-color:whit;padding-top:3px;padding-bottom:3px;'><span style='margin-right:10px' class='glyphicon glyphicon-bell' aria-hidden='true'></span><span>3 tables remaining</span></p>";
        var $chatBox = $('#botReplyDiv').clone().prop('id',"botdiv"+id);
        var $loading = $('.loader');
        $chatBox.css("display", "block");
        $chatBox.find('p').html($('<p/>').append($hotelDiv));
        $('#alme-chat-history').append($chatBox);
        $chatBox.insertBefore($loading);
        scrollChatToBottom();
}
//showHotel(0);
function showConfirm(id,benename,currency,type,dater,amount,details,Accname,accno){
        var $confirmDiv = "<div class='table-responsive'><table style='width: 100%;' class='table-hover '><tr><td>Beneficiary</td><td>"+benename+"</td></tr>"+
                                "<tr><td>Currency</td><td>"+currency+"</td></tr>"+
                                "<tr><td>Type</td><td>"+type+"</td></tr>"+
                                "<tr><td>Date</td><td>"+dater+"</td></tr>"+
                                "<tr><td>Amount</td><td>"+amount+"</td></tr>"+
                                "<tr><td>Details</td><td>"+details+"</td></tr>"+
                                "<tr><td>Account name</td><td>"+Accname+"</td></tr>"+
                                "<tr><td>Account number</td><td>"+accno+"</td></tr></table></div>";
        $confirmDiv+='<div class="btn-group " role="group" aria-label="..."><button type="button" id="accept" class="btn btn-default">Accept</button> <button type="button" id="reject" class="btn btn-default">Reject</button></div>';
        var $chatBox = $('#botReplyDiv').clone().prop('id',"botdiv"+id);
        var $loading = $('.loader');
        $chatBox.css("display", "block");
        $chatBox.find('p').html($('<p/>').append($confirmDiv));
        $('#alme-chat-history').append($chatBox);
        $chatBox.insertBefore($loading);
        scrollChatToBottom();
        $( "#accept" ).click(function() {
  converse('accept');
	});

        $( "#reject" ).click(function() {
  converse('reject');
	});
}
//showConfirm(0,"benename","currency","type","dater","amount","details","Accname","accno");

function showCorporateList(id){  

        var $corporateDiv = "<div class='table-responsive'><table class='corporate_table' style='width: 100%;' class=''>"+
                                "<tr><td><span style='margin-right:10px' class='glyphicon glyphicon-plus' aria-hidden='true'></span>benename</td><td><span style='margin-right:10px' class='glyphicon glyphicon-usd' aria-hidden='true'></span>currency</td></tr>"+
                                "<tr><td><span style='margin-right:10px' class='glyphicon glyphicon-th-large' aria-hidden='true'></span>type</td><td><span style='margin-right:10px' class='glyphicon glyphicon-calendar' aria-hidden='true'></span>dater</td></tr>"+
                                "<tr><td><span style='margin-right:10px' class='glyphicon glyphicon-piggy-bank' aria-hidden='true'></span>amount</td><td><span style='margin-right:10px' class='glyphicon glyphicon-file' aria-hidden='true'></span>details</td></tr>"+
                                "<tr><td><span style='margin-right:10px' class='glyphicon glyphicon-font' aria-hidden='true'></span>Accname</td><td><span style='margin-right:10px' class='glyphicon glyphicon-credit-card' aria-hidden='true'></span>Accno</td></tr>"+                               
                                "</table></div><style>.corporate_table td{padding:3px}</style>";
        
        var $chatBox = $('#botReplyDiv').clone().prop('id',"botdiv"+id);
        var $loading = $('.loader');
        $chatBox.css("display", "block");
        $chatBox.find('p').html($('<p/>').append($corporateDiv));
        $('#alme-chat-history').append($chatBox);
        $chatBox.insertBefore($loading);
        scrollChatToBottom();
}
//showCorporateList(0);

function showUserQuery(query){
        var $chatBox = $('#userInputDiv').clone();
        var $loading = $('.loader');
        $chatBox.css("display", "block");
        $chatBox.find('p').html($('<p/>').html(query).text());
        $('#alme-chat-history').append($chatBox);
        $chatBox.insertBefore($loading);
        
}

function showBotReply(reply,id){
    var $chatBox = $('#botReplyDiv').clone().prop('id',"botdiv"+id);;
        var $loading = $('.loader');
        $chatBox.css("display", "block");
        for (i=0;i<reply.length;i++) {
            //code
            $chatBox.find('p').html($('<p/>').append(reply[i]));
        }
        //$chatBox.find('p').html($('<p/>').html(reply));
        
        $('#alme-chat-history').append($chatBox);
        $chatBox.insertBefore($loading);
        
}

function scrollChatToBottom(){
      
    var element = $('#alme-chat-history');
    element.animate({scrollTop: element[0].scrollHeight}, 800);
 
}

function resolveAmbiguousQuery(id,selection ){
    $.ajax({
            url: "http://127.0.0.1:8000/resolveAmbiguousQuery",
            method: 'GET',
            
            data: { id: id,selection:selection },
            success: function(data) {
                //if(data.response=="done")
                //$("#div"+id).hide("slow");
            }
        });
    
    $chatInput.val(selection );
    converse('');
}
$("#alme-input-form").submit(function(event) {
        converse();

        event.preventDefault();
    });
    
    function speak(text){
        var msg = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(msg);
    }  