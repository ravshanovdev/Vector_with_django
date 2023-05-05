const showBtn = document.querySelector('.show-buttons')
const closeBtn = document.querySelector('.close-buttons')
const closeBtnTwo = document.querySelector('.close-btn_two')
const overlay = document.querySelector('.overlay')
// right
const right = document.querySelector('.right')
const buttonRight = document.querySelector('.button-right')
const buttonLeft = document.querySelector('.button-left')
const closeButton = document.querySelector('.close-button')
const btnLeftTwo = document.querySelector('.button-left')
const btnRightTwo = document.querySelector('.btnRight')
const showBtnTwo = document.querySelector('.show-buttons_two')

// =======
const showBtns = document.querySelector('.show-buttonss')
const showBtnThree = document.querySelector('.show-buttons_three')
const share = document.querySelector('.share')







// remove claslist right
const removeRight = () => {
    right.classList.remove('right')
    overlay.classList.remove('hidden')
    // modal.classList.add('hidden')


}

// add claslist Right
const addRight = ()=>{
    right.classList.add('right')
    overlay.classList.add('hidden')



}

// add claslist hidden
const addHidden = ()=>{
    modal.classList.add('hidden')
    overlay.classList.add('hidden')
    
}

// remove claslist hidden
const removeHidden = () => {
    modal.classList.remove('hidden')
    overlay.classList.remove('hidden')

}
// ======================================================= two 
// add claslist right Two
const removeRightTWo = () => {
    right.classList.add('right')
    overlay.classList.add('hidden')
}


// remove claslist right Two

const removeHiddenTwo = () => {
    modal.classList.remove('hidden')
    overlay.classList.remove('hidden')

}
const close = () =>{
    right.classList.add('right')
    modal.classList.add('hidden')
    overlay.classList.add('hidden')

}
// ============================================================

showBtn.addEventListener('click',removeHidden)
closeBtn.addEventListener('click',close)
overlay.addEventListener('click', addHidden)
closeBtnTwo.addEventListener('click', close)
buttonRight.addEventListener('click', removeRight)
closeButton.addEventListener('click',close)
buttonLeft.addEventListener('click', addRight)
showBtnTwo.addEventListener('click', removeRight)
btnLeftTwo.addEventListener('click', removeHiddenTwo)
btnRightTwo.addEventListener('click', removeRightTWo)

document.addEventListener('keydown', (e)=>{
    if(e.key == 'Escape'){
        close()
    }
})

showBtns.addEventListener('click',removeHidden)
share.addEventListener('click',removeHidden)
showBtnThree.addEventListener('click',removeRight)