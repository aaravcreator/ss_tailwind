const url = window.location.href
var confettiSettings = { target: 'my-canvas' };
var confetti = new ConfettiGenerator(confettiSettings);
confetti.render();
const quizbox = document.getElementById('quiz-box')
const canvas = document.getElementById('my-canvas')

$.ajax({
    type:'GET',
    url:`${url}data/`,
    success: function(response){
        
        const data = response.data 
        
        let count = 0;
        data.forEach(element => {
            for(const [question,answers] of Object.entries(element)){
                count = count+1;
                
                
                    quizbox.innerHTML += `
                            <hr>
                            <div class = "mb-2"> 
                                <b>
                                    ${count}) ${question}
                                </b>
                            </div>

                            

                    `
                    
                    answers.forEach(answer=>{
                            // console.log(question)
                            quizbox.innerHTML  +=
                            
                            `
                                <div>
                                    <input type = "radio" class = "ans" id = "${question}-${answer}" name ="${question}" value = "${answer}">
                                    <label for= "${question} ">${answer}</label>
                                </div>
                            `
                    })
            }
            
        });
 
    },
    error:function(error){
        console.log(error)
    }
})

const quizform = document.getElementById('quiz-form')
const message_alert = document.getElementById('message-alert')
const failed_alert = document.getElementById('failed_alert')
const passed_alert = document.getElementById('passed-alert')
const countdown = document.getElementById('countdown')
const countdown1 = document.getElementById('countdown1')
console.log(passed_alert)
const csrf = document.getElementsByName('csrfmiddlewaretoken')
// console.log(message_alert)

const sendData = ()=>{
    const element = [...document.getElementsByClassName('ans')]
    // console.log(url)
    
    
    const data = {}
    data['csrfmiddlewaretoken'] =csrf[0].value
    let count_selected =0
    element.forEach(el=>{
        
        
        if (el.checked){
            count_selected = count_selected+1
            data[el.name] = el.value
        }
        else{
            
            if (!data[el.name]){
                data[el.name] = null
                
                
            }
        }
    })
    // console.log(count_selected)
    if (count_selected!=0){

        $.ajax({
            type:'POST',
            url:`${url}save/`,
            data:data,
            success: function(res){
                
    
                // console.log(res.empty)
                
                const results = res.passed  
                // console.log(results)
                if (results == false){
                    let counting = 3;
                    // console.log(res.lesson_number)
                    failed_alert.classList.remove('not-visible')
                    setInterval(function() { handleTimer(); }, 950);
                    setTimeout(()=>{
                        window.location.href = `/course/${res.course}/${res.lesson_number}`
                    },3500)
                    function handleTimer(){
                        countdown.innerHTML =  `<p class = "text center">${counting}</p>`
                        counting--;
                    }
                    

                }
                else if (results == true){
                    if (res.last_lesson){
                        
                        passed_alert.classList.remove('not-visible')
                        passed_alert.innerHTML = `
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                         </button>
                        <h1 class="text-center" style="color:black;">Congrats you compleated the course  </h1>
                        <br>
                    
                        
                        `
                        document.getElementById('savebtn').display = "none"
                        canvas.classList.remove('not-visible')
                        setTimeout(()=>{
                            canvas.classList.add('not-visible')
                        },3500)
                        
                        
                        
                    }
                    else{

                        let counting = 4;
                    
                        passed_alert.classList.remove('not-visible')
                        setInterval(function() { handleTimer(); }, 950);
                        setTimeout(()=>{
                            window.location.href = `/course/${res.course}/${res.lesson_number}`
                        },3500)
                        function handleTimer(){
                            countdown1.innerHTML =  `<p class = "text center">${counting}</p>`
                            counting--;
                        }
                        
                    }   
                    
                    
                }
                
                quizbox.classList.add('not-visible')
                
                
                
            },
            error:function(error){
                console.log(error)
            }
        })

    }
    else{
        
            message_alert.classList.remove('not-visible')
            setTimeout(()=>{
                message_alert.classList.add('not-visible');
                // message_alert.fadeOut();
            },2000)
            
        }
        
}
    


quizform.addEventListener('submit',(e)=>{
    e.preventDefault()
    sendData()
    

})