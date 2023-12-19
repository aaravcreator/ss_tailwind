const btn= document.getElementById('quiz-btn')
btn.addEventListener('click',()=>{
    const course = btn.getAttribute('data-course')
    const lesson = btn.getAttribute('data-pk')
    console.log(course,lesson)
    window.location.href = `/quiz/${course}/${lesson}/`
    
})
