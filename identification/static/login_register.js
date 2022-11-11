// console.log("loaded landing.js");

function changeActivetab(e) {
	const clickedTab = e.target;
	const tabs = clickedTab.parentElement.parentNode.children;

	for (let tab of tabs) {
		tab.className = "tab";
	}

	clickedTab.parentElement.className += " active";

	// for (let c of document.querySelector(".tab-content").children) {
	// 	if (c.id == clickedTab.href) c.style.display = "block";
	//   else c.style.display = "none"
	// }
}

const tabLinks = document.querySelectorAll(".tab-group a");

for (let t of tabLinks) {
	t.addEventListener("click", changeActivetab);
}

$(".tab a").on("click", function (e) {
  e.preventDefault();
  
  // $(this).parent().addClass('active');
  // $(this).parent().siblings().removeClass('active');
  
	target = $(this).attr("href");

	$(".tab-content > div").not(target).hide();

	$(target).fadeIn(1000);
});
