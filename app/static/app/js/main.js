(() => {
    const closeBtn = document.querySelector('.sidenav__closebtn');
    const openBtn = document.getElementById('openbtn');
    const sidenav = document.getElementById('sidenav');
    const main = document.getElementById('main');

    function openNav() {
        sidenav.style.width = '300px';
        main.style.marginLeft = '300px';
        main.style.opacity = '0.33';
        // main.style.backgroundColor = 'rgba(240,240,240,0.4)';
        closeBtn.setAttribute('data-open') = 'true';
    }

    function closeNav() {
        sidenav.style.width = '0';
        main.style.marginLeft = '0';
        main.style.opacity = '1';
        // main.style.backgroundColor = 'transparent';
        closeBtn.setAttribute('data-open') = 'false';
    }

    closeBtn.addEventListener('click', closeNav);
    openBtn.addEventListener('click', openNav);
})();