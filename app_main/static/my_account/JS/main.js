document.addEventListener("DOMContentLoaded", function() {

    const tabTitles = document.querySelectorAll('.tab-titles li');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabTitles.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');

            tabTitles.forEach(tab => tab.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    const fileInput = document.getElementById('user_image_input');
    const form = document.getElementById('update-user-image');

    fileInput.addEventListener('change', function() {
        form.submit();
    });

});