function swalDelete(currentCIN){
    swal({
        title:"Are you sur ?",
        text:'It will be deleted permanently !',
        type:'warning',
        showCancelButton:true,
        confirmButtonColor:'#3085d6',
        cancelButtonColor:'#d33',
        showLoaderOnConfirm:true,
        preConfirm:function(){
            return new Promise(function(resolve){
                $.ajax({
                    url:'index_agent_edit_leave',
                    type:'POST',
                    data:currentCIN,
                    dataType:'json'
                })
                .done(function(response){
                    swal('Deleted !',response.message,response.status);
                })
                .fail(function(){
                    swal('Oops !',
                    'Something went wrong with ajax !.',
                    'error');
                });
            });
        },
        allowOutsideClick:false
    });
}
function swalEdit(currentCIN){
    $.ajax({
        url:'index_agent_edit_leave',
        type:'POST',
        data:currentCIN,
        dataType:'json'
    })
}

//     Verifier le formuliare de update user profile
function swalCheck($username,$nom,$prenom,$email){
    var usernameRegex = '/^[a-z0-9_-]{3,16}$/'; 
    var emailRegex = '^[A-Z0-9._%+-]+@[A-Z0-9.-]+.[A-Z]{2,4}$';

}

$(document).ready(function() {
        //script main pagespeed
        var navbaraffichee=true;
        $('.menu-header img').click(function(event) {
            /* Act on the event */
            if (navbaraffichee) {
                $('#navbar').fadeOut(100,'linear');
                $('#content-page').css("grid-column","1/3");
                navbaraffichee=false;
            }
            else{
                $('#navbar').fadeIn(900,'linear');
                $('#content-page').css("grid-column","2/3");
                navbaraffichee=true;
            }
        });
        //Connexion style
        $('.logou-button').hover(function(){
            $('.user-existe').css('color','red');
            $('.user-existe').css('background','red');
        });
        $('.logou-button').mouseleave(function(event) {
            /* Act on the event */
            $('.user-existe').css('color','lightgreen');
            $('.user-existe').css('background','lightgreen');
        });
        //--------------------------operation demamde configuration----
        //-------------------------------------------------------------
        /*$('#selected_cin_demande').change(function(){
            alert('ok');
        });*/
        //-----------------Supprimer de mande !

        /*--------------------------Ajouter demande-----------
        ------------------------------------------------------
        ------------------------------------------------------
        */
        //$('#btn-ajouter-demande').click(function(event) {
            /* Act on the event */
            //$('#conge-application-historique').hide();
            //$('#container-add-leave-demande').fadeIn(900,'swing');
            //$('#btn-reteur-historique-page').click(function(){
                //$('#container-add-leave-demande').hide();
                //$('#conge-application-historique').fadeIn(900,'swing');
            //});
        //});
        //-------------------------------------------------------------
        //-------------- Validation form ajout demande-----------------
        //-------------------------------------------------------------
        //$('#form-add-leave').validate();
        $.validate({
            //modules : 'date, security'
        });
        
        /*-----------------------------
        ----------------Show dialog-----
        $(document).ready(function(){
    $("#customFieldDialog").dialog({
      resizable: false,
      modal: true,
      autoOpen: false,
      width:315,
      buttons: {
        "Save" : function() {
          $("#customFieldForm").submit();
        },
        "Cancel" : function() {
          $(this).dialog("close");
          return false;
        }
      }
    });
    */
    //----------------------------------------------------
    //****************************************************
    //          Bloc edit demande
    //---------------------------------------------------

    $('#icon-ed-current-leave').click(function(event) {
        /* Act on the event */
        //var currentCIN=$(this).parent().prev().prev().prev().prev().prev().prev().prev().text();

        //$('#conge-application-historique').hide();
        //$('#container-edit-leave-demande').fadeIn(900, function() {
            //Stuff to do *after* the animation takes place
        //});
        //$('#ed-cin').attr('value',currentCIN);
        //var currentCIN='';
        var currentCIN=$('#selected_cin_demande').val();
        if (currentCIN=='' && currentCIN.length<4) {
            swal(
                'Ereur......!',
                'S\'il vous plait ! Selectionner le CIN de la demande a editer !',
                 'error'
            );
            event.preventDefault();
        }
        if (currentCIN.length>4) {
            /*$.ajax({
                url:'index_agent_edit_leave',
                type:'POST',
                data:currentCIN,
                dataType:'json'
            });*/
            
            
        }

    });
    //------------------------------------------------
    //**********************************************
    //          Bloc supprimer demande
    //----------------------------------------------
    $('#submit-supp-current-leave').click(function(event) {
        /* Act on the event */
        //event.preventDefault();
        var currentCIN=$('#selected_cin_demande').val();
        if (currentCIN=='' && currentCIN.length<4) {
            swal(
                'Ereur......!',
                'S\'il vous plait ! Selectionner le CIN de la demande a editer !',
                 'error'
            );
            event.preventDefault();
        }
        if (currentCIN.length>4) {
           swalDelete(currentCIN);
           event.preventDefault(); 
        }

    });
    //---------------------------------------------
    //                  Flash messages              
    //----------------------------------------------
    $('.alert').fadeIn(3200).delay(3800).fadeOut(1800);

    //-----------------------------------------------------
    //              Index agent profile
    //----------------------------------------------------
    $('#formulaire_update_profile [type="text"]').addClass('form-control');
    $('#formulaire_update_profile [type="email"]').addClass('form-control');
    $('#formulaire_update_profile [type="text"]').attr({
        'data-validation':'length alphanumeric',
        'data-validation-length':'min4'
    });
    //----------------------
    //  Verifier le formulaire de update user profile
    /*$('.form-control').eq(0).keyup(function(){
        var usernameRegex =  new RegExp('/[a-zA-Z0-9_-]{4,16}$/'); 
        var emailRegex = '^[A-Z0-9._%+-]+@[A-Z0-9.-]+.[A-Z]{2,4}$';
        $val=$(this).val();
        if(usernameRegex.test($val)){
            $(this).css('border','2px solid green');
        }
        else{
            $(this).css('border','2px solid red')
        }
    });*/
    /*$('#formulaire_update_profile').submit(function(e){
        username=$('.form-control').eq(0).val();
        nom=$('.form-control').eq(1).val();
        prenom=$('.form-control').eq(2).val();
        email=$('.form-control').eq(3).val();
        if (username.length>=4 && nom.length>=4 && prenom.length>=4){
            e.preventDefault();
            swal(
                'Ooops......!',
                'S\'il vous plait ! verifiez bien les entrees  !',
                 'error'
            );
        } 
        
    });*/
    //*********************************************** */
    //************ Bloc changer password  */
    $('#form-changer-password [type="password"]').addClass('form-control');
    $('#form-changer-password [type="password"]').attr({
        'data-validation':'password',
        'data-validation-length':'min8'
    });
});
