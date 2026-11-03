document.addEventListener("DOMContentLoaded", () => {
    const sourceText = window.PRACTICE_SOURCE_TEXT || "";

    const textDisplay = document.getElementById("text-display");
    const typingInput = document.getElementById("typing-input");
    const timerElement = document.getElementById("timer");
    const wpmElement = document.getElementById("wpm");
    const cpmElement = document.getElementById("cpm");
    const accuracyElement = document.getElementById("accuracy");
    const errorsElement = document.getElementById("errors");

    const resultForm = document.getElementById("result-form");
    const typedTextInput = document.getElementById("typed-text-input");
    const durationInput = document.getElementById("duration-input");
    const charactersInput = document.getElementById("characters-input");
    const correctInput = document.getElementById("correct-input");
    const incorrectInput = document.getElementById("incorrect-input");
    const accuracyInput = document.getElementById("accuracy-input");
    const wpmInput = document.getElementById("wpm-input");
    const cpmInput = document.getElementById("cpm-input");

    const restartButton = document.getElementById("restart-button");
    const finishButton = document.getElementById("finish-button");

    let startTime = null;
    let timerInterval = null;
    let isFinished = false;

    function renderText() {
        textDisplay.innerHTML = "";

        for (let i = 0; i < sourceText.length; i++) {
            const span = document.createElement("span");
            span.textContent = sourceText[i];
            span.dataset.index = i;
            textDisplay.appendChild(span);
        }

        updateHighlight("");
    }

    function updateHighlight(typedText) {
        const spans = textDisplay.children;
        let correct = 0;
        let incorrect = 0;

        for (let i = 0; i < spans.length; i++) {
            const span = spans[i];
            const expectedChar = sourceText[i];
            const typedChar = typedText[i];

            span.classList.remove(
                "correct",
                "incorrect",
                "current",
                "pending"
            );

            if (typedChar === undefined) {
                span.classList.add("pending");

                if (i === typedText.length) {
                    span.classList.add("current");
                }
            } else if (typedChar === expectedChar) {
                span.classList.add("correct");
                correct += 1;
            } else {
                span.classList.add("incorrect");
                incorrect += 1;
            }
        }

        return { correct, incorrect };
    }

    function calculateStats() {
        const typedText = typingInput.value;
        const { correct, incorrect } = updateHighlight(typedText);

        const typedCharacters = typedText.length;
        const elapsedSeconds = startTime
            ? Math.floor((Date.now() - startTime) / 1000)
            : 0;

        const minutes = elapsedSeconds / 60;

        const cpm = minutes > 0 ? typedCharacters / minutes : 0;
        const wpm = minutes > 0 ? typedText.trim().split(/\s+/).filter(Boolean).length / minutes : 0;

        const totalChecked = correct + incorrect;
        const accuracy = totalChecked > 0 ? (correct / totalChecked) * 100 : 100;

        timerElement.textContent = `${elapsedSeconds} c`;
        wpmElement.textContent = Math.round(wpm);
        cpmElement.textContent = Math.round(cpm);
        accuracyElement.textContent = `${accuracy.toFixed(1)}%`;
        errorsElement.textContent = incorrect;

        return {
            typedText,
            elapsedSeconds,
            typedCharacters,
            correct,
            incorrect,
            accuracy,
            wpm,
            cpm,
        };
    }

    function startTimer() {
        if (startTime || isFinished) {
            return;
        }

        startTime = Date.now();

        timerInterval = setInterval(() => {
            calculateStats();
        }, 1000);
    }

    function stopTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
    }

    function finishPractice() {
        if (isFinished) {
            return;
        }

        isFinished = true;
        stopTimer();

        const stats = calculateStats();

        typedTextInput.value = stats.typedText;
        durationInput.value = stats.elapsedSeconds;
        charactersInput.value = stats.typedCharacters;
        correctInput.value = stats.correct;
        incorrectInput.value = stats.incorrect;
        accuracyInput.value = stats.accuracy.toFixed(2);
        wpmInput.value = stats.wpm.toFixed(2);
        cpmInput.value = stats.cpm.toFixed(2);

        resultForm.submit();
    }

    function restartPractice() {
        typingInput.value = "";
        startTime = null;
        isFinished = false;
        stopTimer();
        renderText();
        calculateStats();
        typingInput.focus();
    }

    typingInput.addEventListener("input", () => {
        startTimer();

        if (typingInput.value.length >= sourceText.length) {
            finishPractice();
        }
    });

    typingInput.addEventListener("paste", (event) => {
        event.preventDefault();
    });

    restartButton.addEventListener("click", restartPractice);
    finishButton.addEventListener("click", finishPractice);

    renderText();
    calculateStats();
    typingInput.focus();
});