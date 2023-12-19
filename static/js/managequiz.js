
const back = document.getElementById('back')
back.addEventListener('click',()=>{
    console.log(window.location.host)
    window.location.href = `/dashboard/manage_course/${back.getAttribute('data-course')}`
})

