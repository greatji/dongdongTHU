$(".menu,#menu").click(function(){
		$(".dh_tc").stop().animate({"left":"0px"},400);
		$(".mengban").stop().fadeIn();
});
$(".mengban").click(function(){
		$(".dh_tc").stop().animate({"left":"-520px"},400);
		$(".mengban").stop().fadeOut();
});















//返回顶部
$(".xxxxxxxxx").click(function(){
		$('html, body').animate({scrollTop:0}, 600);
});

//
var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        slidesPerView: 1,
        paginationClickable: true,
        spaceBetween: 30,
        loop: true,
        autoplay: 3000,
        autoplayDisableOnInteraction: false
    });

function setTab(name,cursel,n){
 for(i=1;i<=n;i++){
  var menu=document.getElementById(name+i);
  var con=document.getElementById("con_"+name+"_"+i);
  if(menu) menu.className=((i==cursel)?"hover":"");
  if(con) con.style.display=((i==cursel)?"block":"none");
 }
}