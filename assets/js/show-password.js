/**
 * Show Password scriptlet
 * Adapted from: https://codepen.io/gabrieleromanato/pen/VYmrJV
 *
 * This scriptlet requires 2 elements:
 *     1. A password field with an id 'password'
 *     2. A 'Show password' element with an id 'show_password'
 */
(function() {
    document.addEventListener('DOMContentLoaded', function() {
        var toggle_button = document.querySelector('#show-password');
        var toggle_icon = document.querySelector('#show-password use');
        var password_field = document.querySelector('#password');

        if (toggle_button == null || password_field == null) { return; }

        toggle_button.addEventListener('click', function() {
            if (password_field.getAttribute('type') == 'password') {
                password_field.setAttribute('type', 'text');
                if (toggle_icon) {
                    toggle_icon.setAttribute('href', toggle_icon.getAttribute('data-show-icon'));
                }
            } else {
                password_field.setAttribute('type', 'password');
                if (toggle_icon) {
                    toggle_icon.setAttribute('href', toggle_icon.getAttribute('data-hide-icon'));
                }
            }
        }, false);
    });
})();
