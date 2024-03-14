var socketio = io();

var messages = document.getElementById('messages');

const create_chatMessage = (name, message, date, color) => {
    const chatMessage_content = `
        <div class="message">
            <span>
                <strong style='color: ${color}'>${name}</strong>: ${message}
            </span>
            <span class="date">${date}</span>
        </div>
    `;
    messages.innerHTML += chatMessage_content;

    messages.scrollTo(0, messages.scrollHeight);
};

const create_join_leave = (message, date) => {
    const leave_join_content = `
        <div class="message">
            <span>
                ${message}
            </span>
            <span class="date">${date}</span>
        </div>
    `;
    messages.innerHTML += leave_join_content;

    messages.scrollTo(0, messages.scrollHeight);
};

const create_memberCount_leave = (message, members, membersText) => {
    const memberCount_content = `
        <div class="message">
            <span>
                ${message} <span class="members">${members}</span> ${membersText}
            </span>
        </div>
    `;

    messages.innerHTML += memberCount_content;

    messages.scrollTo(0, messages.scrollHeight);
};

const create_memberCount_join = (message, members, hauseName) => {
    const memberCount_content = `
        <div class="message">
            <span>
                ${message} <span class="members">${members}</span> member of ${hauseName}
            </span>
        </div>
    `;

    messages.innerHTML += memberCount_content;

    messages.scrollTo(0, messages.scrollHeight);
};

const create_nwordcounterlessthan30 = (nwords, word) => {
    const nwordcounter_content = `
        <div class="message">
            <span>
                <strong>N-Word Counter: </strong>${nwords} ${word} reached, ${30-nwords} more to go!
            </span>
        </div>
    `;

    messages.innerHTML += nwordcounter_content;

    messages.scrollTo(0, messages.scrollHeight);
};

const nwordcounter30 = () => {
    const nwordcounter_content = `
        <div class="message">
            <span>
                <strong>N-Word Counter: </strong> THIS HAUSE HAS ATTAINED DIVINE COTTON FARMING POWERS!
            </span>
        </div>
    `;
    divinenword = document.getElementById("divinenword");
    
    divinenword.play(0)
    messages.innerHTML += nwordcounter_content;

    messages.scrollTo(0, messages.scrollHeight);
};

const create_nwordcountermorethan30 = (nwords) => {
    const nwordcounter_content = `
        <div class="message">
            <span>
                <strong>N-Word Counter: </strong>${nwords}
            </span>
        </div>
    `;

    messages.innerHTML += nwordcounter_content;

    messages.scrollTo(0, messages.scrollHeight);
};

socketio.on("join_leave", (data) => {
    create_join_leave(data.message, data.date);
});

socketio.on("memberCount_leave", (data) => {
    create_memberCount_leave(data.message, data.members, data.membersText);
});

socketio.on("memberCount_join", (data) => {
    create_memberCount_join(data.message, data.members, data.hauseName);
});

socketio.on("chatMessage_send", (data) => {
    create_chatMessage(data.name, data.message, data.date, data.color);
});

socketio.on("nwordcounterlessthan30", (data) => {
    create_nwordcounterlessthan30(data.nwords, data.word);
});

socketio.on("nwordcounter30", (data) => {
    nwordcounter30(data.nwords);
});

socketio.on("nwordcountermorethan30", (data) => {
    create_nwordcountermorethan30(data.nwords);
});

const sendMessage = () => {
    const messageInput = document.getElementById('message');

    if (messageInput.value == "") return

    socketio.emit("chatMessage", {message: messageInput.value});
    messageInput.value = "";
};

const leave = () => {
    window.location.href = "/";
};

//send message on clicking enter
document.getElementById('message').addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("send").click();
  }
});

