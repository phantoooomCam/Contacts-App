const bntDelete = document.querySelectorAll('.btn-delete')

if (bntDelete){
    const btnArray= Array.from(bntDelete)
    btnArray.forEach((btn) => {
        btn.addEventListener('click',(e)=>{
            if(!confirm('Are you sure you want to delete it?')){
                e.preventDefault();
            }
    
        });
    });
}