// 这里可以放置您的JavaScript代码
document.addEventListener('DOMContentLoaded', function() {
    var analyzeButton = document.getElementById('analyze-button');
    analyzeButton.addEventListener('click', function() {
        var formData = new FormData(document.getElementById('resume-matching-form'));
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            // data = data.replace(/\n/g, '<br>');  // 将\n换成<br>
            document.getElementById('analysis-result').innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
