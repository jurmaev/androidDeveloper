(() => {
    const closeBtn = document.querySelector('.sidenav__closebtn');
    const openBtn = document.getElementById('openbtn');
    const sidenav = document.getElementById('sidenav');
    const main = document.getElementById('main');

    function openNav() {
        sidenav.style.width = '300px';
        main.style.marginLeft = '300px';
        main.style.opacity = '0.33';
        closeBtn.setAttribute('data-open') = 'true';
    }

    function closeNav() {
        sidenav.style.width = '0';
        main.style.marginLeft = '0';
        main.style.opacity = '1';
        closeBtn.setAttribute('data-open') = 'false';
    }

    closeBtn.addEventListener('click', closeNav);
    openBtn.addEventListener('click', openNav);

    const accs = document.querySelectorAll('.skills__accordion');
    console.log(accs)
    accs.forEach(acc => {
        acc.addEventListener('click', () => {
            acc.classList.toggle('skills__accordion--active');
            const panel = acc.nextElementSibling;
            if(panel.style.maxHeight) panel.style.maxHeight = null;
            else panel.style.maxHeight = panel.scrollHeight + "px";
        })
    });
})();