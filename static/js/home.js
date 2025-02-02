loginBtn = document.getElementById('login-btn');
loginBtn.addEventListener('click', function(){
    window.location.href='/login';
});

registerBtn = document.getElementById('register-btn');
registerBtn.addEventListener('click', function(){
    window.location.href='/register';
});

addFood = document.getElementById('add-food');
addFood.addEventListener('click', function(){
    console.log('HI')
    window.location.href='/add';
});