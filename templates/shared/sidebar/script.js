wtf.header = {
    data: {
        mobileBtn: document.getElementById('m-nav-btn'),
        sideBar: document.querySelector('.sidebar')
    }
};
(function () {
    document.addEventListener('DOMContentLoaded', () => {
        wtf.header.data.mobileBtn.addEventListener('click', () => {
            wtf.header.data.sideBar.classList.toggle('active');
        });
    });
}());