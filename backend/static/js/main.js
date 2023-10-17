$(".person").on('click', function(){
    $(this).toggleClass('focus').siblings().removeClass('focus');
})