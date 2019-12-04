$(function () {

    let listOfAnswers = [''];
    let sessionId = Math.random().toString(36).substring(7);
    const theUrl = '/generate';
    // Define some elements from the DOM and utility methods.
    let $form = $("#msgForm"),
        $newMsg = $form.find("input"),
        $sendBtn = $form.find("button"),
        $feed = $("#msgs"),
        _wait = ms => new Promise((r) => setTimeout(r, ms)), // See [0]
        _secs = (a, b) => Math.floor(Math.random() * (b - a + 1)) + a;

    // Define our send method.
    var _send = data => {
        // Send data to a new .msg
        let $msg = $('<div class="msg"></div>'),
            {sender, typing} = data;
        if (sender !== "me") {
            $msg.addClass("to");
        } else {
            $msg.addClass("from");
        }
        $msg.text(data.msg);

        if (typing) {
            $msg.addClass("typing");
            $msg.addClass("flashit");
        }

        $msg.appendTo($feed);
        // If sending was successful, clear the text field.
        $newMsg.val("");
        // And simulate a reply from our agent.
        if (sender === "me") setTimeout(_agentReply, 1000);
        if (typing) return $msg; // ref to new DOM .msg
    };


    var _agentReply = () => {
        // After a few seconds, the agent starts to type a message.
        let waitAfew = _wait(_secs(1000, 2000)),
            showAgentTyping = async () => {
                console.log("Bot is typing...");
                // Let the user know the agent is typing
                let $agentMsg = _send({msg: "Bot is typing...", typing: true, sender: false});
                document.body.scrollTop = document.body.scrollHeight; // For Safari
                document.documentElement.scrollTop = document.documentElement.scrollHeight; // For Chrome, Firefox, IE and Opera
                // and in a few seconds show the typed message.
                waitAfew.then(() => {
                    // @TODO: Simulate actual typing by removing the typing message when the agent isn't typing, and before the agent sends the typed message. Also allow typing to continue a number of times with breaks in between.
                    maxEntries = listOfAnswers.slice(1).slice(-4).join(" ");

                    request = $.ajax({
                        type: "POST",
                        url: theUrl,
                        data: {
                            'data': maxEntries,
                            'sess': sessionId
                        }
                    });
                    request.done(function (response) {
                        listOfAnswers.push(response);
                        $agentMsg.text(response);
                        $agentMsg.removeClass("flashit");
                        $agentMsg.removeClass("typing");
                    });
                    request.fail(function () {

                        $agentMsg.text(response);
                        $agentMsg.removeClass("flashit");
                        $agentMsg.removeClass("typing");
                    });


                });

            };
        waitAfew.then(showAgentTyping());
    };

    // Define event handlers: Hitting Enter or Send should send the form.
    $newMsg.on("keypress", function (e) {
        // @TODO: Allow [mod] + [enter] to expand field & insert a <BR>
        if (e.which === 13) {
            // Stop the prop
            e.stopPropagation();
            e.preventDefault();
            // Wrap the msg and send!
            let theEnvelope = {
                msg: $newMsg.val(),
                sender: "me"
            };
            listOfAnswers.push($newMsg.val());
            return _send(theEnvelope);
        } else {
            // goggles
        }
    });
    $sendBtn.on("click", function (e) {
        // Stop the prop
        e.stopPropagation();
        e.preventDefault();
        // Wrap the msg and send!
        listOfAnswers.push($newMsg.val());
        let theEnvelope = {
            msg: $newMsg.val(),
            sender: "me"
        };
        return _send(theEnvelope);
    });
});