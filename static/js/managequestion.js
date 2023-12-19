const back = document.getElementById('back')
back.addEventListener('click',()=>{
    console.log(window.location.host)
    window.location.href = `/dashboard/manage_quiz/${back.getAttribute('data-course')}`
})

