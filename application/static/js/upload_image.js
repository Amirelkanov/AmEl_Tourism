'use strict';

(function (document, window, index) {
    let inputs = document.querySelectorAll('.custom-file-input');
    Array.prototype.forEach.call(inputs, function (input) {
        let label = input.nextElementSibling,
            labelVal = label.innerHTML;

        input.addEventListener('change', function (e) {
            let fileName;
            if (this.files.length > 1 && this.files) {
                fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}',
                    this["files"].length);
            } else
                fileName = e.target.value.split('\\').pop();

            if (fileName)
                label.querySelector('span').innerHTML = fileName;
            else
                label.innerHTML = labelVal;
        });

    });
}(document, window, 0));