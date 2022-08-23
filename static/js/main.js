const btn_delete = document.querySelectorAll('.delete');
//const campSelect = document.getElementById

if(btn_delete){
  const btn_array = Array.from(btn_delete);
  btn_array.forEach((btn)=> {
    btn.addEventListener('click', (evt)=>{
      if(!confirm("Registro eliminado")){
          evt.preventDefault();
      }
    });  
  });   
}

const close = document.querySelector('#close')
if (close){
  setTimeout(()=>{
    close.remove()
  }, 3000);
}