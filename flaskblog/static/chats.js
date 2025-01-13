document.addEventListener("DOMContentLoaded", function () {
    const messagesWrapper = document.getElementById("messages-wrapper");
    if (messagesWrapper) {
        messagesWrapper.scrollTop = messagesWrapper.scrollHeight;
    }
});
