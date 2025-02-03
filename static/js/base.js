const siteTitle = document.getElementById('site-title');
siteTitle.addEventListener('click', function(){
    window.location.href='/'
});

const logoutBtn = document.getElementById('site-logout');
logoutBtn.addEventListener('click', function(){
    window.location.href='/logout'
});
