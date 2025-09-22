// 图片数据
const images=[];
for(let i=1;i<=60;i++){ images.push({id:`cartoon-${i}`,category:"卡通",title:`卡通 ${i}`,src:`avatar/cartoon/${i}.jpg`}); }
for(let i=1;i<=209;i++){ images.push({id:`flash-${i}`,category:"闪图",title:`闪图 ${i}`,src:`avatar/flash/${i}.gif`}); }
for(let i=1;i<=100;i++){ images.push({id:`bg-${i}`,category:"背景图",title:`背景图 ${i}`,src:`avatar/background/${i}.jpg`}); }

// 状态
let activeCat="全部", query="", visible=[], page=0, pageSize=40, currentIndex=0;
const masonry=document.getElementById("masonry");
const emptyEl=document.getElementById("empty");

// 洗牌函数
function shuffleArray(array){
  const arr = array.slice();
  for(let i=arr.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// 渲染批量
function renderBatch(reset=true){
  const q=query.trim().toLowerCase();
  visible=images
    .filter(i => activeCat==="全部" ? true : i.category===activeCat)
    .filter(i => i.title.toLowerCase().includes(q));

  // 首页随机打乱显示
  visible = shuffleArray(visible);

  if(reset){ 
    page=0; 
    masonry.innerHTML=""; 
  }
  if(visible.length===0){ 
    emptyEl.style.display="block"; 
    return; 
  } else emptyEl.style.display="none";

  const start=page*pageSize, end=start+pageSize, batch=visible.slice(start,end);
  batch.forEach((img,idx)=>{
    const fig=document.createElement("div"); fig.className="card";
    const imgEl=document.createElement("img"); imgEl.src=img.src; imgEl.alt=img.title; imgEl.loading="lazy"; imgEl.onclick=()=>openLightbox(start+idx);
    const meta=document.createElement("div"); meta.className="meta"; meta.innerHTML=`<div>${img.title}</div><div class="cat">${img.category}</div>`;
    fig.appendChild(imgEl); fig.appendChild(meta);
    masonry.appendChild(fig);
  });
  page++;
}

// 滚动加载更多
window.addEventListener("scroll",()=>{
  if(window.innerHeight+window.scrollY>=document.body.offsetHeight-200){
    if(page*pageSize<visible.length) renderBatch(false);
  }
});

// 分类按钮
document.querySelectorAll(".filters button").forEach(btn=>{
  btn.onclick=()=>{
    document.querySelectorAll(".filters button").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    activeCat=btn.dataset.cat;
    query=""; document.getElementById("search").value="";
    renderBatch(true);
  };
});

// 搜索
document.getElementById("search").addEventListener("input",e=>{
  query=e.target.value;
  renderBatch(true);
});

// Lightbox
function openLightbox(idx){
  currentIndex=idx;
  const item=visible[idx];
  document.getElementById("lightbox-img").src=item.src;
  document.getElementById("lightbox-caption").textContent=item.title+" ("+item.category+")";
  document.getElementById("lightbox").style.display="flex";
}
function closeLightbox(){document.getElementById("lightbox").style.display="none";}
function navLightbox(dir){currentIndex=(currentIndex+dir+visible.length)%visible.length; openLightbox(currentIndex);}
window.addEventListener("keydown",e=>{
  if(document.getElementById("lightbox").style.display==="flex"){
    if(e.key==="ArrowRight") navLightbox(1);
    if(e.key==="ArrowLeft") navLightbox(-1);
    if(e.key==="Escape") closeLightbox();
  }
});

// 初始化
renderBatch(true);