
$(document).ready(function(){
    
    //=======================================
    //              Add employe
    //====================================
    
    $('#form-add-employe [type="text"]').addClass('form-control');
    $('#form-add-employe [type="email"]').addClass('form-control');
    $('#form-add-employe [type="text"]:not(eq(5))').attr({
        'data-validation':'length alphanumeric',
        'data-validation-length':'min4'
    });
    $('#form-add-employe [type="email"]').attr({
        'data-validation':'email'
    });
    //=====================================
    //----------------------------------------------
    //          Edit  employe
    //--------------------------------------------
    var cin_edit_emp='';
    $('.edit_employe').click(function(e){
        $("#employes-historique").hide();
        $("#edit_employe").fadeIn(1200);
        var $current_cin=$(this).parent().prev().prev().prev().prev().prev().text();
        var $current_nom_prenom=$(this).parent().prev().prev().prev().prev().text()
        var $current_tel=$(this).parent().prev().prev().prev().text()
        var $current_service=$(this).parent().prev().prev().text()
        var $table_nom_prenom=$current_nom_prenom.split(" ");
        var $current_nom=$table_nom_prenom[0];
        var $current_prenom=$table_nom_prenom[1];
        e.preventDefault();
        $('#form-edit-employe [type="text"]:eq(0)').attr('value',$current_cin);
        $('#form-edit-employe [type="text"]:eq(1)').attr('value',$current_nom);
        $('#form-edit-employe [type="text"]:eq(2)').attr('value',$current_prenom);
        $('#form-edit-employe [type="email"]:eq(0)').attr('value','abc.example@gmail.com');
        $('#form-edit-employe [type="tel"]:eq(0)').attr('value',$current_tel);
        $('#form-edit-employe [type="text"]:eq(3)').attr('value',$current_service);
        /*$.ajax({
            url:'{% url "instance_emp_ajax" %}',
            type:'GET',
            data:{
                'current_cin':current_cin
            },
            dataType:'json'
        });*/
        //$('#cin_edit').val()=current_cin;
    });
    $('#icon-ed-current-employe').click(function(e){
        
        var $cin_emp=$('#selected_cin_employe').val()=cin_edit_emp;
        if($cin_emp=='' || $cin_emp.lenght()<=4){
            e.preventDefault();
            swal(
                'Ereur......!',
                'S\'il vous plait ! Selectionner le CIN de la demande a editer !',
                 'error'
            );
              
        }
    });
    //================================================================
    //                      search employe
    //----------------------------------------------------------------
    $('#serach-emp').focus(function(){
        $('#employes_table').hide();
        $('#other-table').fadeIn(1000);
    });
    $('#serach-emp').blur(function(){
        
        $('#other-table').hide();
        $('#employes_table').fadeIn(1000);
        $('#serach-emp').attr('value',' ');
    });
    //===========================================
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
        $('.userRH-existe').css('color','red');
        $('.userRH-existe').css('background','red');
    });
    $('.logou-button').mouseleave(function(event) {
        /* Act on the event */
        $('.userRH-existe').css('color','lightgreen');
        $('.userRH-existe').css('background','lightgreen');
    });
    //----------------------------------------
    //          Validation forms
    //--------------------------------------
    $.validate({
        //modules : 'date, security'
    });
    //---------------------------------------------------
    //---------------------------------------------
    //                  Flash messages              
    //----------------------------------------------
    $('.alert').delay(3800).fadeOut(1800);
    $('.show-inf-error').delay(3800).fadeOut(1800);
    //--------------------------------------------------
    //-----------------------------------------------------
    //              Index superRH profile
    //----------------------------------------------------
    
    $('#formulaire_update_profile [type="text"]').addClass('form-control');
    $('#formulaire_update_profile [type="email"]').addClass('form-control');
    $('#formulaire_update_profile [type="text"]').attr({
        'data-validation':'length alphanumeric',
        'data-validation-length':'min4'
    });
});