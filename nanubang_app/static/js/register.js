$(document).ready(function()
{
    
    $('.tag-label').click(function()
    {
        var radioVal = $(this).html();
        document.getElementById('id_tag').value = radioVal;
    })


    $("input:checkbox[class=id_room_options]").click(function()
    {
        var items=[];
        $('input[class="id_room_options"]:checkbox:checked').each(function(){items.push($(this).val());}); 
        var tmp = items.join(','); 
        document.getElementById('id_room_options').value = tmp;
        
    })

    $("input:radio[name=seller-info]").click(function()
    {
        var radioVal = $('input:radio[name="seller-info"]:checked').val();
        $('#seller-info-val').html(radioVal);
        document.getElementById('id_sublessor_type1').value = radioVal;
        document.getElementById('seller-info-val').value = radioVal;
        document.getElementById('id_kakaotalk').placeholder = radioVal+" 입력하기";
        
    })

    $("input:radio[name=is_duplex]").click(function()
    {
        var radioVal = $('input:radio[name="is_duplex"]:checked').val();
        if( radioVal === '예')
            document.getElementById('id_is_duplex').checked = true; 
        else
            document.getElementById('id_is_duplex').checked = false; 
    })
    
    $("#id_start_date" ).datepicker({
        dateFormat : 'yy-mm-dd',
		maxDate : 90,
        minDate : 0,
        onSelect: function (date) {
            var dt2 = $('#id_end_date');
            var startDate = $(this).datepicker('getDate');
            var minDate = $(this).datepicker('getDate');
            startDate.setDate(startDate.getDate() + 365);
            minDate.setDate(minDate.getDate() + 1);
            //sets dt2 maxDate to the last day of 30 days window
            dt2.datepicker('option', 'maxDate', startDate);
            dt2.datepicker('option', 'minDate', minDate);
        }
    });
    $("#id_end_date" ).datepicker({
        dateFormat : 'yy-mm-dd',
    });
    $("#id_photo1").change(function(){
        readURL(this,1);
        getImgName(1);
        document.getElementById('file-label1').style.display = "none";
        document.getElementById('file-label2').style.display = "block";
        document.getElementById('upload_desc').innerText = "다음 2번사진 업로드해주세요";
    });

    $("#id_photo2").change(function(){
        readURL(this,2);
        getImgName(2);
        document.getElementById('file-label2').style.display = "none";
        document.getElementById('file-label3').style.display = "block";
        document.getElementById('upload_desc').innerText = "다음 3번사진 업로드해주세요";
    });
    $("#id_photo3").change(function(){
        readURL(this,3);
        getImgName(3);
        document.getElementById('file-label3').style.display = "none";
        document.getElementById('file-label4').style.display = "block";
        document.getElementById('upload_desc').innerText = "다음 4번사진 업로드해주세요";
    });
    $("#id_photo4").change(function(){
        readURL(this,4);
        getImgName(4);
    });
    $("#id_photo5").change(function(){
        readURL(this,5);
        getImgName(5);
    });
    
    $("#upload_div").click(function()
    {
        if(document.getElementById('file-label2').style.zIndex == -1)
            document.getElementById('upload_input').click();
        else
            alert('이미지 2개이상 업로드 해주세요')
    });

});

function check1() {
    var chk_radio = document.getElementsByName('management_cost_include');
    var mancost_box = document.getElementById('id_management_cost_include');

    var sel_type = null;
    for (var i = 0; i < chk_radio.length; i++) {
        if (chk_radio[i].checked == true) {
            sel_type = chk_radio[i].id;
        }
    }
    if (sel_type == "id_management_cost_include_no") {
        mancost_box.readOnly = false;
        mancost_box.style.backgroundColor = '#ffffff';
        mancost_box.required = true;
    }
    else {
        mancost_box.readOnly = true;
        mancost_box.style.backgroundColor = '#bdbdbd';
        mancost_box.value = 0;
    }
}

function check2() {
    var chk_radio = document.getElementsByName('deposit_necessity');
    var mancost_box = document.getElementById('id_deposit_take');

    var sel_type = null;
    for (var i = 0; i < chk_radio.length; i++) {
        if (chk_radio[i].checked == true) {
            sel_type = chk_radio[i].id;
        }
    }
    if (sel_type == "deposit_necessity_no") {
        mancost_box.readOnly = true;
        mancost_box.style.backgroundColor = '#bdbdbd';
        mancost_box.value = 0;
    }
    else {
        mancost_box.readOnly = false;
        mancost_box.style.backgroundColor = '#ffffff';
        mancost_box.required = true;
    }
}

function fold() {
    var menus = document.getElementsByClassName("additional-field-btn")[0].parentElement.nextElementSibling;
    if (menus.classList.contains('folded')) {
        menus.classList.remove('folded');
    } else {
        menus.classList.add('folded');
    }
}

function tab1() {
    var tab1 = document.getElementsByClassName("tab1")[0];
    var tab2 = document.getElementsByClassName("tab2")[0];
    var tab1_content = document.getElementsByClassName("tab1-content")[0];
    var tab2_content = document.getElementsByClassName("tab2-content")[0];

    if (tab2.classList.contains('selected')) {
        tab2.classList.remove('selected');
        tab1.classList.add('selected');
        tab2_content.classList.add('folded');
        tab1_content.classList.remove('folded');
    }
}

function tab2() {
    var tab1 = document.getElementsByClassName("tab1")[0];
    var tab2 = document.getElementsByClassName("tab2")[0];
    var tab1_content = document.getElementsByClassName("tab1-content")[0];
    var tab2_content = document.getElementsByClassName("tab2-content")[0];

    if (tab1.classList.contains('selected')) {
        tab1.classList.remove('selected');
        tab2.classList.add('selected');
        tab1_content.classList.add('folded');
        tab2_content.classList.remove('folded');
    }
}

function readURL(input,num) 
{ 
    var id = "#image_section"+num;
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $(id).attr('src', e.target.result);
        }
 
        reader.readAsDataURL(input.files[0]);
    }
}
function getImgName(num)
{
    var id = "id_photo"+num;
    var imgName = document.getElementById(id);
    var fileName = imgName.value.split(/(\\|\/)/g).pop();
}

function img_reset()
{
    for(var i=1; i<5; i++)
    {
        var id1 = 'image_section'+i
        var id2 = 'file-label'+i
        document.getElementById(id1).src = "../static/img/img_icon_temp.png";
        document.getElementById(id2).style.zIndex = 5-i;
    }
}



