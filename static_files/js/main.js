console.log('i am working ')


let likeBtns = document.getElementsByClassName('favourites');

for(let i = 0 ; i <likeBtns.length; i++ ){
   
    likeBtns[i].addEventListener('click',function(){
        let itemId = this.dataset.item
        let action = this.dataset.action

       
        
         updateItemLikes(itemId,action)
         
    })


}

const updateItemLikes = (itemId,action) => {
    
   

    let url = '/like/'

    fetch(url , {
        method: 'POST',
        headers:{
            'Content-Type': 'application/Json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'itemId':itemId ,'action':action})
    })
    .then(response => response.json())
    .then(data => {
        location.reload()
        console.log(data)
       

    })

    

}