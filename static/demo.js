//$(document).ready(function() {
    var $chatInput = $('#alme-input-field'),
        $loading = $('.loader');
var dialog = "initial"; // initial-0 is for greeting 



var hotel_image ="data:image/jpeg;base64,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";
    
function converse(val) {

	    if (val=='accept' || val=='reject')
	    {
	    	if(val=='accept'){
	    		var query="yes";
	    	}
	    	else{
	    		var query="no";
	    	}
	    	
	    }
	    else{
	    	var query = ($chatInput.val());
	    }
        
        if (query=='' || query==' ') {
            alert('give some text');
        }else if(query=="book hotel"){
            showHotel(0);
        }
        else{
            showUserQuery(query);
            scrollChatToBottom();
        $.ajax({
            url: "/getAnswer",
            method: 'GET',
            
            data: { query: query,dialog:dialog },
            success: function(data) {
                //console.log(data);
                if (data.dialog=='summary')
                {

                	showConfirm(data.id,data.response[1],data.response[2],"Transaction",data.response[3],data.response[4],data.response[5],data.response[6],data.response[7]);
                	dialog=data.dialog;
                	/*if(data.response[0].toLowerCase().indexOf("corporatelist")>=0){
                    showCorporateList(0);
                }else if(data.response[0].toLowerCase().indexOf("corporatelist")>=0){
                    showConfirm(0,"benename","currency","type","dater","amount","details","Accname","accno");
                }else{
                    showBotReply(data.response,data.id);
                }*/

                }
                else
                {

                	var $chatBox = $('#botReplyDiv').clone().prop('id',"botdiv"+data.id);
                var $loading = $('.loader');
                $chatBox.css("display", "block");
                var ul  = document.createElement('ul');
                for (i=0;i<data.response.length;i++) {
                       //code
                       //console.log(data.response[i])
		       console.log(data.dialog)
                       var li=document.createElement('li');
                       if (data.dialog=='link'){
                       	if(i==1){
                       		//alert(data.dialog);
                       		li.appendChild(document.createTextNode(data.response[i]));
                       	}
                       	else{
                       		li.appendChild(document.createTextNode(data.response[i]));
                       	}
                       	

                       }
		       else if (data.dialog=='search_payment' && (i==1 || i==2 || i==3)) {
			var b = document.createElement('button');
			b.setAttribute('content', data.response[i]);
			b.setAttribute('class', 'btn');
			b.setAttribute('id',data.response[i])
			b.innerHTML = data.response[i];	
			li.appendChild(b);
		       
		       }
		       else if (data.dialog=='search by date' && (i==1 || i==2)) {
			var b = document.createElement('button');
			b.setAttribute('content', data.response[i]);
			b.setAttribute('class', 'btn');
			b.setAttribute('id',data.response[i])
			b.innerHTML = data.response[i];	
			li.appendChild(b);
		       }
		       else if(data.dialog=='confirm_email' && i==2){
                       		//alert(data.dialog);
						var a = document.createElement("a");
							
						var linking = (data.response[i]);
							
						a.textContent = linking;
						a.setAttribute('href', "/pdf/output.pdf");
							
						li.appendChild(a);
                       	}
                       else{
                       	li.appendChild(document.createTextNode(data.response[i]));
                       }
                       
                       ul.appendChild(li);
                }   
		        $chatBox.find('p').html($('<p/>').html(ul));
		        $('#alme-chat-history').append($chatBox);
		        $chatBox.insertBefore($loading);
		                //speak(data.response);
		                if(data.dialog=='link'){
		                	dialog="initial"
		                }
		                else{
		                	dialog = data.dialog;
		                }
		                
		               /* if(data.status ==true){
		                    collectFeedback(data.id);
		                }*/

                }
                
                
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
            url: "/resolveAmbiguousQuery",
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