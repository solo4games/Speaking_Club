function chooseIt(el) {
    current = el.closest('ul').querySelector('.active');
    if (current !== null) {
        current.classList.remove('active');
    }
    el.classList.add('active');
}